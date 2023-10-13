# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from contextlib import contextmanager
from pathlib import Path
import os
import csv
import json

import frappe
from frappe import _
from frappe.core.page.permission_manager.permission_manager import add, reset, update
from erpnext_china_mdm.setup.after_install.server_script import premission_lead
from frappe.desk.page.setup_wizard.setup_wizard import make_records

def read_lines(filename: str) -> list[str]:
	"""Return a list of lines from a file in the data directory."""
	return (Path(__file__).parent.parent / "data" / filename).read_text().splitlines()





def install(country='China'):
	install_roles() # 添加角色
	install_server_script() # 添加客户端脚本
	install_lead_source() # 添加线索来源
	# install_industry_type() # 添加行业
	add_uom_data() # 添加UOM
	# 测试环境载入数据
	install_user() # 添加测试账号
	install_user_premission()  # 为测试账号添加权限
	set_system_setting()

def install_server_script():
	frappe.get_doc(premission_lead.script).insert()
	frappe.db.commit()

def set_system_setting():
	frappe.db.set_single_value('System Settings', 'login_with_email_link', 0)
	frappe.db.commit()

def install_lead_source():
	# Lead Source 和 Industry Type
	frappe.db.delete('Lead Source')
	frappe.db.commit()

	records = []
	for doctype, title_field, filename in (
		("Lead Source", "source_name", "lead_source.txt"),
		):
		records += [{"doctype": doctype, title_field: title} for title in read_lines(filename)]
	make_records(records)

def install_industry_type():
	frappe.db.delete('Industry Type')
	frappe.db.commit()

	records = []
	for doctype, title_field, filename in (
		("Industry Type", "source_name", "industry_type.txt"),
		):
		records += [{"doctype": doctype, W: title} for title in read_lines(filename)]
	make_records(records)

def add_uom_data():
	frappe.db.delete('UOM')
	frappe.db.commit()
	frappe.db.delete('UOM Conversion Factor')
	frappe.db.commit()

	# add UOMs
	uoms = json.loads(
		open(frappe.get_app_path("erpnext_china_mdm", "setup", "after_install", "data", "uom_data.json")).read()
	)
	for d in uoms:
		if not frappe.db.exists("UOM", _(d.get("uom_name"))):
			frappe.get_doc(
				{
					"doctype": "UOM",
					"uom_name": _(d.get("uom_name")),
					"name": _(d.get("uom_name")),
					"must_be_whole_number": d.get("must_be_whole_number"),
					"enabled": 1,
				}
			).db_insert()

	# bootstrap uom conversion factors
	uom_conversions = json.loads(
		open(
			frappe.get_app_path("erpnext_china_mdm", "setup", "after_install", "data", "uom_conversion_data.json")
		).read()
	)
	for d in uom_conversions:
		if not frappe.db.exists("UOM Category", _(d.get("category"))):
			frappe.get_doc({"doctype": "UOM Category", "category_name": _(d.get("category"))}).db_insert()

		if not frappe.db.exists(
			"UOM Conversion Factor",
			{"from_uom": _(d.get("from_uom")), "to_uom": _(d.get("to_uom"))},
		):
			frappe.get_doc(
				{
					"doctype": "UOM Conversion Factor",
					"category": _(d.get("category")),
					"from_uom": _(d.get("from_uom")),
					"to_uom": _(d.get("to_uom")),
					"value": d.get("value"),
				}
			).db_insert()

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

	with open(premission_filepath, mode='rt',encoding="utf8") as file:
		reader = csv.DictReader(file)
		#添加premission
		premissions = []
		for line in reader:
			premission = {'parent': line['doctype'],'role': line['role'],'permlevel':int(line['permlevel'])}
			if premission not in premissions:
				add(**premission)
				frappe.db.commit()
				premissions.append(premission)
		
	with open(premission_filepath, mode='rt',encoding="utf8") as file:
		reader = csv.DictReader(file)
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
	user_filepath = Path(__file__).parent.parent / "data" / 'user.csv'
	with open(user_filepath, mode='rt',encoding="utf8") as file:
		reader = csv.DictReader(file)

		#添加role
		for line in reader:
			frappe.get_doc({'doctype':'User',
				   			'email':line['email'],
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