from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry

class CustomStockEntry(StockEntry):
	@property
	def custom_item_uoms_string(self):
		item_code = self.items.item_code
		item_doc = frappe.get_doc('Item', item_code)
		return item_doc.custom_uoms_string