# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe

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
		_("Index") + ":Data/:50",
		_("Employee") + ":Data/:200",
		_("Employee Name") + ":Data/:200",
		_("UAN") + ":Link/ESI Location:200",
		_("Gross") + ":Float/:200",
		_("PF 13%") + ":Float/:200",
		_("PF 12%") + ":Float/:200",
		_("Days") + ":Int/:200",
		_("NCP") + ":Int/:200",
		_("Total") + ":Float/:200",


	]
	return columns


def get_data(filters):
	data = []
	sp = frappe.get_all("Employee",{"status":"Active"},["*"])
	for emp in sp:
		sal = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["gross_pay"]) or " "
		sal_present = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["payment_days"]) or " "
		sal_absent = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["absent_days"]) or " "
		sal_name = frappe.db.get_value("Salary Slip", {"employee": emp.name,"start_date":filters.from_date,"end_date":filters.to_date}, ["name"]) or " "
		esi = int(frappe.get_value('Salary Detail',{'salary_component':"Earned Provident Fund",'parent':sal_name},["amount"]) or 0)
		ded_esi = int(frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':sal_name},["amount"]) or 0)
		tot = esi + ded_esi
		if esi > 0:
			row = [1,emp.name,emp.employee_name,emp.uan_number,sal, esi ,ded_esi,sal_present,sal_absent,tot]
			data.append(row)
	return data
