# Copyright (c) 2024, Fisher and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class SensitiveDocType(Document):
	@frappe.whitelist()
	def update_property_setter(self):
		updated, inserted, skipped = 0, 0, 0
		doctype_list = {d.doc_type for d in self.fields}
		docfields = frappe.get_all('DocField', 
				filters = {'parent': ('in', doctype_list )},
				fields= ['parent as dt', 'fieldname']
			)
		docfields.extend(frappe.get_all('Custom Field', 
				filters = {'dt': ('in', doctype_list )},
				fields= ['dt', 'fieldname']
		))
		valid_docfield_set = {(d.dt,d.fieldname) for d in docfields}

		data = frappe.get_all('Property Setter',
				filters = {
					'doc_type': ('in', doctype_list),
					'doctype_or_field': 'DocField',
					'property': 'permlevel'
				},
				fields = ['name', 'doc_type', 'field_name','value']
			)
		property_map = {(d.doc_type, d.field_name):(d.name, d.value) for d in data}
		for row in self.fields:			
			if (row.doc_type, row.field_name) not in valid_docfield_set:
				frappe.msgprint(_("skiped invalid docType {0} field {1}").format(_(row.doc_type), row.field_name))
				skipped += 1
				row.update_status = _('Invalid Field')
				continue
			existing_property = property_map.get((row.doc_type, row.field_name))
			if existing_property:
				if existing_property[1] != self.permlevel:
					frappe.db.set_value('Property Setter',existing_property[0], 'value', self.permlevel)
					row.update_status = _('Updated')
					updated += 1
				else:
					row.update_status = _('No update needed')
			else:
				new_property = frappe.new_doc('Property Setter')
				new_property.update({
					'doc_type': row.doc_type,
					'field_name': row.field_name,
					'doctype_or_field': 'DocField',
					'property': 'permlevel',
					'value': self.permlevel,
					'property_type': 'Check'
				})
				new_property.insert(ignore_permissions=1)
				row.update_status = _('Inserted')
				inserted += 1
		if updated or inserted:
			frappe.msgprint(_('Updated {0} inserted {1} property records').format(updated, inserted))

	@frappe.whitelist()
	def update_custom_perm(self):
		from frappe.permissions import add_permission

		for row in self.whitelist_roles:
			add_permission(self.doc_type, row.role, self.permlevel, ptype = 'write')
		frappe.msgprint(_("Updated custom permissions successfully"))