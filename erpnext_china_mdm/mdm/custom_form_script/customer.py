# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

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
		if not old and frappe.db.exists("Customer", {"lead_name": self.lead_name}):
			frappe.throw("当前线索已经创建过客户，不可重复创建！")

		# 如果公司类型的客户  新增或者是修改客户名称时，通过企查查校验名称
		if (not old or self.has_value_changed("customer_name")) and self.customer_type == 'Company':
			config = frappe.get_single("QCC Settings")
			q = qcc.Qcc(app_key=config.app_key, secret_key=config.secret_key, url=config.qcc_api_url)
			results = q.request(self.customer_name)
			if results:
				frappe.throw(results)
		
        # 个人->公司，公司 x->个人
		if old and old.customer_type == 'Company' and self.customer_type == "Individual":
			frappe.throw("公司客户不可转化为个人客户！")
		
		# 如果客户关联的线索发生变化，同时修改客户联系方式子表
		if self.has_value_changed("lead_name"):

			lead = frappe.get_doc("Lead", self.lead_name)
			if old:
				old_lead = frappe.get_doc("Lead", old.lead_name)
				for item in self.custom_customer_contacts:
					if item.mobile == old_lead.mobile_no and item.wechat == old_lead.custom_wechat and item.phone == old_lead.phone:
						item.contact_name = lead.first_name
						item.mobile = lead.mobile_no
						item.wechat = lead.custom_wechat
						item.phone = lead.phone
						break
			else:
				self.append("custom_customer_contacts", {
					"contact_name": lead.first_name,
					"mobile": lead.mobile_no,
					"wechat": lead.custom_wechat,
					"phone": lead.phone
				})
			