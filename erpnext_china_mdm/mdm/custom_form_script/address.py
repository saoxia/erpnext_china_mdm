# Copyright (c) 2015, Frappe Technologies and contributors
# License: MIT. See LICENSE
import frappe

from frappe.contacts.doctype.address.address import Address

class CustomAddress(Address):
	
	def before_save(self):

		if self.has_value_changed('phone') and self.phone:
			self.check_address_contact()
	
	# 填写的联系方式必须是 客户 联系方式子表中的一个或者是没有录入过的
	def check_address_contact(self):
		if self.phone:
			self.phone = self.phone.replace(" ", "")
			links = [link.link_name for link in self.links if link.link_doctype=='Customer']
			contact_infos = frappe.db.get_all("Customer Contact Item", filters=[["parent", 'in', links]], pluck='contact_info')
			# 如果是当前关联的客户中已经存在的联系方式
			if contact_infos and self.phone in contact_infos:
				return
			
			# 如果是在所有客户中都没有录入过的
			has_contact = frappe.db.get_value("Customer Contact Item", filters={"contact_info": self.phone})
			if not has_contact:
				# for link in self.links:
				# 	if link.link_doctype == 'Customer':
				# 		customer = frappe.get_doc("Customer", link.link_name)
				# 		customer.append("custom_customer_contacts", {
				# 			"contact_name": self.contact,
				# 			"contact_info": self.phone,
				# 			"source": "Other",
				# 		})
				# 		customer.save(ignore_permissions=True)
				return
			else:
			# 如果是在其他客户中已经存在
				frappe.throw("当前联系方式（电话）已在其他客户中存在！")