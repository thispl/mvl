from codecs import ignore_errors
from multiprocessing.spawn import old_main_modules
from os import truncate
from types import FrameType
import frappe
import json
import re
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
# from erpnext.hr.utils import get_holiday_dates_for_employee
# import pandas as pd
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from frappe import _

@frappe.whitelist()
def get_total_payable_to_mvl(doc,method):
	sum_amount = 0
	if doc.invoice_name != "MVL,,Retainer":
		if doc.invoice_name !="MVL,,Manpower Supply Service":
			if doc.principal_employer == "CHN - Retainers":
				for i in doc.earnings:
					if i.salary_component != "Insurance":
						sum_amount += i.amount
				frappe.db.set_value("Salary Slip",doc.name,"total_payable_to_mvl",sum_amount)
			else:
				for i in doc.earnings:
					sum_amount += i.amount
				frappe.db.set_value("Salary Slip",doc.name,"total_payable_to_mvl",sum_amount)

@frappe.whitelist()
def date_of_retirement():
	employee = frappe.get_all(
		'Employee',
		filters={'status':'Active'},
		fields=['*']
	)
	for i in employee:
		# print(i.employee)
		retirement_date = add_years(i.date_of_birth, 60)
		# print(retirement_date)
		today = date.today()
		if today < retirement_date:
			import datetime
			# print(retirement_date)
			import calendar
			first_day_current_month = datetime.date(retirement_date.year, retirement_date.month, 1)
			last_day = calendar.monthrange(retirement_date.year, retirement_date.month)[1]
			result_date = first_day_current_month + timedelta(days=last_day - 1)
			# print("Resulting date:", result_date)
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
def update_workspace():
	work = frappe.db.sql("""update `tabWorkspace` set is_hidden = 1 where name = 'Accounting' """,as_dict = 1)
	print(work)

@frappe.whitelist()
def get_amt(invoice_name,start_date,end_date):
	amt = frappe.db.sql("""select sum(rounded_total)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' """%(invoice_name, start_date,end_date),as_dict=1)[0]
	return amt['amt'] or 0

