# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from frappe.utils.data import add_days, today
from frappe.utils import  formatdate,get_last_day, get_first_day, add_days
from frappe.utils import format_datetime

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	data = []
	if filters.unit :
		employees = frappe.db.sql("""select * from `tabEmployee` where status = "Active" and unit = '%s' """%(filters.unit),as_dict = True)
	else:
		employees = frappe.db.sql("""select * from `tabEmployee` where status = "Active" """,as_dict = True)
	for emp in employees:
		salary_slips = frappe.db.sql("""select * from `tabRecord Slip` where employee = '%s' and start_date between '%s' and '%s' order by start_date  """%(emp.name,filters.from_date,filters.to_date),as_dict = True)
		pd = ad = pdw = b = da = hra = wa = ca = ma = sa = oa = eb = eda = ehra = ewa = eca = ema = esa = eoa = oh = omt = gp = epf = esi = ab = i = g = u = le = stl = sc = pmvl = dpf = desi = lw = pt = td = rt = epfw = esiw = tot = inv = ta = la = sad = st = est = ptr = 0	
		for ss in salary_slips:
			pd += float(ss.days_atteded)
			ad += float(ss.ncp)
			pdw += float(frappe.db.get_value('Employee',ss.employee,'per_day_wage') or 0)
			b += float(frappe.db.get_value('Employee',ss.employee,'basic') or 0)
			da += float(frappe.db.get_value('Employee',ss.employee,'dearness_allowance') or 0)
			hra += float(frappe.db.get_value('Employee',ss.employee,'house_rent_allowance') or 0)
			wa += float(frappe.db.get_value('Employee',ss.employee,'washing_allowance') or 0)
			ca += float(frappe.db.get_value('Employee',ss.employee,'conveyance_allowance') or 0)
			ma += float(frappe.db.get_value('Employee',ss.employee,'medical_allowance') or 0)
			sa += float(frappe.db.get_value('Employee',ss.employee,'special_allowance') or 0)
			oa += float(frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['other_allowance']) or 0)
			eb += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Basic",'parent':ss.name},["amount"]) or 0)
			eda += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Dearness Allowance",'parent':ss.name},["amount"]) or 0)
			ehra += int(frappe.get_value('Salary Detail',{'salary_component':"Earned House Rent Allowance",'parent':ss.name},["amount"]) or 0)
			ewa += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Washing Allowance",'parent':ss.name},["amount"]) or 0)
			eca += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Conveyance Allowance",'parent':ss.name},["amount"]) or 0)
			ema += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Medical Allowance",'parent':ss.name},["amount"]) or 0)
			esa += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Special Allowance",'parent':ss.name},["amount"]) or 0)
			eoa += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Other Allowance",'parent':ss.name},["amount"]) or 0)
			oh += float(ss.overtime_hours or 0)
			omt += int(frappe.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':ss.name},["amount"]) or 0)
			gp += int(ss.gross_pay)
			epf += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Provident Fund",'parent':ss.name},["amount"]) or 0)
			esi += int(frappe.get_value('Salary Detail',{'abbr':"ESI",'parent':ss.name},["amount"]) or 0)
			ab += int(frappe.get_value('Salary Detail',{'salary_component':"Attendance Bonus",'parent':ss.name},["amount"]) or 0)
			i += int(frappe.get_value('Salary Detail',{'salary_component':"Insurance",'parent':ss.name},["amount"]) or 0)
			g += int(frappe.get_value('Salary Detail',{'salary_component':"Gratuity",'parent':ss.name},["amount"]) or 0)
			u += int(frappe.get_value('Salary Detail',{'salary_component':"Uniform",'parent':ss.name},["amount"]) or 0)
			le += int(frappe.get_value('Salary Detail',{'salary_component':"Leave Encashment",'parent':ss.name},["amount"]) or 0)
			stl += int(ss.sub_total or 0)
			sc += int(frappe.get_value('Salary Detail',{'salary_component':"Service Charges",'parent':ss.name},["amount"]) or 0)
			pmvl += int(ss.total_payable_to_mvl or 0)
			dpf  += int(frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':ss.name},["amount"]) or 0)
			desi += int(frappe.get_value('Salary Detail',{'abbr':"D_ESI",'parent':ss.name},["amount"]) or 0)
			lw += int(frappe.get_value('Salary Detail',{'salary_component':"L/w Fund",'parent':ss.name},["amount"]) or 0)
			pt += int(frappe.get_value('Salary Detail',{'salary_component':"Professional Tax",'parent':ss.name},["amount"]) or 0)
			td += int(ss.total_deduction or 0)
			rt += int(ss.rounded_total)
			epfw += int(ss.epf_wages or 0)
			esiw += int(ss.esi_wages or 0)
			tot += ((int(ss.gross_pay)) - int(frappe.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':ss.name},["amount"]) or 0))
			inv = frappe.db.get_value('Employee',ss.employee,'invoice_name') 
			ta += int(frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['transport_allowance']) or 0)
			la += int(frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['lunch_allowance']) or 0)
			sad += int(frappe.get_value('Salary Detail',{'salary_component':"Salary Advance Detection",'parent':ss.name},["amount"]) or 0)
			st += int(frappe.db.get_value('Employee',ss.employee,'stipend') or 0)
			est += int(frappe.get_value('Salary Detail',{'salary_component':"Stipend",'parent':ss.name},["amount"]) or 0)
			ptr += int(frappe.get_value('Salary Detail',{'salary_component':"PT Refund",'parent':ss.name},["amount"]) or 0)
		row1 = [1, 
		 	ss.start_date,
			ss.end_date,
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
			pd,ad,pdw,b,da,hra,wa,ca,ma,sa,oa,(b+da+hra+wa+ca+ma+sa),eb,eda,ehra,ewa,eca,ema,esa,eoa,oh,omt,gp,epf,esi,ab,i,g,u,le,stl,sc,pmvl,dpf,desi,lw,pt,td,rt,epfw,esiw,tot,inv,ta,la,sad,st,est,ptr
			]
		
		salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where employee = '%s' and docstatus != 2 and start_date between '%s' and '%s' order by start_date  """%(emp.name,filters.from_date,filters.to_date),as_dict = True)
		pd = ad = pdw = b = da = hra = wa = ca = ma = sa = oa = eb = eda = ehra = ewa = eca = ema = esa = eoa = oh = omt = gp = epf = esi = ab = i = g = u = le = stl = sc = pmvl = dpf = desi = lw = pt = td = rt = epfw = esiw = tot = inv = ta = la = sad = st = est = ptr = 0	
		for ss in salary_slips:
			pd += float(ss.payment_days)
			ad += float(ss.absent_days)
			pdw += float(frappe.db.get_value('Employee',ss.employee,'per_day_wage') or 0)
			b += float(frappe.db.get_value('Employee',ss.employee,'basic') or 0)
			da += float(frappe.db.get_value('Employee',ss.employee,'dearness_allowance') or 0)
			hra += float(frappe.db.get_value('Employee',ss.employee,'house_rent_allowance') or 0)
			wa += float(frappe.db.get_value('Employee',ss.employee,'washing_allowance') or 0)
			ca += float(frappe.db.get_value('Employee',ss.employee,'conveyance_allowance') or 0)
			ma += float(frappe.db.get_value('Employee',ss.employee,'medical_allowance') or 0)
			sa += float(frappe.db.get_value('Employee',ss.employee,'special_allowance') or 0)
			oa += float(frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['other_allowance']) or 0)
			eb += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Basic",'parent':ss.name},["amount"]) or 0)
			eda += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Dearness Allowance",'parent':ss.name},["amount"]) or 0)
			ehra += int(frappe.get_value('Salary Detail',{'salary_component':"Earned House Rent Allowance",'parent':ss.name},["amount"]) or 0)
			ewa += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Washing Allowance",'parent':ss.name},["amount"]) or 0)
			eca += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Conveyance Allowance",'parent':ss.name},["amount"]) or 0)
			ema += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Medical Allowance",'parent':ss.name},["amount"]) or 0)
			esa += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Special Allowance",'parent':ss.name},["amount"]) or 0)
			eoa += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Other Allowance",'parent':ss.name},["amount"]) or 0)
			oh += float(ss.overtime_hours or 0)
			omt += int(frappe.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':ss.name},["amount"]) or 0)
			gp += int(ss.gross_pay)
			epf += int(frappe.get_value('Salary Detail',{'salary_component':"Earned Provident Fund",'parent':ss.name},["amount"]) or 0)
			esi += int(frappe.get_value('Salary Detail',{'abbr':"ESI",'parent':ss.name},["amount"]) or 0)
			ab += int(frappe.get_value('Salary Detail',{'salary_component':"Attendance Bonus",'parent':ss.name},["amount"]) or 0)
			i += int(frappe.get_value('Salary Detail',{'salary_component':"Insurance",'parent':ss.name},["amount"]) or 0)
			g += int(frappe.get_value('Salary Detail',{'salary_component':"Gratuity",'parent':ss.name},["amount"]) or 0)
			u += int(frappe.get_value('Salary Detail',{'salary_component':"Uniform",'parent':ss.name},["amount"]) or 0)
			le += int(frappe.get_value('Salary Detail',{'salary_component':"Leave Encashment",'parent':ss.name},["amount"]) or 0)
			stl += int(ss.sub_total or 0)
			sc += int(frappe.get_value('Salary Detail',{'salary_component':"Service Charges",'parent':ss.name},["amount"]) or 0)
			pmvl += int(ss.total_payable_to_mvl or 0)
			dpf  += int(frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':ss.name},["amount"]) or 0)
			desi += int(frappe.get_value('Salary Detail',{'abbr':"D_ESI",'parent':ss.name},["amount"]) or 0)
			lw += int(frappe.get_value('Salary Detail',{'salary_component':"L/w Fund",'parent':ss.name},["amount"]) or 0)
			pt += int(frappe.get_value('Salary Detail',{'salary_component':"Professional Tax",'parent':ss.name},["amount"]) or 0)
			td += int(ss.total_deduction or 0)
			rt += int(ss.rounded_total)
			epfw += int(ss.epf_wages or 0)
			esiw += int(ss.esi_wages or 0)
			tot += ((int(ss.gross_pay)) - int(frappe.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':ss.name},["amount"]) or 0))
			inv = frappe.db.get_value('Employee',ss.employee,'invoice_name') 
			ta += int(frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['transport_allowance']) or 0)
			la += int(frappe.db.get_value('Attendance and OT Register',{'employee':ss.employee,'start_date':filters.from_date,'docstatus':1},['lunch_allowance']) or 0)
			sad += int(frappe.get_value('Salary Detail',{'salary_component':"Salary Advance Detection",'parent':ss.name},["amount"]) or 0)
			st += int(frappe.db.get_value('Employee',ss.employee,'stipend') or 0)
			est += int(frappe.get_value('Salary Detail',{'salary_component':"Stipend",'parent':ss.name},["amount"]) or 0)
			ptr += int(frappe.get_value('Salary Detail',{'salary_component':"PT Refund",'parent':ss.name},["amount"]) or 0)
		row = [1, 
		 	ss.start_date,
			ss.end_date,
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
			pd,ad,pdw,b,da,hra,wa,ca,ma,sa,oa,(b+da+hra+wa+ca+ma+sa),eb,eda,ehra,ewa,eca,ema,esa,eoa,oh,omt,gp,epf,esi,ab,i,g,u,le,stl,sc,pmvl,dpf,desi,lw,pt,td,rt,epfw,esiw,tot,inv,ta,la,sad,st,est,ptr
			]

		data.append(row1)
		data.append(row)
	return data

def get_columns():
	columns = [
		_("Index") + ":Data/:50",
		_("Start Date") + ":Date/:50",
		_("End Date") + ":Date/:50",
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
		_("Earned Provident Fund 13%") + ":Data:150",
		_("Earned Employee State Insurence 3.75%") + ":Data:150",
		_("Attendance Bonus") + ":Data:150",
		_("Insurance") + ":Data:150",
		_("Gratuity") + ":Data:150",
		_("Uniform") + ":Data:150",
		_("CL/EL") + ":Data:150",
		_("Sub Total") + ":Data:150",
		_("Service Charges") + ":Data:150",
		_("Total payable to MVL") + ":Data:150",
		_("Provident Fund 12 %") + ":Data:150",
		_("Employee State Insurence 0.75%") + ":Data:150",
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
		_("Fixed Stipned") + ":Data:150",
		_("Earned Stipned") + ":Data:150",
		_("PT Refund") + ":Data:150"
	]
	return columns