// Copyright (c) 2024, Fisher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sensitive DocType', {
	update_property_setter(frm){
		frm.call('update_property_setter', null, 
			(r) => {refreshfield('fields')}
		);			
	},
	update_custom_perm(frm){
		frm.call('update_custom_perm', null, null);			
	}
});
