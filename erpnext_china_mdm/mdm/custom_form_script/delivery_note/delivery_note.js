// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on('Sales Order', {
	onload(frm) {
		// 删除按钮
		frm.remove_custom_button(__('Delivery Trip'), __('Create'));
		frm.remove_custom_button(__('Installation Note'), __('Create'));
		}
	})