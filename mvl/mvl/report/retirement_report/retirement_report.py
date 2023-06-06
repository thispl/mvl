# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from frappe.utils import formatdate


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		_("Employee") + ":Data/:200",
		_("Employee Name") + ":Data/:200",
		_("Department") + ":Link/Department:200",
		_("Designation") + ":Link/Designation :200",
		_("Date Of Retirement") + ":Date/:100",
	]
	return columns

def get_data(filters):
	data = []
	# sa = frappe.db.get_all("Sales Invoice",{"Customer":filters.customer,"posting_date":('between',(filters.from_date,filters.to_date))},['*'])
	sa = frappe.db.sql(""" select * from `tabEmployee` where status = "Active" and  date_of_retirement between '%s' and '%s'  """%(filters.from_date,filters.to_date),as_dict=True)
	frappe.errprint(sa)
	for i in sa:
		frappe.errprint(i.employee)
		sb = frappe.get_doc('Employee', i.name)
		print(sb)
		row = [i.name,i.employee_name,i.department,i.designation,i.date_of_retirement]
		data.append(row)
	return data
