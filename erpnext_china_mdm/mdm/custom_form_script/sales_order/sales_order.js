frappe.ui.form.on('Sales Order', {
	onload(frm) {
		// 删除按钮
		frm.remove_custom_button(__('Purchase Order'), __('Create'));
		frm.remove_custom_button(__('Work Order'), __('Create'));
		frm.remove_custom_button(__('Material Request'), __('Create'));
		frm.remove_custom_button(__('Request for Raw Materials'), __('Create'));
		frm.remove_custom_button(__('Purchase Order'), __('Create'));
		frm.remove_custom_button(__('Payment Request'), __('Create'));
		frm.remove_custom_button(__('Maintenance Visit'), __('Create'));
		frm.remove_custom_button(__('Maintenance Schedule'), __('Create'));
		}
	})