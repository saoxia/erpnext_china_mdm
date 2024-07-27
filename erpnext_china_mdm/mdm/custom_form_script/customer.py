# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from erpnext.selling.doctype.customer.customer import Customer

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