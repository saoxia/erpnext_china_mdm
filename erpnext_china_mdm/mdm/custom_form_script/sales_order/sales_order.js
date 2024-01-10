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


		// 销售订单选择物料时，只选择已经定义的UOM
		frm.fields_dict['items'].grid.get_field('uom').get_query = function(doc, cdt, cdn){
			var row = locals[cdt][cdn];
			return {
				query:"erpnext.accounts.doctype.pricing_rule.pricing_rule.get_item_uoms",
				filters: {'value':row.item_code, apply_on:"Item Code"},
			}
		};
	}})
