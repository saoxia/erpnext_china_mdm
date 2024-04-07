# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import __version__ as frappe_version


@frappe.whitelist()
def get_data_for_custom_field_wrapper(doctype, fieldname=None, field=None):
    from frappe.desk.query_report import get_data_for_custom_field

    dummy_doc = frappe.get_doc({'doctype': doctype})
    try:
        is_frappe_above_v13 = int(frappe_version.split('.')[0]) > 13
        if dummy_doc.has_permlevel_access_to(field or fieldname):
            #14版之后移除了fieldname参数
            if is_frappe_above_v13:
                return get_data_for_custom_field(doctype = doctype, field=field)
            else:
                return get_data_for_custom_field(doctype = doctype, fieldname=fieldname or field, field=field)
        else:
            frappe.msgprint(_('No field permission'))
    except Exception as e:
        frappe.msgprint(f"Add Column for {doctype} {fieldname} with error {str(e)}")        
