import frappe

from erpnext_china.hrms_china.custom_form_script.employee.employee import get_employee_tree


def has_query_permission(user):

	if frappe.db.get_value('Has Role',{'parent':user,'role':['in',['System Manager','仓库管理']]}):
		# 如果角色包含管理员，则看到全量
		conditions = ''
	elif frappe.db.get_value('Has Role',{'parent':user,'role':['in',['仓库']]}):
		'''
		如果权限是仓库，则可以看到特定仓库的物料
		'''
		# 用户和用户下级
		users = get_employee_tree(parent=user)
		users.append(user)
		users_str = str(tuple(users)).replace(',)',')')

		conditions = f'''
			name in 
			(select distinct parent from `tabStock Entry Detail`
				where (
					s_warehouse in 
						(
							select distinct parent from `tabWarehouse User`
							where warehouse_user in ('yueyanling@zhushigroup.cn')
						)
					)
					or 
					(
					t_warehouse in 
						(
							select distinct parent from `tabWarehouse User`
							where warehouse_user in {users_str}
						)
					)
			)
		'''
	return conditions