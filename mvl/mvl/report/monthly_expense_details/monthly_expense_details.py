# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns , data
	

def get_columns():
	columns =[
		_("Index") + ":Data/:50",
		_("Bill No.") + ":Link/Monthly Invoice:200",
		_("Name of the Unit") + "::200",
		_("Amount") + "::120",
		_("Expense") + "::100",
		_("Profit") + "::100"
	]
	return columns

def get_data(filters):
	data=[]
	invoice = frappe.db.sql("""select * from `tabInvoice Name` where active = 1 """, as_dict=1)
	for i in invoice :
		bill = frappe.db.get_value("Monthly Invoice",{'invoice_name':i.name,'from_date':filters.start_date,"to_date":filters.end_date},['name'])
		input_string = str(bill)
		last_four_digits = input_string[-5:]
		frappe.errprint(i.travel_allowance)
		if i.travel_allowance == 0 :
			salary_slip = frappe.db.sql("""select sum(total_payable_to_mvl) as amount  from `tabSalary Slip` where invoice_name ='%s' and start_date = '%s' and end_date ='%s' """%(i.inv_name,filters.start_date,filters.end_date),as_dict= True)
			amount = salary_slip[0]['amount'] if salary_slip and salary_slip[0].get('amount') is not None else 0
			salary_slip1 = frappe.db.sql("""select sum(sub_total) as amount  from `tabSalary Slip` where invoice_name ='%s' and start_date = '%s' and end_date ='%s' """%(i.inv_name,filters.start_date,filters.end_date),as_dict= True)
			expense = salary_slip1[0]['amount'] if salary_slip1 and salary_slip1[0].get('amount') is not None else 0
			frappe.errprint(amount)
			frappe.errprint(amount)
			row=[1,
				last_four_digits,
				i.name,
				amount,
				expense,
				(amount-expense)
				]
			data.append(row)
		else:
			att = frappe.db.sql("""select sum(transport_allowance) as amount  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' """%(i.inv_name,filters.start_date,filters.end_date),as_dict= True)
			tr = att[0]['amount'] if att and att[0].get('amount') is not None else 0
			sc = tr/10
			row=[1,
				last_four_digits,
				i.name,
				tr + sc,
				sc,
				tr - sc
				]
			data.append(row)
	return data


