# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from erpnext.selling.doctype.customer.customer import Customer

class CustomCustomer(Customer):
    
    def validate(self):
        super().validate()
        self.clean_fields()

    def clean_fields(self):
        if self.customer_name:
            self.customer_name = str(self.customer_name).replace(' ', '')