import frappe
from erpnext.stock.doctype.item.item import Item

class CustomItem(Item):
    def set_custom_uoms_string(self):
        uoms = self.uoms
        uom_dict = {}
        for idx in uoms:
            uom = idx.as_dict()['uom']
            conversion_factor = idx.as_dict()['conversion_factor']
            uom_dict.update({conversion_factor:uom})
        uom_dict = {key: uom_dict[key] for key in sorted(uom_dict.keys())}

        # 小于0的情况
        s = ''
        last_uom = None
        last_conversion_factor = None
        for conversion_factor,uom in reversed(list(uom_dict.items())):
            if self.stock_uom != uom and conversion_factor < 1:
                if last_uom:
                    conversion_factor_last_conversion_factor = int(last_conversion_factor/conversion_factor)
                    s = f'{conversion_factor_last_conversion_factor}{uom}/{last_uom};{s}'
                else:
                    s = f'{int(1/conversion_factor)}{uom}/{self.stock_uom};{s}'
                last_uom = uom
                last_conversion_factor = conversion_factor
        
        #大于0的情况
        last_uom = None
        last_conversion_factor = None
        for conversion_factor,uom in uom_dict.items():
            if (conversion_factor - int(conversion_factor)) == 0 :
                conversion_factor = int(conversion_factor)
            if self.stock_uom != uom and conversion_factor >= 1:
                if last_uom:
                    if (conversion_factor/last_conversion_factor - int(conversion_factor/last_conversion_factor)) == 0 :
                        conversion_factor_last_conversion_factor = int(conversion_factor/last_conversion_factor)
                    s = f'{s};{conversion_factor_last_conversion_factor}{last_uom}/{uom}'
                else:
                    s = f'{s};{conversion_factor}{self.stock_uom}/{uom}'
            last_uom = uom
            last_conversion_factor = conversion_factor
        self.custom_uoms_string = s.replace(';;',';')
        if len(self.custom_uoms_string) > 1 :
            if self.custom_uoms_string[0] == ';':
                self.custom_uoms_string = self.custom_uoms_string[1:]

    def before_save(self):
        self.set_custom_uoms_string()


@frappe.whitelist()
def get_item_default_warehouse(**kwargs):
	item_code = kwargs.get('item_code')
	company = kwargs.get('company')
	if item_code:
		item = frappe.get_doc('Item', item_code)
		for i in item.item_defaults:
			if i.company == company:
				return i.default_warehouse 

