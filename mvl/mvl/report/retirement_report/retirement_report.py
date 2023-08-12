# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		("Employee") + ":Link/Employee:200",
		("Employee Name") + ":Data/:200",
		("Department") + ":Link/Department:200",
		("Designation") + ":Link/Designation:200",
		("Date Of Retirement") + ":Date/:100",
	]
	return columns

def get_data(filters):
	data = []
	sa = frappe.db.sql(""" select * from `tabEmployee` where status = "Active" and  date_of_retirement between '%s' and '%s'  """%(filters.from_date,filters.to_date),as_dict=True)
	# frappe.errprint(sa)
	for i in sa:
		frappe.errprint(i.employee)
		row = [i.name,i.employee_name,i.department,i.designation,i.date_of_retirement]
		data.append(row)
	return data
