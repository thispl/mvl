# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_first_day,
	get_link_to_form,
	getdate,
	money_in_words,
	rounded,
)

class ArrearSalaryUpdation(Document):
	pass
	
@frappe.whitelist()
def get_tott_ncp(from_date,to_date,invoice_name,payment_days,employee):
	frappe.errprint("HI")
	tot = date_diff(to_date, from_date) + 1
	ncp = float(tot) - float(payment_days)
	ad = frappe.db.sql("""select name from `tabSalary Structure Assignment` where employee = '%s' and docstatus = 1 ORDER BY from_date DESC LIMIT 1  """%(employee),as_dict=True)[0]
	if not ad:
		frappe.msgprint("Please assign a Salary Structure Assignment")
	else:
		# frappe.errprint("HI")
		# frappe.errprint(ad.name)
		ss = frappe.db.get_value("Salary Structure Assignment",{'name':ad.name},['salary_structure'])
		# frappe.errprint(ss)
		
	return [ncp,tot]
