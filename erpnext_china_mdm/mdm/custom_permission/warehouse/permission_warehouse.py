import frappe

from erpnext_china.hrms_china.custom_form_script.employee.employee import get_employee_tree


def get_descendants(name, nodes):
    descendants = []
    for node in nodes:
        if node['parent_warehouse'] == name:
            descendants.append(node)
            descendants.extend(get_descendants(node['name'], nodes))
    return descendants

def get_user_all_warehouses(users):
	user_warehouses = frappe.get_all("Warehouse User", filters={"warehouse_user": ["in", users]}, pluck='parent')
	warehouses = frappe.get_all("Warehouse", filters={
		"name": ["in", list(set(user_warehouses))]
	}, fields=["name", "parent_warehouse"])
	all_warehouses = frappe.get_all("Warehouse", fields=["name", "parent_warehouse"])
	finall_warehouses = []
	for w in warehouses:
		finall_warehouses += get_descendants(w['name'], all_warehouses) + [w]
	return finall_warehouses

def has_query_permission(user):

	if frappe.db.get_value('Has Role',{'parent':user,'role':['in',['System Manager','仓库管理']]}):
		# 如果角色包含管理员，则看到全量
		conditions = ''
	elif frappe.db.get_value('Has Role',{'parent':user,'role':['in',['仓库']]}):
		'''
		如果权限是仓库，则可以看到自己的仓库和仓库的下级
		上级用户可以看到下级用户的仓库
		'''
		# 用户和用户下级
		users = get_employee_tree(parent=user)
		users.append(user)
		# 找到用户及下级所有的仓库
		warehouses = get_user_all_warehouses(users)
		warehouses = tuple(set([w['name'] for w in warehouses]))
		string = str(warehouses).replace(',)', ')')
		conditions = """('')"""
		if len(warehouses) > 0:
			conditions = f"""
				name in {string}
			"""
	return conditions

def has_permission(doc, user, permission_type=None):
	if frappe.db.get_value('Has Role',{'parent':user,'role':['in',['System Manager','仓库管理']]}):
		# 如果角色包含管理员，则看到全量
		return True
	elif frappe.db.get_value('Has Role',{'parent':user,'role':['in',['仓库']]}):
		users = get_employee_tree(parent=user)
		users.append(user)
		warehouses = get_user_all_warehouses(users)
		if doc.name in list(set([w['name'] for w in warehouses])):
			return True
	return False