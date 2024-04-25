from erpnext.stock.doctype.item.item import Item

class CustomItem(Item):
    def set_custom_uoms_string(self):
        uoms = self.uoms
        # 从小到大排序
        uom_dict = {}
        for idx in uoms:
            uom = idx.as_dict()['uom']
            conversion_factor = idx.as_dict()['conversion_factor']
            uom_dict.update({conversion_factor:uom})
        #uom_dict = {key: uom_dict[key] for key in sorted(uom_dict.keys())}
        s = ''
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
        self.custom_uoms_string = s[1:]

    def before_save(self):
        self.set_custom_uoms_string()




