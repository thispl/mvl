# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from frappe.utils import formatdate
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
		_("ESI ID") + ":Link/ESI Location:200",
		_("Gross Pay") + ":Float/:200",
		_("ESI @ 0.75% ") + ":Float/:200",
		_("ESI @ 3.25% ") + ":Float/:200",
		_("Total") + ":Float/:200"
	]
	return columns

def get_data(filters):
	data = []
	if filters.esi_id:
		sp = frappe.get_all("Employee",{"esi_id":filters.esi_id},["*"])
		for emp in sp:
			sal = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["gross_pay"]) or " "
			# frappe.errprint(sal)
			sal_name = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["name"]) or " "
			# frappe.errprint(sal_name)
			esi = int(frappe.get_value('Salary Detail',{'salary_component':"Employee State Insurance",'parent':sal_name},["amount"]) or 0)
			ded_esi = int(frappe.get_value('Salary Detail',{'salary_component':"Deduction Employee State Insurance",'parent':sal_name},["amount"]) or 0)
			tot = esi + ded_esi
			frappe.errprint(esi)
			frappe.errprint(ded_esi)
			row = [emp.name,emp.employee_name,emp.esi_number,sal, esi ,ded_esi,tot]
			data.append(row)
	return data
		
