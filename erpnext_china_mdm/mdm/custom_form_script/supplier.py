
import frappe
from erpnext.buying.doctype.supplier.supplier import Supplier

from erpnext_china_mdm.utils import qcc

class CustomSupplier(Supplier):
	
	def validate(self):
		super().validate()
		self.qcc_verify()

	def qcc_verify(self):
		# 如果公司类型的客户 修改了客户名或者个人客户修改为公司客户则必须要通过企查查查询
		if (self.has_value_changed("supplier_name") or self.has_value_changed("supplier_type")) and self.supplier_type == 'Company':
			config = frappe.get_single("QCC Settings")
			q = qcc.QccApiNameSearch(app_key=config.app_key, secret_key=config.secret_key)
			result = q.name_search(self.supplier_name)
			if result.code != 200:
				frappe.throw(result, title="企查查查询失败")
			else:
				if self.supplier_name not in result.data:
					frappe.throw(result.data, title="请选择以下结果中的一个", as_list=True)