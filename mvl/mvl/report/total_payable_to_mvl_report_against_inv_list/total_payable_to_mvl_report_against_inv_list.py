# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from frappe.utils.data import add_days, today
from frappe.utils import  formatdate
from frappe.utils import format_datetime

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		_("Invoice Name") + ":Data/:800",
		_("Total Payable to MVL") + ":Currency/:250",
	]
	return columns

def get_data(filters):
	data = []
	invoice = frappe.db.sql("""select inv_name from `tabInvoice Name` """, as_dict=True)
	for iv in invoice:
		salary_slip = frappe.db.sql("""select sum(total_payable_to_mvl) as amount  from `tabSalary Slip` where invoice_name='%s' and start_date ='%s' and end_date ='%s' """%(iv.inv_name,filters.from_date,filters.end_date),as_dict=1)[0] or 0.0
		att_ot_reg = frappe.db.sql("""select sum(transport_allowance) as amount  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance='%s' and start_date ='%s' and end_date ='%s' and docstatus = 1 """%(iv.inv_name,filters.from_date,filters.end_date),as_dict=1)[0] or 0.0
		trans = 0
		if type(att_ot_reg['amount']) == float:
			trans = round(att_ot_reg['amount'] * 1.1)
			# frappe.errprint(round(att_ot_reg['amount'] * 1.1))
		else:
			trans = 0
			# frappe.errprint(0)
		# frappe.errprint(type(att_ot_reg['amount']))
		row1 = [iv.inv_name, (salary_slip['amount'] or 0 + trans or 0)]
		data.append(row1)
	for i in invoice:
		if i.inv_name == "Renowned Engineers Private Limited,,Manpower Supply Service":
			lun_all = frappe.db.sql("""select sum(lunch_allowance) as amount  from `tabAttendance and OT Register` where invoice_name='%s' and start_date ='%s' and end_date ='%s' and  docstatus = 1 """%(i.inv_name,filters.from_date,filters.end_date),as_dict=1)[0] or 0.0
			lun = 0
			if type(lun_all['amount']) == float:
				lun = round(lun_all['amount'] * 1.1)
				# frappe.errprint(round(lun_all['amount'] * 1.1))
			else:
				lun = 0
				# frappe.errprint(0)
			# frappe.errprint(type(lun_all['amount']))
			row1 = ["Renowned Engineers Private Limited,,Manpower Supply Service Lunch",lun or 0]
			data.append(row1)
	return data