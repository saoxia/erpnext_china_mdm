# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import re
import frappe
from erpnext.selling.doctype.customer.customer import Customer
from erpnext_china_mdm.utils import qcc

class CustomCustomer(Customer):
	
	def validate(self):
		super().validate()
		self.clean_fields()

	def clean_fields(self):
		if self.customer_name:
			self.customer_name = str(self.customer_name).replace(' ', '')
	
	# 线索转化为客户后，不修改线索状态为 Converted
	def update_lead_status(self):
		"""If Customer created from Lead, update lead status to "Converted"
		update Customer link in Quotation, Opportunity"""
		if self.lead_name:
			# frappe.db.set_value("Lead", self.lead_name, "status", "Converted")
			pass

	def before_save(self):
		old = self.get_doc_before_save()
		# 同一条线索只能创建一个客户
		if self.has_value_changed("lead_name") and frappe.db.exists("Customer", {"lead_name": self.lead_name}):
			frappe.throw("当前线索已经创建过客户，不可重复创建！")

		# 如果公司类型的客户 修改了客户名或者个人客户修改为公司客户则必须要通过企查查查询
		if (self.has_value_changed("customer_name") or self.has_value_changed("customer_type")) and self.customer_type == 'Company':
			config = frappe.get_single("QCC Settings")
			q = qcc.Qcc(app_key=config.app_key, secret_key=config.secret_key)
			code, result = q.name_search(self.customer_name)
			if code != 200:
				frappe.throw(result, title="企查查查询失败")
			else:
				if self.customer_name not in result:
					frappe.throw(result, title="请选择以下结果中的一个", as_list=True)

		# 个人->公司，公司 x->个人
		if old and old.customer_type == 'Company' and self.customer_type == "Individual":
			frappe.throw("公司客户不可转化为个人客户！")
		
		# 如果客户关联的线索发生变化，同时修改客户联系方式子表
		if self.has_value_changed("lead_name"):

			lead = frappe.get_doc("Lead", self.lead_name)
			if old:
				if len(self.custom_customer_contacts) == 0:
					self.add_customer_contact_item(lead)
				else:
					for item in self.custom_customer_contacts:
						if item.source == 'Lead':
							item.contact_name = lead.first_name
							item.mobile = lead.mobile_no
							item.wechat = lead.custom_wechat
							item.phone = lead.phone
							break
					else:
						self.add_customer_contact_item(lead)
			else:
				self.add_customer_contact_item(lead)
		

	def add_customer_contact_item(self, lead):
		self.append("custom_customer_contacts", {
			"contact_name": lead.first_name,
			"mobile": lead.mobile_no,
			"wechat": lead.custom_wechat,
			"phone": lead.phone,
			"source": "Lead",
			"lead": lead.name
		})