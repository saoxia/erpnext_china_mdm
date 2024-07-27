import frappe

from erpnext_china.hrms_china.custom_form_script.employee.employee import get_employee_tree

def has_query_permission(user):
	if frappe.db.get_value('Has Role',{'parent':user,'role':['in',['System Manager','网络推广管理']]}):
		# 如果角色包含管理员，则看到全量
		conditions = ''
	else:
		# 其他情况则只能看到自己,上级可以看到下级
		users = get_employee_tree(parent=user)
		users.append(user)
		users_str = str(tuple(users)).replace(',)',')')
		conditions = f"(tabLead.owner in {users_str}) or (lead_owner in {users_str}) or (custom_sea = '公海')" 
		if len(frappe.get_all('Has Role', {'parent':user,'role': ['in', ['网络推广', '销售']]})) > 0:
			# conditions = f"(custom_sea='公海') or (owner in {users_str}) or (lead_owner in {users_str})" 
			conditions = f"((tabLead.owner in {users_str}) or (lead_owner in {users_str}) or (custom_sea = '公海')) and (tabLead.status != 'Do Not Contact')" 
	return conditions

def has_permission(doc, user, permission_type=None):
	if frappe.db.get_value('Has Role',{'parent':user,'role':['in',['System Manager','网络推广管理']]}):
		# 如果角色包含管理员，则看到全量
		return True
	else:
		# 其他情况则只能看到自己,上级可以看到下级
		users = get_employee_tree(parent=user)
		users.append(user)
		# if (doc.owner in users) or (doc.lead_owner in users) or (doc.custom_sea == "公海" and len(frappe.get_all('Has Role', {'parent':user,'role': ['in', ['网络推广', '销售']]})) > 0):
		if (doc.owner in users) or (doc.lead_owner in users) or (doc.custom_sea == '公海'):
			return True
		else:
			return False