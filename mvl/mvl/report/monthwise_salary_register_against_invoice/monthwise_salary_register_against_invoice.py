# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from frappe.utils.data import add_days, today
from frappe.utils import  formatdate,get_last_day, get_first_day, add_days
from frappe.utils import format_datetime
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


def execute(filters=None):
	if not filters:
		filters = {}
	currency = None
	if filters.get("currency"):
		currency = filters.get("currency")
	company_currency = erpnext.get_company_currency(filters.get("company"))
	salary_slips = get_salary_slips(filters, company_currency)
	if not salary_slips:
		return [], []

	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
	ss_ded_map = get_ss_ded_map(salary_slips, currency, company_currency)
	doj_map = get_employee_doj_map()

	data = []
	for ss in salary_slips:
		row = [1,
			ss.employee,
			ss.employee_name,
			frappe.db.get_value('Employee',ss.employee,'father_or_spouse_name') or "",
			frappe.db.get_value('Employee',ss.employee,'relationship') or "",
			formatdate(frappe.db.get_value('Employee',ss.employee,'date_of_birth') or ""),
			frappe.db.get_value('Employee',ss.employee,'department') or "",
			frappe.db.get_value('Employee',ss.employee,'designation') or "",
			ss.principal_employer,
			frappe.db.get_value('Employee',ss.employee,'unit') or "",
			formatdate(frappe.db.get_value('Employee',ss.employee,'date_of_joining') or ""),
			frappe.db.get_value('Employee',ss.employee,'uan_number') or "-",
			frappe.db.get_value('Employee',ss.employee,'esi_number') or "-",
			frappe.db.get_value('Employee',ss.employee,'bank_ac_no') or "-",
			frappe.db.get_value('Employee',ss.employee,'bank_name') or "-",
			frappe.db.get_value('Employee',ss.employee,'ifsc_code') or "-",
			ss.payment_days,
			ss.absent_days,
			frappe.db.get_value('Employee',ss.employee,'per_day_wage') or 0,
			frappe.db.get_value('Employee',ss.employee,'basic') or 0,
			frappe.db.get_value('Employee',ss.employee,'dearness_allowance') or 0,
			frappe.db.get_value('Employee',ss.employee,'house_rent_allowance') or 0,
			frappe.db.get_value('Employee',ss.employee,'washing_allowance') or 0,
			frappe.db.get_value('Employee',ss.employee,'conveyance_allowance') or 0,
			frappe.db.get_value('Employee',ss.employee,'medical_allowance') or 0,
			frappe.db.get_value('Employee',ss.employee,'special_allowance') or 0,
			frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['other_allowance']) or 0,
			(int(frappe.db.get_value('Employee',ss.employee,'basic') or 0)+
			int(frappe.db.get_value('Employee',ss.employee,'dearness_allowance') or 0)+
			int(frappe.db.get_value('Employee',ss.employee,'house_rent_allowance') or 0)+
			int(frappe.db.get_value('Employee',ss.employee,'washing_allowance') or 0)+
			int(frappe.db.get_value('Employee',ss.employee,'conveyance_allowance') or 0)+
			int(frappe.db.get_value('Employee',ss.employee,'medical_allowance') or 0)+
			int(frappe.db.get_value('Employee',ss.employee,'special_allowance') or 0)) or 0,
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Basic",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Dearness Allowance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned House Rent Allowance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Washing Allowance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Conveyance Allowance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Medical Allowance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Special Allowance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Other Allowance",'parent':ss.name},["amount"]) or 0),
			ss.overtime_hours or 0,
			int(frappe.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':ss.name},["amount"]) or 0),
			ss.gross_pay,
			int(frappe.get_value('Salary Detail',{'salary_component':"Earned Provident Fund",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'abbr':"ESI",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Attendance Bonus",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Insurance",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Gratuity",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Uniform",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Leave Encashment",'parent':ss.name},["amount"]) or 0),
			ss.sub_total or 0,
			int(frappe.get_value('Salary Detail',{'salary_component':"Service Charges",'parent':ss.name},["amount"]) or 0),
			ss.total_payable_to_mvl or 0,
			int(frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'abbr':"D_ESI",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"L/w Fund",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Professional Tax",'parent':ss.name},["amount"]) or 0),
			ss.total_deduction or 0,
			ss.rounded_total,
			ss.epf_wages or 0,
			ss.esi_wages or 0,
			((int(ss.gross_pay)) - int(frappe.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':ss.name},["amount"]) or 0)),
			frappe.db.get_value('Employee',ss.employee,'invoice_name') or "",
			frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['transport_allowance']) or 0,
			frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['lunch_allowance']) or 0,
			int(frappe.get_value('Salary Detail',{'salary_component':"Salary Advance Detection",'parent':ss.name},["amount"]) or 0),
			int(frappe.get_value('Salary Detail',{'salary_component':"Stipend",'parent':ss.name},["amount"]) or 0)
			]
		data.append(row)

	return columns, data


def get_columns(salary_slips):
	columns = [
		_("Index") + ":Data/:50",
		_("Employee") + ":Employee:120",
		_("Employee Name") + "::200",
		_("Father's / Spouse's Name") + "::200",
		_("Relationship") + "::100",
		_("Date of Birth") + "::120",
		_("Department") + "::100",
		_("Designation") + "::100",
		_("Principal Employer") + "::100",
		_("Unit") + "::60",
		_("Date of Joining") + "::120",
		_("UAN Number") + "::100",
		_("ESI Number") + "::100",
		_("Bank A/c Number") + "::120",
		_("Bank Name") + "::120",
		_("IFS Code") + "::120",
		_("Days Atteded") + "::120",
		_("NCP") + "::120",
		_("Per Day Basic") + ":Data:120",
		_("Fixed Basic") + ":Data:100",
		_("Fixed Dearness Allowance") + ":Data:200",
		_("Fixed House Rent Allowance") + ":Data:200",
		_("Fixed Washing Allowance") + ":Data:200",
		_("Fixed Conveyance Allowance") + ":Data:200",
		_("Fixed Medical Allowance") + ":Data:200",
		_("Fixed Special Allowance") + ":Data:200",
		_("Fixed Other Allowance") + ":Data:200",
		_("Total") + ":Data:150",
		_("Earned Basic") + ":Data:100",
		_("Earned Dearness Allowance") + ":Data:200",
		_("Earned House Rent Allowance") + ":Data:200",
		_("Earned Washing Allowance") + ":Data:200",
		_("Earned Conveyance Allowance") + ":Data:200",
		_("Earned Medical Allowance") + ":Data:200",
		_("Earned Special Allowance") + ":Data:200",
		_("Earned Other Allowance") + ":Data:200",
		_("OT Hours") + ":Data:120",
		_("OT Amount") + ":Data:120",
		_("E Gross") + ":Currency:150",
		_("Earned Provident Fund") + ":Data:150",
		_("Earned Employee State Insurence") + ":Data:150",
		_("Attendance Bonus") + ":Data:150",
		_("Insurance") + ":Data:150",
		_("Gratuity") + ":Data:150",
		_("Uniform") + ":Data:150",
		_("CL/EL") + ":Data:150",
		_("Sub Total") + ":Data:150",
		_("Service Charges") + ":Data:150",
		_("Total payable to MVL") + ":Data:150",
		_("Provident Fund") + ":Data:150",
		_("Employee State Insurence") + ":Data:150",
		_("L/w Fund") + ":Data:150",
		_("Professional Tax") + ":Data:150",
		_("Total Deductions") + ":Data:150",
		_("Net Pay") + ":Data:150",
		_("EPF Wages") + ":Data:150",
		_("ESI wages") + ":Data:150",
		_("Gross Wages") + ":Data:150",
		_("Invoice Name") + "::200",
		_("Travel Allowance") + ":Data:200",
		_("Lunch Allowance") + ":Data:200",
		_("Salary Advance Detection") + ":Data:150",
		_("Stipned") + ":Data:150"
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql(
		"""select distinct sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)"""
		% (", ".join(["%s"] * len(salary_slips))),
		tuple([d.name for d in salary_slips]),
		as_dict=1,
	):
		salary_components[_(component.type)].append(component.salary_component)

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters, company_currency):
	filters.update({"from_date": filters.get("from_date"), 
	"to_date": filters.get("to_date"),
	"invoice_name":filters.get("invoice_name")
	})
	conditions, filters = get_conditions(filters, company_currency)
	salary_slips = frappe.db.sql(
		"""select * from `tabSalary Slip` where docstatus != 2 and %s order by employee"""% conditions,
		filters,
		as_dict=1,
	)
	return salary_slips or []


def get_conditions(filters, company_currency):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}
	if filters.get("docstatus"):
		conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])
	if filters.get("from_date"):
		conditions += " and start_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " and end_date <= %(to_date)s"
	if filters.get("company"):
		conditions += " and company = %(company)s"
	if filters.get("invoice_name"):
		conditions += " and invoice_name = %(invoice_name)s"
	if filters.get("invoice_name_for_travel_allowance"):
		conditions += " and invoice_name_for_travel_allowance = %(invoice_name_for_travel_allowance)s"
	if filters.get("currency") and filters.get("currency") != company_currency:
		conditions += " and currency = %(currency)s"
	return conditions, filters

def get_employee_doj_map():
	return frappe._dict(frappe.db.sql("""SELECT employee,date_of_joining FROM `tabEmployee` """))

def get_ss_earning_map(salary_slips, currency, company_currency):
	ss_earnings = frappe.db.sql(
		"""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)"""
		% (", ".join(["%s"] * len(salary_slips))),
		tuple([d.name for d in salary_slips]),
		as_dict=1,
	)
	
	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_earning_map[d.parent][d.salary_component] += flt(d.amount) * flt(
				d.exchange_rate if d.exchange_rate else 1
			)
		else:
			ss_earning_map[d.parent][d.salary_component] += flt(d.amount)
	return ss_earning_map


def get_ss_ded_map(salary_slips, currency, company_currency):
	ss_deductions = frappe.db.sql(
		"""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)"""
		% (", ".join(["%s"] * len(salary_slips))),
		tuple([d.name for d in salary_slips]),
		as_dict=1,
	)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_ded_map[d.parent][d.salary_component] += flt(d.amount) * flt(
				d.exchange_rate if d.exchange_rate else 1
			)
		else:
			ss_ded_map[d.parent][d.salary_component] += flt(d.amount)
	return ss_ded_map


@frappe.whitelist()
def get_to_date(from_date):
	return get_last_day(from_date)