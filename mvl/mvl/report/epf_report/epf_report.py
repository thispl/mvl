# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
import math
from frappe.utils import add_months, cint, flt, getdate, time_diff_in_hours,time_diff_in_seconds
import locale

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		_("Index") + ":Data/:50",
		_("UAN") + ":Data:150",
		_("Name") + ":Data:150",
		_("EPF Gross Wages") + ":Data:150",
		_("PF Wages") + ":Data:150",
		_("PEN Wages") + ":Data:150",
		_("EDLI Wages") + ":Data:150",
		_("EPFO 12%") + ":Data:150",
		_("EPFO 8.33%") + ":Data:150",
		_("EPFO 3.67%") + ":Data:150",
		_("NCP") + ":Data:150",
		_("REFUND") + ":Data:150",
		_("TEXT Data") + ":Data:300",
	]
	return columns

def get_data(filters):
	data = []
	if filters.unit:
		emp = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE status='Active' and unit = '%s' """%(filters.unit),as_dict=True)
	else:
		emp = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE status='Active' """,as_dict=True)
	for i in emp:
		if filters.arrear_slip=='Yes':
			a = frappe.db.get_value("Salary Slip", {'employee': i.name,'start_date': filters.start_date,'end_date': filters.end_date,'docstatus': ['!=', 2],"arrear_slip":['!=',0]},['name'])
		else:
			a = frappe.db.get_value("Salary Slip", {'employee': i.name,'start_date': filters.start_date,'end_date': filters.end_date,'docstatus': ['!=', 2]},['name'])
		if a:
			ss = frappe.get_doc("Salary Slip", a) 
			gp = ss.gross_pay or 0
			if frappe.db.exists("Salary Detail", {'salary_component':"EPF Wages",'parent':a}):
				ncp=ss.absent_days or 0
				epf = ss.epf_wages or 0
				pen_eli = frappe.get_value("Employee",{'name':i.name},['pension_eligibility'])
				if pen_eli == 1:
					if epf < 15000:
						pen = epf
						edli = epf
					else:
						pen = 15000
						edli = 15000
					pfw=(epf * 0.12)
					penw=(pen * 0.0833)
					edliw=pfw-penw
				else:
					pen = 0
					if epf < 15000:
						edli = epf
					else:
						edli = 15000
					pfw=(epf * 0.12)
					penw=0
					edliw=pfw-penw
				row = [1,i.get("uan_number",''),i.get('employee_name', ''),round(gp,0),round(epf,0),round(pen,0),round(edli,0),round(pfw,0),round(penw,0),round(edliw,0),math.ceil(ncp),0,
					str(i.get("uan_number",'')) + str("#~#") +
					str(i.get('employee_name', '')) + str("#~#") +
					str(round(gp)) + str("#~#") +
					str(round(epf)) + str("#~#") +
					str(round(pen)) + str("#~#") +
					str(round(edli)) + str("#~#") +
					str(round(pfw)) + str("#~#") +
					str(round(penw)) + str("#~#") +
					str(round(edliw)) + str("#~#") +
					str(math.ceil(ncp)) + str("#~#") +
					str('0') + str("#~#")
				]
				data.append(row)
	return data
		
