# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cstr, add_days, date_diff, getdate, format_date
# from frappe import _, bold
# from frappe.utils.csvutils import UnicodeWriter, read_csv_content
# from frappe.utils.data import format_date
# from frappe.utils.file_manager import get_file
# from frappe.model.document import Document
# from frappe.utils.background_jobs import enqueue

# from datetime import date, timedelta, datetime
# import openpyxl
# from openpyxl import Workbook
# import re
# from frappe import _
# import frappe
# from frappe.model.document import Document
# from datetime import date, timedelta, datetime,time
# from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
# 	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today, format_date)
# # import pandas as pd
# import math
# from frappe.utils import add_months, cint, flt, getdate, time_diff_in_hours,time_diff_in_seconds
# import locale


# import openpyxl
# import xlrd
# import re
# from openpyxl.styles import Font, Alignment, Border, Side
# from openpyxl import load_workbook
# from openpyxl.utils import get_column_letter
# from openpyxl.styles import GradientFill, PatternFill
# from six import BytesIO, string_types
# import openpyxl.styles as styles



# @frappe.whitelist()
# def download():
# 	filename = 'EPF Excel Report'
# 	test = build_xlsx_response(filename)
	
# def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
# 	args = frappe.local.form_dict
# 	column_widths = column_widths or []
# 	if wb is None:
# 		wb = openpyxl.Workbook()
		 
# 	ws = wb.create_sheet(sheet_name, 0)
# 	ws.append(["Emp Code","UAN","Name","EPF Gross Wages","PF Wages","PEN Wages","EDLI Wages","EPFO 12%","EPFO 8.33%","EPFO 3.67%","NCP","REFUND"])
# 	align_center = Alignment(horizontal='center',vertical='center')
# 	for header in ws.iter_rows(min_row=1, max_row=1, min_col=1, max_col=12):
# 		for cell in header:
# 			cell.font = Font(bold=True)
# 			cell.alignment = align_center
	
# 	data1= get_data(args)
# 	for row in data1:
# 		ws.append(row)

# 	xlsx_file = BytesIO()
# 	wb.save(xlsx_file)
# 	return xlsx_file

# def build_xlsx_response(filename):
# 	xlsx_file = make_xlsx(filename)
# 	frappe.response['filename'] = filename + '.xlsx'
# 	frappe.response['filecontent'] = xlsx_file.getvalue()
# 	frappe.response['type'] = 'binary'

# @frappe.whitelist()
# def get_data(args):
# 	ss = []
# 	emp = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE status='Active'""", as_dict=True)
# 	for i in emp:
# 		a = frappe.db.exists("Salary Slip", {'employee': i.name,'start_date': args.start_date,'end_date': args.end_date,'docstatus': ['!=', 2]})

# 		if a:
# 			a_doc = frappe.get_doc("Salary Slip", a) 

# 			pf = a_doc.esi_wages or 0

# 			epf = a_doc.epf_wages or 0
# 			if epf < 15000:
# 				pen = epf
# 			else:
# 				pen = 15000
# 			pfw=(epf * 0.12)
# 			penw=(epf * 0.0833)
# 			edliw=(epf * 0.0367)

# 			ncp=a_doc.absent_days or 0
# 			row = [
# 				i.get('name', ''),
# 				i.get("uan_number",''),
# 				i.get('employee_name', ''),
# 				pf,
# 				epf,
# 				pen,
# 				pen,
# 				round(pfw),
# 				round(penw),
# 				round(edliw),
# 				ncp,
# 				0
# 			]
# 			ss.append(row)
# 	return ss