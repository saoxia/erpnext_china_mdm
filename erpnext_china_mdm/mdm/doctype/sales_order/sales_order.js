frappe.ui.form.on('Sales Order', {
	onload(frm) {
		// 删除付款申请按钮
		frm.remove_custom_button(__('Payment Request'), __('Create'));
		// 删除材料申请按钮
		frm.remove_custom_button(__('Material Request'), __('Create'));	
		// 删除采购订单按钮
		frm.remove_custom_button(__('Purchase Order'), __('Create'));	
		}
	})