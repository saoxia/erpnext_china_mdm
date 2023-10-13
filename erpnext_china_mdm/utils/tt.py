import frappe

@frappe.whitelist()
def get_employee_tree(parent=None, 
                    pluck='email',
                    orient='list',
                    levle=None,
                    is_root=None,
                    use_cache=False):
    '''
    parent: default None
        用户唯一标识的类型，可以输入str或dict
        key: email|userid|username
        value: 唯一标识的值

    pluck: default ['email'] 返回的字段名
        email|userid|username

    orient: list|dict , 是否返回树状结构

    levle: all|int ,返回多少层级的信息

    is_root: False
    '''
    if is_root:
        employee = 'HR-EMP-00002'
    # 递归函数来获取下级employee
    def get_subordinates(employee):
        subordinates = []

        filters = {'reports_to': employee,
                'status': 'Active'}
        employees = frappe.get_all('Employee',filters=filters,fields=['employee'],as_list=True)
        employees = [item[0] for item in employees]
        for i in employees:
            subordinates.append(i)
            subordinates.append(get_subordinates(i))
        return subordinates

    return get_subordinates(employee)

