# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from contextlib import contextmanager
from pathlib import Path

import frappe
from frappe.core.page.permission_manager.permission_manager import add, reset, update




@contextmanager
def install_roles():
	import csv
	with open((Path(__file__).parent.parent / "data" / 'premission.csv'), mode='rt',encoding="utf8") as file:
		reader = csv.DictReader(file)

	#添加role
	roles = []
	for line in reader:
		roles.append({'role': line['role']})
	for role_name in list(set(roles)):
		frappe.get_doc({'doctype':'Role','role_name':role_name}).insert()
	frappe.db.commit()

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

	# 添加模块组
	
@contextmanager
def install_user(user_email=None,roles=None):

	# 添加测试账号
	user_info = {'doctype':'User',
				'email':"bmyxsyx1@foxmail.com",
				'username': 'A团队销售一线1',
				'first_name': 'A团队销售一线1'}
	frappe.get_doc(user_info).insert()
	frappe.db.commit()
	# 为测试账号添加角色
	user = frappe.get_doc("User", "atdxsyx1@foxmail.com")
	user.add_roles("销售一线")
	frappe.db.commit()
	# 为测试账号添加模块组
	user.db_set('module_profile','销售',commit=True)
