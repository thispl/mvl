
from codecs import ignore_errors
from multiprocessing.spawn import old_main_modules
from os import truncate
from types import FrameType
import frappe
import json
import re
from frappe import throw,_
import datetime
from frappe.utils import add_years
from datetime import datetime
from frappe.utils.background_jobs import enqueue
from frappe import permissions
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import read_csv_content
from frappe.utils.data import format_date, get_url_to_list
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
						  nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime, format_date,get_time)
from datetime import datetime
from calendar import IllegalMonthError, month, monthrange
from frappe import _, get_value, msgprint
from frappe.utils import flt, get_url_to_list
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, today
import requests
from datetime import date, timedelta, time
import calendar
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from datetime import datetime
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from frappe import _
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


@frappe.whitelist()
def get_total_payable_to_mvl(doc,method):
	added_to_sub_total = 0
	added_to_total_payable__to_mvl = 0
	added_to_epf_wages = 0
	added_to_esi_wages = 0
	invoice = frappe.get_value("Invoice Name",{'name':doc.invoice_name},['sub_total','total_payable_to_mvl','epf_wages','esi_wages'])
	for i in doc.earnings:
		if invoice[0] == 1:
			if i.added_to_sub_total == 1:
				added_to_sub_total += i.amount
		if invoice[1] == 1:
			if i.added_to_total_payable__to_mvl == 1:
				added_to_total_payable__to_mvl += i.amount
		if invoice[2] == 1:
			if i.salary_component == "EPF Wages":
				added_to_epf_wages = i.amount
		if invoice[3] == 1:
			if i.salary_component == "ESI Wages":
				added_to_esi_wages = i.amount
	frappe.db.set_value("Salary Slip",doc.name,"sub_total",added_to_sub_total)
	frappe.db.set_value("Salary Slip",doc.name,"total_payable_to_mvl",added_to_total_payable__to_mvl)
	frappe.db.set_value("Salary Slip",doc.name,"epf_wages",added_to_epf_wages)
	frappe.db.set_value("Salary Slip",doc.name,"esi_wages",added_to_esi_wages)
	if doc.arrear_slip == 1:
		if frappe.db.exists("Salary Slip",{'employee':doc.employee,'start_date':doc.start_date,'end_date':doc.end_date,'docstatus':('!=',2),'arrear_slip':0}):
			ssl = frappe.get_doc("Salary Slip",{'employee':doc.employee,'start_date':doc.start_date,'end_date':doc.end_date,'docstatus':('!=',2),'arrear_slip':0})
			
			ss = frappe.get_value("Salary Slip",{'employee':doc.employee,'start_date':doc.start_date,'end_date':doc.end_date,'docstatus':('!=',2),'arrear_slip':0},['name'])
			ss_epf_wages = frappe.get_value("Salary Slip",{'employee':doc.employee,'start_date':doc.start_date,'end_date':doc.end_date,'docstatus':('!=',2),'arrear_slip':0},['epf_wages'])
			ss_esi_wages = frappe.get_value("Salary Slip",{'employee':doc.employee,'start_date':doc.start_date,'end_date':doc.end_date,'docstatus':('!=',2),'arrear_slip':0},['esi_wages'])
			
			epf = frappe.get_value('Salary Detail',{'salary_component':"Earned Provident Fund",'parent':ss},["amount"])
			esi = frappe.get_value('Salary Detail',{'abbr':"ESI",'parent':ss},["amount"])
			dpf = frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':ss},["amount"])
			desi = frappe.get_value('Salary Detail',{'abbr':"D_ESI",'parent':ss},["amount"])	
			parent_doc = frappe.get_doc('Salary Slip', doc.name)
			for detail in ssl.get('earnings'):
				if detail.salary_component == "Earned Provident Fund" and epf == 0:
					detail.amount = 0
				elif detail.salary_component == "Employee State Insurance" and esi == 0:
					detail.amount = 0
			for detail in ssl.get('deductions'):
				if detail.salary_component == "Provident Fund" and dpf == 0:
					detail.amount = 0
				elif detail.salary_component == "Deduction Employee State Insurance" and desi == 0:
					detail.amount = 0
			if ss_epf_wages == 0 :
				doc.epf_wages = 0
			if ss_esi_wages == 0:
				doc.esi_wages = 0 
			parent_doc.save()
	if doc.arrear_slip == 0:
		if frappe.db.exists("Salary Slip", {'employee': doc.employee, 'docstatus': ('!=', 2), 'arrear_slip': 1, 'parent_slip': ('!=', '')}):
			ss_list = frappe.get_all("Salary Slip", {'employee': doc.employee, 'docstatus': ('!=', 2), 'arrear_slip': 1, 'parent_slip': ('!=', '')})
			net_total = 0
			for s in ss_list:
				net_total += s.rounded_total
				frappe.db.set_value("Salary Slip", s.name, "parent_slip", doc.name)
				frappe.db.commit()
			frappe.db.set_value("Salary Slip", doc.name, "arrear_amount", net_total)

@frappe.whitelist()
def update_ncp(doc,method):
	if doc.unit == "ABC-CBE":
		tot = frappe.get_value("Unit",{'name':doc.unit},['man_days'])
		ncp = tot - doc.payment_days
		frappe.errprint(tot)
		frappe.errprint(ncp)
	else:
		tot = date_diff(doc.end_date, doc.start_date) + 1
		ncp = tot - doc.payment_days
		frappe.errprint(tot)
		frappe.errprint(ncp)
	frappe.db.set_value("Attendance and OT Register",doc.name,"non_contribution_days",ncp)

@frappe.whitelist()
def update_man_days(unit,man_days):
	employee = frappe.get_all("Employee",{'status':"Active",'unit':unit},['*'])
	for emp in employee:
		frappe.db.set_value("Employee",emp.name,"man_days",man_days)
		if emp.per_day_wage != 0:
			frappe.db.set_value("Employee",emp.name,"basic",(float(emp.per_day_wage) * float(man_days)))
	return "OK"

@frappe.whitelist()
def get_man_days_via_employee(pdw,md):
	if pdw != 0:
		frappe.errprint("HI")
		basic = float(pdw) * float(md)
		return basic
		

@frappe.whitelist()
def get_total_via_employee(basic, house_rent_allowance, dearness_allowance, washing_allowance, conveyance_allowance , medical_allowance , special_allowance):
	total = int(basic) + int(house_rent_allowance) + int(dearness_allowance) + int(washing_allowance) + int(conveyance_allowance) + int(medical_allowance) + int(special_allowance)
	return total

@frappe.whitelist()
def get_total_arrear_via_employee(arrear_basic, arrear_house_rent_allowance, arrear_dearness_allowance, arrear_washing_allowance, arrear_conveyance_allowance , arrear_medical_allowance , arrear_special_allowance , arrear_stipend):
	arrear_total = int(arrear_basic) + int(arrear_house_rent_allowance) + int(arrear_dearness_allowance) + int(arrear_washing_allowance) + int(arrear_conveyance_allowance) + int(arrear_medical_allowance) + int(arrear_special_allowance) + int(arrear_stipend)
	return arrear_total

@frappe.whitelist()
def get_basic(pdw):
	today = date.today()
	last_day = get_last_day(today)
	input_string = str(last_day)
	last_four_digits = input_string[-2:]
	basic = int(pdw) * int(last_four_digits)
	return basic

		

@frappe.whitelist()
def date_of_retirement():
	employee = frappe.get_all(
		'Employee',
		filters={'status':'Active'},
		fields=['*']
	)
	for i in employee:
		retirement_date = add_years(i.date_of_birth, 60)
		today = date.today()
		if today < retirement_date:
			import datetime
			import calendar
			first_day_current_month = datetime.date(retirement_date.year, retirement_date.month, 1)
			last_day = calendar.monthrange(retirement_date.year, retirement_date.month)[1]
			result_date = first_day_current_month + timedelta(days=last_day - 1)
			frappe.db.set_value('Employee', i.name, 'date_of_retirement', retirement_date)
			frappe.db.set_value('Employee', i.name, 'actual_relieving_date', result_date)

@frappe.whitelist()
def date_of_retirement_mail():
	import datetime
	current_date = datetime.date.today()
	month = current_date.month
	first_date = datetime.date(current_date.year, month + 1, 1)
	if month == 12:
		next_month = 2
		next_year = current_date.year + 1
	else:
		next_month = month + 2
		next_year = current_date.year
	last_date = datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)
	print("First date of the current month:", first_date)
	print("Last date of the current month:", last_date)
	employee = frappe.get_all(
		'Employee',
		filters={'status':'Active','actual_relieving_date':('between',(first_date,last_date))},
		fields=['*']
	)
	for i in employee:
		print(i.actual_relieving_date)
		print(i.employee)

@frappe.whitelist()
def get_amt(invoice_name,start_date,end_date):
	amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' """%(invoice_name, start_date,end_date),as_dict=1)[0]
	return amt['amt'] or 0

@frappe.whitelist()
def change_draft():
	net = frappe.db.sql("""select sum(net_pay) as amount from `tabSalary Slip` where start_date = '%s' and end_date ='%s' and docstatus != 2"""%("2023-07-01","2023-07-31"),as_dict=1)[0] or 0
	lun = frappe.db.sql("""select sum(lunch_allowance) as amount from `tabAttendance and OT Register` where start_date ='%s' and end_date ='%s' and docstatus = 1"""%("2023-07-01","2023-07-31"),as_dict=1)[0] or 0
	tra = frappe.db.sql("""select sum(transport_allowance) as amount from `tabAttendance and OT Register` where start_date ='%s' and end_date ='%s' and docstatus = 1"""%("2023-07-01","2023-07-31"),as_dict=1)[0] or 0
	print((net['amount']))
	print((lun['amount']))
	print((tra['amount']))

@frappe.whitelist()
def contract_end_date(contract_start_date,years):
	from datetime import datetime, timedelta
	frappe.errprint("HI")
	if contract_start_date:
		csd = datetime.strptime(contract_start_date, "%Y-%m-%d")
		cy = int(years)
		frappe.errprint(type(csd))
		frappe.errprint(type(cy))
		ced = csd + timedelta(days=cy * 365)
		ced_date = datetime.strptime(str(ced), "%Y-%m-%d %H:%M:%S")
		frappe.errprint(ced)
		frappe.errprint(ced_date)
		contract_end_date = ced_date.strftime("%Y-%m-%d")
		frappe.errprint(contract_end_date)
		return contract_end_date
	
@frappe.whitelist()
def get_contract_end_date(doc,method):
	from datetime import datetime, timedelta
	if doc.contract_start_date:
		csd = datetime.strptime(doc.contract_start_date, "%Y-%m-%d")
		cy = doc.contract_years
		frappe.errprint(type(csd))
		frappe.errprint(type(cy))
		ced = csd + timedelta(days=cy * 365)
		ced_date = datetime.strptime(str(ced), "%Y-%m-%d %H:%M:%S")
		frappe.errprint(ced)
		frappe.errprint(ced_date)
		contract_end_date = ced_date.strftime("%Y-%m-%d")
		frappe.db.set_value('Employee', doc.name, 'contract_end_date', contract_end_date)

		

# @frappe.whitelist()
# def create_cl(doc,method):
# 	import datetime
# 	doj = str(doc.date_of_joining)
# 	employee_date_of_joining = datetime.datetime.strptime(doj, "%Y-%m-%d %H:%M:%S")
# 	current_date = datetime.datetime.now()
# 	if employee_date_of_joining.year == current_date.year and employee_date_of_joining.month == current_date.month:
# 		print(doc.name)
# 		print("Employee joined this month.")
# 		if not frappe.db.exists("Employee Casual Leave",{'employee':doc.employee}):
# 			att = frappe.new_doc("Employee Casual Leave")
# 			att.employee = doc.employee
# 			att.date = doc.date_of_joining
# 			att.employee_name = doc.employee_name
# 			att.company = doc.company
# 			att.total_leaves_allocated = 1
# 			att.save(ignore_permissions=True)
# 			frappe.db.commit()
# 		else:
# 			frappe.errprint("HI")
	
@frappe.whitelist()
def update_casual_leave(doc,method):
	casual_leave_doc = frappe.get_all("Employee Casual Leave", filters={"employee": doc.employee}, limit=1)
	if casual_leave_doc:
		casual_leave_doc = frappe.get_doc("Employee Casual Leave", casual_leave_doc[0].name)
		if casual_leave_doc.total_leaves_allocated is not None:
			total_leaves_allocated = int(casual_leave_doc.total_leaves_allocated)
			doc.cl_days = int(doc.cl_days)
			if total_leaves_allocated >= doc.cl_days:
				casual_leave_doc.total_leaves_allocated = str(total_leaves_allocated - doc.cl_days)
				casual_leave_doc.save()
				return "Casual leave deducted successfully."
			else:
				return "Insufficient casual leave balance."
		else:
			frappe.throw(_("Casual leave allocation not found.")) 
		frappe.throw(_("Employee Casual Leave document not found."))


@frappe.whitelist()
def validate_dat(doc, method):
	if doc.is_new():
		existing_doc = frappe.get_all(doc.doctype, filters={'start_date': doc.start_date,'employee':doc.employee,'docstatus':1})
		if existing_doc:
			frappe.throw(f"Attendance and OT Register with start date {doc.start_date} for Employee {doc.employee}is already exists. Please choose a different date.")
	date_1 = str(doc.start_date)
	date_2 = str(doc.end_date)
	length_of_string1 = len(date_1)
	length_of_string2 = len(date_2)
	if length_of_string1 > 10 and length_of_string2 > 10:
		date1 = datetime.strptime(date_1, "%Y-%m-%d %H:%M:%S")
		date2 = datetime.strptime(date_2, "%Y-%m-%d %H:%M:%S")
	else:
		date1 = datetime.strptime(date_1, "%Y-%m-%d").date()
		date2 = datetime.strptime(date_2, "%Y-%m-%d").date()

	date_difference = (date2 - date1).days
	payment_days = int(doc.payment_days)

	if payment_days > (date_difference + 1):
		frappe.throw(f"Payroll Days is {date_difference}, but Payment Days is {payment_days}. Kindly check the Payment Days")


@frappe.whitelist()
def create_hooks_att():
	job = frappe.db.exists('Scheduled Job Type', 'update_total_leaves_allocated')
	if not job:
		att = frappe.new_doc("Scheduled Job Type")
		att.update({
			"method": 'mvl.custom.update_total_leaves_allocated',
			"frequency": 'Cron',
			"cron_format": '30 00 * * *'
		})
		att.save(ignore_permissions=True)


@frappe.whitelist()
def update_total_leaves_allocated():
	employees = frappe.get_all("Employee",{'status':"Active"},['*'])
	for emp in employees:
		print(emp.date_of_joining)
		today = date.today()
		doj = str(emp.date_of_joining)
		do = datetime.strptime(doj, '%Y-%m-%d')
		add_do = do + timedelta(days=30)
		add_do_str = add_do.strftime("%Y-%m-%d")
		add_date = datetime.strptime(add_do_str, '%Y-%m-%d').date()
		print(today)
		print(add_date)
		if not frappe.db.exists("Employee Casual Leave",{'employee':emp.name}):
			if add_date == today:
				print("HI")
				leave = frappe.new_doc("Employee Casual Leave")
				leave.employee = emp.name
				leave.total_leaves_allocated = 1
				leave.last_add_on = today
				doj = str(today)
				do = datetime.strptime(doj, '%Y-%m-%d')
				add_do = do + timedelta(days=30)
				add_do_str = add_do.strftime("%Y-%m-%d")
				add_date = datetime.strptime(add_do_str, '%Y-%m-%d').date()
				leave.next_add_on = add_date
				leave.save(ignore_permissions = True)
				frappe.db.commit
		else:
			leave = frappe.get_doc("Employee Casual Leave",{'employee':emp.name})
			if leave.next_add_on == today:
				print("HI")
				leave.total_leaves_allocated = leave.total_leaves_allocated + 1
				leave.last_add_on = today
				doj = str(today)
				do = datetime.strptime(doj, '%Y-%m-%d')
				add_do = do + timedelta(days=30)
				add_do_str = add_do.strftime("%Y-%m-%d")
				add_date = datetime.strptime(add_do_str, '%Y-%m-%d').date()
				leave.next_add_on = add_date
				leave.save(ignore_permissions = True)
				frappe.db.commit

@frappe.whitelist()
def get_data_for_annexture(from_date,to_date,invoice_name):
	data = ''
	data += '<table  border= 1 solid black width = 100%>'
	slip = frappe.get_all("Salary Slip",{'start_date': from_date,'end_date':to_date,'invoice_name':invoice_name } ,['*'])
	data += '<tr><td style="padding:1px;border: 1px solid black;"><b>EmpID</b></td><td style="padding:1px;border: 1px solid black;"><b>EmpName</b></td><td style="padding:1px;border: 1px solid black;"><b>Designation</b></td><td style="padding:1px;border: 1px solid black;"><b>Location</b></td><td style="padding:1px;border: 1px solid black;"><b>DaysAttd</b></td><td style="padding:1px;border: 1px solid black;"><b>B</b></td><td style="padding:1px;border: 1px solid black;"><b>DA</b></td><td style="padding:1px;border: 1px solid black;"><b>HRA</b></td><td style="padding:1px;border: 1px solid black;"><b>WA</b></td><td style="padding:1px;border: 1px solid black;"><b>CA</b></td><td style="padding:1px;border: 1px solid black;"><b>SPA</b></td><td style="padding:1px;border: 1px solid black;"><b>MA</b></td><td style="padding:1px;border: 1px solid black;"><b>Total</b></td><td style="padding:1px;border: 1px solid black;"><b>EB</b></td><td style="padding:1px;border: 1px solid black;"><b>EDA</b></td><td style="padding:1px;border: 1px solid black;"><b>EHRA</b></td><td style="padding:1px;border: 1px solid black;"><b>EWA</b></td><td style="padding:1px;border: 1px solid black;"><b>ECA</b></td><td style="padding:1px;border: 1px solid black;"><b>ESPA</b></td><td style="padding:1px;border: 1px solid black;"><b>EMA</b></td><td style="padding:1px;border: 1px solid black;"><b>OA</b></td><td style="padding:1px;border: 1px solid black;"><b>OT Hrs</b></td><td style="padding:1px;border: 1px solid black;"><b>OT Amt</b></td><td style="padding:1px;border: 1px solid black;"><b>Gross</b></td><td style="padding:1px;border: 1px solid black;"><b>EPF 13%</b></td><td style="padding:1px;border: 1px solid black;"><b>ESI 3.28%</b></td><td style="padding:1px;border: 1px solid black;"><b>Bonus</b></td><td style="padding:1px;border: 1px solid black;"><b>U</b></td><td style="padding:1px;border: 1px solid black;"><b>I</b></td><td style="padding:1px;border: 1px solid black;"><b>Sub Total</b></td><td style="padding:1px;border: 1px solid black;"><b>SC10%</b></td><td style="padding:1px;border: 1px solid black;"><b>Total Payable to MVL</b></td><td style="padding:1px;border: 1px solid black;"><b>DPF 12%</b></td><td style="padding:1px;border: 1px solid black;"><b>DESI 0.78%</b></td><td style="padding:1px;border: 1px solid black;"><b>L/W Fund</b></td><td style="padding:1px;border: 1px solid black;"><b>P/Tax</b></td><td style="padding:1px;border: 1px solid black;"><b>I/Tax</b></td><td style="padding:1px;border: 1px solid black;"><b>Salary Advance</b></td><td style="padding:1px;border: 1px solid black;"><b>Deductions</b></td><td style="padding:1px;border: 1px solid black;"><b>Net Pay</b></td></tr>'
	pd = 0
	t_bas = 0
	t_da = 0
	t_hra = 0
	t_wa = 0
	t_ca = 0
	t_spa = 0
	t_ma = 0
	t_tot = 0
	t_ebas = 0
	t_eda = 0
	t_ehra = 0
	t_ewa = 0
	t_eca = 0
	t_espa = 0
	t_ema = 0
	t_oa = 0
	t_ot_hours = 0
	t_ot_amt = 0
	t_egross = 0
	t_epf = 0
	t_esi = 0
	t_ab = 0
	t_uniform = 0
	t_ins = 0
	t_leave = 0
	t_add = 0
	t_mvl = 0
	t_dpf = 0
	t_desi = 0
	t_lf = 0
	t_ptax = 0
	t_intx = 0
	t_od = 0
	t_sad = 0
	t_net = 0
	
	for i in slip:
		bas = frappe.db.get_value("Employee",{'name':i.employee} ,['basic']) 
		da = frappe.db.get_value("Employee",{'name':i.employee} ,['dearness_allowance']) 
		hra = frappe.db.get_value("Employee",{'name':i.employee} ,['house_rent_allowance']) 
		wa = frappe.db.get_value("Employee",{'name':i.employee} ,['washing_allowance']) 
		ca = frappe.db.get_value("Employee",{'name':i.employee} ,['conveyance_allowance']) 
		spa = frappe.db.get_value("Employee",{'name':i.employee} ,['special_allowance']) 
		ma = frappe.db.get_value("Employee",{'name':i.employee} ,['medical_allowance']) 
		gross = bas+da+hra+wa+ca+spa+ma
		ebas = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Basic",'parent':i.name},["amount"]) or 0
		eda = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Dearness Allowance",'parent':i.name},["amount"]) or 0
		ehra = frappe.db.get_value('Salary Detail',{'salary_component':"Earned House Rent Allowance",'parent':i.name},["amount"]) or 0
		ewa = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Washing Allowance",'parent':i.name},["amount"]) or 0
		eca = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Conveyance Allowance",'parent':i.name},["amount"]) or 0
		espa = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Medical Allowance",'parent':i.name},["amount"]) or 0
		ema = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Special Allowance",'parent':i.name},["amount"]) or 0
		oa = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Other Allowance",'parent':i.name},["amount"]) or 0
		ot_hours = i.overtime_hours
		ot_amt = frappe.db.get_value('Salary Detail',{'salary_component':"Overtime Amount",'parent':i.name},["amount"]) or 0
		egross = ebas + eda + ehra + ewa + eca + espa + ema + oa + ot_amt
		epf = frappe.db.get_value('Salary Detail',{'salary_component':"Earned Provident Fund",'parent':i.name},["amount"]) or 0
		esi = frappe.db.get_value('Salary Detail',{'abbr':"ESI",'parent':i.name},["amount"]) or 0
		ab = frappe.db.get_value('Salary Detail',{'salary_component':"Attendance Bonus",'parent':i.name},["amount"]) or 0
		uniform = frappe.db.get_value('Salary Detail',{'salary_component':"Uniform",'parent':i.name},["amount"]) or 0
		ins = frappe.db.get_value('Salary Detail',{'salary_component':"Insurance",'parent':i.name},["amount"]) or 0
		leave = frappe.db.get_value('Salary Detail',{'salary_component':"Leave Encashment",'parent':i.name},["amount"]) or 0
		add = frappe.db.get_value('Salary Detail',{'salary_component':"Other Additions",'parent':i.name},["amount"]) or 0
		dpf = frappe.db.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':i.name},["amount"]) or 0 
		desi = frappe.db.get_value('Salary Detail',{'abbr':"D_ESI",'parent':i.name},["amount"]) or 0 
		lf = frappe.db.get_value('Salary Detail',{'salary_component':"L/w Fund",'parent':i.name},["amount"]) or 0 
		ptax = frappe.db.get_value('Salary Detail',{'salary_component':"Professional Tax",'parent':i.name},["amount"]) or 0 
		intx = frappe.db.get_value('Salary Detail',{'salary_component':"Income Tax",'parent':i.name},["amount"]) or 0 
		od = frappe.db.get_value('Salary Detail',{'salary_component':"Other Deductions",'parent':i.name},["amount"]) or 0 
		sad = frappe.db.get_value('Salary Detail',{'salary_component':"Salary Advance Detection",'parent':i.name},["amount"]) or 0 
		data += '<tr><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td><td style="padding:1px;border: 1px solid black;">%s</td></tr>'%(
	i.employee,
	i.employee_name,
	i.designation,
	i.unit,
	i.payment_days,
	int(bas),
	int(da),
	int(hra),
	int(wa),
	int(ca),
	int(spa),
	int(ma),
	int(gross),
	int(ebas),
	int(eda),
	int(ehra),
	int(ewa),
	int(eca),
	int(espa),
	int(ema),
	int(oa),
	ot_hours,
	int(ot_amt),
	int(egross),
	int(epf),
	int(esi),
	int(ab),
	int(uniform),
	int(ins),
	int(leave),
	int(add),
	int(i.total_payable_to_mvl),
	int(dpf),
	int(desi),
	int(lf),
	int(ptax),
	int(intx),
	int(od),
	int(sad),
	int(i.rounded_total)
	)
		pd += i.payment_days
		t_bas += bas
		t_da += da
		t_hra += hra
		t_wa += wa
		t_ca += ca
		t_spa += spa
		t_ma += ma
		t_tot += gross
		t_ebas += ebas
		t_eda += eda
		t_ehra += ehra
		t_ewa += ewa
		t_eca += eca
		t_espa += espa
		t_ema += ema
		t_oa += oa
		t_ot_hours += ot_hours
		t_ot_amt += ot_amt
		t_egross += egross
		t_epf += epf
		t_esi += esi
		t_ab += ab
		t_uniform += uniform
		t_ins += ins
		t_leave += leave
		t_add += add
		t_mvl += i.total_payable_to_mvl
		t_dpf += dpf
		t_desi += desi
		t_lf += lf
		t_ptax += ptax
		t_intx += intx
		t_od += od
		t_sad += sad
		t_net += i.rounded_total
	data += '<tr><td colspan =4><b>Total</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;border: 1px solid black;"><b>%s</b></td></tr>'%(
	int(pd),
	int(t_bas),
	int(t_da),
	int(t_hra),
	int(t_wa),
	int(t_ca),
	int(t_spa),
	int(t_ma),
	int(t_tot),
	int(t_ebas),
	int(t_eda),
	int(t_ehra),
	int(t_ewa),
	int(t_eca),
	int(t_espa),
	int(t_ema),
	int(t_oa),
	int(t_ot_hours),
	int(t_ot_amt),
	int(t_egross),
	int(t_epf),
	int(t_esi),
	int(t_ab),
	int(t_uniform),
	int(t_ins),
	int(t_leave),
	int(t_add),
	int(t_mvl),
	int(t_dpf),
	int(t_desi),
	int(t_lf),
	int(t_ptax),
	int(t_intx),
	int(t_od),
	int(t_sad),
	int(t_net)
	)
	data += '</table>'
	return data

@frappe.whitelist()
def att_ot_cancel():
	cancel = frappe.db.sql("""delete from `tabSalary Slip` """,as_dict = True)
	print(cancel)

@frappe.whitelist()
def inactive_employee(doc,method):
	if doc.status=="Active":
		if doc.relieving_date:
			throw(_("Please remove the relieving date for the Active Employee."))

@frappe.whitelist()
def update_employee_no(name,employee_number):
	emp = frappe.get_doc("Employee",name)
	emps=frappe.get_all("Employee",{"status":"Active"},['*'])
	for i in emps:
		if emp.employee_number == employee_number:
			pass
		elif i.employee_number == employee_number:
			frappe.throw(f"Employee Number already exists for {i.name}")
		else:
			frappe.db.set_value("Employee",name,"employee_number",employee_number)
			frappe.rename_doc("Employee", name, employee_number, force=1)
			return employee_number

@frappe.whitelist()
def total_tracking():
	employee=frappe.get_all('Employee',{'status':'Active'},['*'])
	first_day_current_month = datetime.today().replace(day=1)
	last_day_previous_month = first_day_current_month - timedelta(days=1)
	first_day_previous_month = last_day_previous_month.replace(day=1)
	formatted_first_day = first_day_previous_month.strftime("%Y-%m-%d")
	formatted_last_day = last_day_previous_month.strftime("%Y-%m-%d")
	for emp in employee:
		val=frappe.get_doc('Employee',emp.name)
		val.total_ = int(val.basic) + int(val.house_rent_allowance) + int(val.dearness_allowance) + int(val.washing_allowance) + int(val.conveyance_allowance) + int(val.medical_allowance) + int(val.special_allowance)
		val.append(
			"total_salary_tracking",
			{
				"from_date": formatted_first_day,
				"to_date": formatted_last_day,
				"total_salary":val.total_,
			},)
		val.save()

import frappe

@frappe.whitelist()
def clear_total_salary_tracking():
	# Fetch all active employees
	employees = frappe.get_all('Employee', fields=['name'])
	
	for emp in employees:
		# Fetch the child table entries related to the employee
		child_table_entries = frappe.get_all('Total Salary Tracking', filters={'parent': emp.name}, fields=['name'])
		
		for entry in child_table_entries:
			# Delete each child table entry
			frappe.delete_doc('Total Salary Tracking', entry.name, force=1)
	
	# Commit the changes to the database
	frappe.db.commit()


@frappe.whitelist()
def create_hooks_total_tracking():
	job = frappe.db.exists('Scheduled Job Type', 'total_tracking')
	if not job:
		att = frappe.new_doc("Scheduled Job Type")
		att.update({
			"method": 'mvl.custom.total_tracking',
			"frequency": 'Cron',
			"cron_format": '10 00 1 * *'
		})
		att.save(ignore_permissions=True)


@frappe.whitelist()
def validate_arrear_or_not(doc, method):
	if doc.is_new():
		if doc.unit == '':
			filters = {
				'start_date': doc.start_date,
				'end_date': doc.end_date,
				'docstatus': 0,
				'arrear_slip': doc.arrear_slip,
				'unit':doc.unit
			}
			if frappe.db.exists("Payroll Entry", filters):
				frappe.throw(f"Already exists for the same particulars")
		elif doc.unit != '':
			print("HI")
			filters = {
				'start_date': doc.start_date,
				'end_date': doc.end_date,
				'docstatus': 1,
				'arrear_slip': doc.arrear_slip,
				'unit':''
			}
			if frappe.db.exists("Payroll Entry", filters):
				frappe.throw(f"Already exists for the same particulars")
			filters1 = {
				'start_date': doc.start_date,
				'end_date': doc.end_date,
				'docstatus': 1,
				'arrear_slip': doc.arrear_slip,
				'unit': doc.unit
			}
			if frappe.db.exists("Payroll Entry", filters1):
				frappe.throw(f"Already exists for the same particulars")



@frappe.whitelist()
def cancel_update_casual_leave(doc, method):
	# Check if casual leave days exist
	if doc.cl_days > 0:
		# Check if Employee Casual Leave document exists for the employee
		if frappe.db.exists("Employee Casual Leave", {'employee': doc.employee}):
			# Get the existing Employee Casual Leave document
			casual_leave_doc = frappe.get_doc("Employee Casual Leave", {'employee': doc.employee})
			# Update total leaves allocated by adding casual leave days from the current document
			total_leaves_allocated = int(casual_leave_doc.total_leaves_allocated)
			casual_leave_doc.total_leaves_allocated = str(total_leaves_allocated + doc.cl_days)
			# Save changes to the Employee Casual Leave document
			casual_leave_doc.save()
			# Show success message
			frappe.msgprint("Casual leave added successfully.")
			# Commit changes to the database
			frappe.db.commit()

	# Update document status to '2' (Cancelled) in the tabAttendance and OT Register table
	frappe.db.sql("""UPDATE `tabAttendance and OT Register` SET docstatus = 2 WHERE name = %s""", (doc.name), as_dict=True)

			

@frappe.whitelist()
def updateatt():
	leave = frappe.db.sql("""delete from `tabMonthly Invoice`  """,as_dict = True)
	print(leave)

@frappe.whitelist()
def salary_slip_validate(doc,method):
	frappe.errprint("Validatemethod")
	sdate=frappe.db.exists("Salary Slip",{'start_date':["between", [doc.start_date, doc.end_date]],"docstatus": 1,"employee":doc.employee})
	edate=frappe.db.exists("Salary Slip",{'end_date':["between", [doc.start_date, doc.end_date]],"docstatus": 1,"employee":doc.employee})
	if sdate or edate:
		frappe.throw(_("Salary slip already exists for {0} in the selected period").format(doc.employee))
