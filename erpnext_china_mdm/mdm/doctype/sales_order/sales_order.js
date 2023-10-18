frappe.ui.form.on('Sales Order', {
	refresh(frm) {
		// 删除付款申请按钮
		frm.remove_custom_button(__('Payment Request'), __('Create'));	
		}
	})
