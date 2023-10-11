# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from contextlib import contextmanager
from pathlib import Path
import os
import csv

import frappe
from frappe import _
from frappe.core.page.permission_manager.permission_manager import add, reset, update


def install(country='China'):
	install_roles() # 添加角色
	install_user() # 添加测试账号
	install_user()  # 添加测试账号


def install_roles():
	premission_filepath = Path(__file__).parent.parent / "data" / 'premission.csv'
	with open(premission_filepath, mode='rt',encoding="utf8") as file:
		reader = csv.DictReader(file)

		#添加role
		roles = []
		for line in reader:
			if line['role'] not in roles:
				frappe.get_doc({'doctype':'Role','role_name':line['role']}).insert()
				frappe.db.commit()
				roles.append(line['role'])

		#添加premission
		premissions = []
		for line in reader:
			premission = {'parent': line['doctype'],'role': line['role'],'permlevel':line['permlevel']}
			if premission not in premissions:
				premissions.append(premission)
		for premission in premissions:
			add(**premission)
		frappe.db.commit()

		#更新premission
		for line in reader:
			premission = {'role': line['role'],
				'permlevel': int(line['permlevel']),
				'doctype': line['doctype'],
				'ptype': line['ptype'],
				'value': int(line['value'])}
			update(**premission)
		frappe.db.commit()

	# 添加模块集合
	frappe.get_doc({'doctype':'Module Profile','module_profile_name':'销售'}).insert()
	frappe.db.commit()
	
	# 设置模块集合的权限
	'''
	modules = frappe.db.get_list('Module Def','name')
	for module_name in modules:
		frappe.get_doc({'doctype':'Block Module','parent':'销售','module':module_name['name']}).insert()
		frappe.db.commit()
	'''
	frappe.db.delete('Block Module',filters = {'parent':'销售','module':'CRM'})
	frappe.db.commit()
	frappe.db.delete('Block Module',filters = {'parent':'销售','module':'Selling'})
	frappe.db.commit()

def install_user():
	premission_filepath = Path(__file__).parent.parent / "data" / 'user.csv'
	with open(premission_filepath, mode='rt',encoding="utf8") as file:
		reader = csv.DictReader(file)

		#添加role
		roles = []
		for line in reader:
			frappe.get_doc({'doctype':'User',
				   			'role_name':line['email'],
							'username':line['username'],
							'first_name':line['first_name']}).insert()
			frappe.db.commit()


@contextmanager
def install_user_premission(user_email=None,roles=None):
	# 为测试账号添加角色
	user = frappe.get_doc("User", "sale_a1@foxmail.com")
	user.add_roles("销售一线")
	frappe.db.commit()
	# 为测试账号添加模块组
	user.db_set('module_profile','销售',commit=True)