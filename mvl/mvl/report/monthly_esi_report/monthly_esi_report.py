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
import math


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data
		
def get_columns(filters):
	columns = [
		_("Index") + ":Data/:50",
		_("Employee") + ":Data/:200",
		_("Employee Name") + ":Data/:200",
		_("Payment Days") + ":Data/:200",
		_("ESI Number") + ":Link/ESI Location:200",
		_("Gross Pay") + ":Currency/:200",
		_("ESI @ 0.75% ") + ":Currency/:200",
		_("ESI @ 3.25% ") + ":Currency/:200",
		_("Total") + ":Currency/:200",
		_("ESI ID") + ":Link/ESI Location:200",
	]
	return columns

def get_data(filters):
	data = []
	if filters.esi_id:
		sp = frappe.get_all("Employee",{'Status':'Active',"esi_id":filters.esi_id},["*"])
	else:
		sp = frappe.get_all("Employee",{'Status':'Active',"esi_id":['!=','']},["*"])
	for emp in sp:
		frappe.errprint(emp.name) 
		gp = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["gross_pay"]) or 0
		pd = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["payment_days"]) or 0
		sal_name = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["name"]) or " "
		wa = frappe.get_value('Salary Detail',{'salary_component':"Earned Washing Allowance",'parent':sal_name},["amount"]) or 0
		esi = int(frappe.get_value('Salary Detail',{'salary_component':"Employee State Insurance",'parent':sal_name},["amount"]) or 0)
		ded_esi = int(frappe.get_value('Salary Detail',{'salary_component':"Deduction Employee State Insurance",'parent':sal_name},["amount"]) or 0)
		tot = esi + ded_esi 
		sal = gp - wa
		frappe.errprint(type(gp)) 
		frappe.errprint(type(wa)) 
		if esi != 0: 
			row = [1,emp.name,emp.employee_name,math.ceil(pd),emp.esi_number,sal,ded_esi, esi ,tot,emp.esi_id]
			data.append(row) 
	return data
		
