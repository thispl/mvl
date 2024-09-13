# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
import math

class MonthlyInvoiceProcessing(Document):
	pass

@frappe.whitelist()
def process_invoice(from_date,to_date):
	invoice = frappe.db.sql("""select * from `tabInvoice Name` where active = 1 """,as_dict = True)
	for i in invoice:
		# frappe.errprint(i.name)
		if i.travel_allowance == 0:
			if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':0}):
				att = frappe.new_doc("Monthly Invoice")
				att.from_date = from_date
				att.to_date = to_date
				att.invoice_name = i.name
				att.arrear_slip = 0
				att.other_state = i.other_state
				att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
				att.invoicing_date = datetime.datetime.now()
				att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
				amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 0 and docstatus = 1 """%(i.name,from_date,to_date),as_dict=1)[0]
				att.total_amount = amt['amt'] or 0
				if att.total_amount != 0:
					if i.other_state == 0:
						att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
						att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
						cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
						sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
						att.cgst_payable_amount = cgst_payable_amount
						att.sgst_payable_amount = sgst_payable_amount
						total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
					else:
						att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
						igst_payable_amount = (amt['amt']*(att.igst_payable))/100
						att.igst_payable_amount = igst_payable_amount
						total = amt['amt'] + igst_payable_amount
					rounded_number = round(total, 2)
					# frappe.errprint(amt['amt'])
					# frappe.errprint(sgst_payable_amount)
					# frappe.errprint(cgst_payable_amount)
					# frappe.errprint(rounded_number)	
					att.total = rounded_number
					value_str = str(rounded_number)
					two_digits = value_str[-2:]
					if '.' in two_digits:
						last_two_digits = value_str[-1:] + '0'
					else:
						last_two_digits = value_str[-2:]
					# frappe.errprint(last_two_digits)
					# frappe.errprint(att.name)
					if  51 > int(last_two_digits) > 0 :
						att.add_on_status = "(Decrease -)"
						rounded_down = math.floor(att.total)
						att.add_on = att.total - rounded_down
						att.roundup = rounded_down
					elif 100 > int(last_two_digits) > 50 :
						att.add_on_status = "(Increase +)"
						rounded_up = math.ceil(att.total)
						att.add_on = rounded_up - att.total 
						att.roundup = rounded_up
					elif int(last_two_digits) == 0 :
						att.add_on_status = ''
						att.add_on = ''
						att.roundup = total
				else:
					att.total = 0
					att.cgst_payable_amount = 0
					att.sgst_payable_amount = 0
					att.igst_payable_amount = 0
				att.save(ignore_permissions=True)
			else:
				att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':0})
				att.from_date = from_date
				att.to_date = to_date
				att.arrear_slip = 0
				att.invoice_name = i.name
				att.other_state = i.other_state
				att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
				att.invoicing_date = datetime.datetime.now()
				att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
				amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 0 and docstatus = 1 """%(i.name,from_date,to_date),as_dict=1)[0]
				att.total_amount = amt['amt'] or 0
				if att.total_amount != 0:
					if i.other_state == 0:
						att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
						att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
						cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
						sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
						att.cgst_payable_amount = cgst_payable_amount
						att.sgst_payable_amount = sgst_payable_amount
						total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
					else:
						att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
						igst_payable_amount = (amt['amt']*(att.igst_payable))/100
						att.igst_payable_amount = igst_payable_amount
						total = amt['amt'] + igst_payable_amount
					rounded_number = round(total, 2)
					# frappe.errprint(amt['amt'])
					# frappe.errprint(sgst_payable_amount)
					# frappe.errprint(cgst_payable_amount)
					# frappe.errprint(rounded_number)	
					att.total = rounded_number
					value_str = str(rounded_number)
					two_digits = value_str[-2:]
					if '.' in two_digits:
						last_two_digits = value_str[-1:] + '0'
					else:
						last_two_digits = value_str[-2:]
					# frappe.errprint(last_two_digits)
					# frappe.errprint(att.name)
					if  51 > int(last_two_digits) > 0 :
						att.add_on_status = "(Decrease -)"
						rounded_down = math.floor(att.total)
						att.add_on = att.total - rounded_down
						att.roundup = rounded_down
					elif 100 > int(last_two_digits) > 50 :
						att.add_on_status = "(Increase +)"
						rounded_up = math.ceil(att.total)
						att.add_on = rounded_up - att.total 
						att.roundup = rounded_up
					elif int(last_two_digits) == 0 :
						att.add_on_status = ''
						att.add_on = ''
						att.roundup = total
				else:
					att.total = 0
					att.cgst_payable_amount = 0
					att.sgst_payable_amount = 0
					att.igst_payable_amount = 0
				att.save(ignore_permissions=True)
				frappe.db.commit()
		else:
			if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':0}):
				att = frappe.new_doc("Monthly Invoice")
				att.from_date = from_date
				att.to_date = to_date
				att.arrear_slip = 0
				att.invoice_name = i.name
				att.other_state = i.other_state
				att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
				att.invoicing_date = datetime.datetime.now()
				att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
				amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
				tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
				sc = tr/10
				att.total_amount = tr + sc 
				if att.total_amount != 0:
					if i.other_state == 0:
						att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
						att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
						cgst_payable_amount = amt[0]['amt']/att.cgst_payable
						sgst_payable_amount = amt[0]['amt']/att.sgst_payable
						att.cgst_payable_amount = cgst_payable_amount
						att.sgst_payable_amount = sgst_payable_amount
						total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
					else:
						att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
						igst_payable_amount = amt[0]['amt']/att.igst_payable
						att.igst_payable_amount = igst_payable_amount
						total = amt[0]['amt'] + igst_payable_amount
					rounded_number = round(total, 2)
					# frappe.errprint(amt['amt'])
					# frappe.errprint(sgst_payable_amount)
					# frappe.errprint(cgst_payable_amount)
					# frappe.errprint(rounded_number)	
					att.total = rounded_number
					value_str = str(rounded_number)
					two_digits = value_str[-2:]
					if '.' in two_digits:
						last_two_digits = value_str[-1:] + '0'
					else:
						last_two_digits = value_str[-2:]
					# frappe.errprint(last_two_digits)
					# frappe.errprint(att.name)
					if  51 > int(last_two_digits) > 0 :
						att.add_on_status = "(Decrease -)"
						rounded_down = math.floor(att.total)
						att.add_on = att.total - rounded_down
						att.roundup = rounded_down
					elif 100 > int(last_two_digits) > 50 :
						att.add_on_status = "(Increase +)"
						rounded_up = math.ceil(att.total)
						att.add_on = rounded_up - att.total 
						att.roundup = rounded_up
					elif int(last_two_digits) == 0 :
						att.add_on_status = ''
						att.add_on = ''
						att.roundup = total
				else:
					att.total = 0
					att.cgst_payable_amount = 0
					att.sgst_payable_amount = 0
					att.igst_payable_amount = 0
				att.save(ignore_permissions=True)
				frappe.db.commit()
			else:
				att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_Slip':0})
				att.from_date = from_date
				att.to_date = to_date
				att.invoice_name = i.name
				att.arrear_slip = 0
				att.other_state = i.other_state
				att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
				att.invoicing_date = datetime.datetime.now()
				att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
				amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
				tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
				sc = tr/10
				att.total_amount = tr + sc 
				if att.total_amount != 0:
					if i.other_state == 0:
						att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
						att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
						cgst_payable_amount = amt[0]['amt']/att.cgst_payable
						sgst_payable_amount = amt[0]['amt']/att.sgst_payable
						att.cgst_payable_amount = cgst_payable_amount
						att.sgst_payable_amount = sgst_payable_amount
						total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
					else:
						att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
						igst_payable_amount = amt[0]['amt']/att.igst_payable
						att.igst_payable_amount = igst_payable_amount
						total = amt[0]['amt'] + igst_payable_amount
					rounded_number = round(total, 2)
					# frappe.errprint(amt['amt'])
					# frappe.errprint(sgst_payable_amount)
					# frappe.errprint(cgst_payable_amount)
					# frappe.errprint(rounded_number)	
					att.total = rounded_number
					value_str = str(rounded_number)
					two_digits = value_str[-2:]
					if '.' in two_digits:
						last_two_digits = value_str[-1:] + '0'
					else:
						last_two_digits = value_str[-2:]
					# frappe.errprint(last_two_digits)
					# frappe.errprint(att.name)
					if  51 > int(last_two_digits) > 0 :
						att.add_on_status = "(Decrease -)"
						rounded_down = math.floor(att.total)
						att.add_on = att.total - rounded_down
						att.roundup = rounded_down
					elif 100 > int(last_two_digits) > 50 :
						att.add_on_status = "(Increase +)"
						rounded_up = math.ceil(att.total)
						att.add_on = rounded_up - att.total 
						att.roundup = rounded_up
					elif int(last_two_digits) == 0 :
						att.add_on_status = ''
						att.add_on = ''
						att.roundup = total
				else:
					att.total = 0
					att.cgst_payable_amount = 0
					att.sgst_payable_amount = 0
					att.igst_payable_amount = 0
				att.save(ignore_permissions=True)
				frappe.db.commit()
	return "ok"

@frappe.whitelist()
def process_invoice_arrear(doc,method):
	from_date = doc.start_date
	to_date = doc.end_date
	if doc.arrear_slip == 1:
		invoice = frappe.db.sql("""select * from `tabInvoice Name` where active = 1 and name = '%s' """%(doc.invoice_name),as_dict = True)
		for i in invoice:
			# frappe.errprint(i.name)
			if i.travel_allowance == 0:
				if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1}):
					att = frappe.new_doc("Monthly Invoice")
					att.from_date = from_date
					att.to_date = to_date
					att.arrear_slip = 1
					att.invoice_name = i.name
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 1 and docstatus = 1 """%(i.name,from_date,to_date),as_dict=1)[0]
					att.total_amount = amt['amt'] or 0
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
							sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = (amt['amt']*(att.igst_payable))/100
							att.igst_payable_amount = igst_payable_amount
							total = amt['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
				else:
					att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1})
					att.from_date = from_date
					att.to_date = to_date
					att.arrear_slip = 1
					att.invoice_name = i.name
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 1 and docstatus = 1  """%(i.name,from_date,to_date),as_dict=1)[0]
					att.total_amount = amt['amt'] or 0
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
							sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = (amt['amt']*(att.igst_payable))/100
							att.igst_payable_amount = igst_payable_amount
							total = amt['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
			else:
				if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1}):
					att = frappe.new_doc("Monthly Invoice")
					att.from_date = from_date
					att.to_date = to_date
					att.invoice_name = i.name
					att.arrear_slip = 1
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date = '%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
					tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
					sc = tr/10
					att.total_amount = tr + sc 
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = amt[0]['amt']/att.cgst_payable
							sgst_payable_amount = amt[0]['amt']/att.sgst_payable
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = amt[0]['amt']/att.igst_payable
							att.igst_payable_amount = igst_payable_amount
							total = amt[0]['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
				else:
					att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1})
					att.from_date = from_date
					att.to_date = to_date
					att.invoice_name = i.name
					att.arrear_slip = 1
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
					tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
					sc = tr/10
					att.total_amount = tr + sc 
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = amt[0]['amt']/att.cgst_payable
							sgst_payable_amount = amt[0]['amt']/att.sgst_payable
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = amt[0]['amt']/att.igst_payable
							att.igst_payable_amount = igst_payable_amount
							total = amt[0]['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()

@frappe.whitelist()
def revert_the_slip(doc,method):
	from_date = doc.start_date
	to_date = doc.end_date
	if doc.arrear_slip == 1:
		invoice = frappe.db.sql("""select * from `tabInvoice Name` where active = 1 and name = '%s' """%(doc.invoice_name),as_dict = True)
		for i in invoice:
			# frappe.errprint(i.name)
			if i.travel_allowance == 0:
				if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1}):
					att = frappe.new_doc("Monthly Invoice")
					att.from_date = from_date
					att.to_date = to_date
					att.arrear_slip = 1
					att.invoice_name = i.name
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 1 and docstatus = 1 """%(i.name,from_date,to_date),as_dict=1)[0]
					att.total_amount = amt['amt'] or 0
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
							sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = (amt['amt']*(att.igst_payable))/100
							att.igst_payable_amount = igst_payable_amount
							total = amt['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
				else:
					att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1})
					att.from_date = from_date
					att.to_date = to_date
					att.arrear_slip = 1
					att.invoice_name = i.name
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 1 and docstatus = 1  """%(i.name,from_date,to_date),as_dict=1)[0]
					att.total_amount = amt['amt'] or 0
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
							sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = (amt['amt']*(att.igst_payable))/100
							att.igst_payable_amount = igst_payable_amount
							total = amt['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
			else:
				if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1}):
					att = frappe.new_doc("Monthly Invoice")
					att.from_date = from_date
					att.to_date = to_date
					att.invoice_name = i.name
					att.arrear_slip = 1
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date = '%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
					tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
					sc = tr/10
					att.total_amount = tr + sc 
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = amt[0]['amt']/att.cgst_payable
							sgst_payable_amount = amt[0]['amt']/att.sgst_payable
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = amt[0]['amt']/att.igst_payable
							att.igst_payable_amount = igst_payable_amount
							total = amt[0]['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
				else:
					att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':1})
					att.from_date = from_date
					att.to_date = to_date
					att.invoice_name = i.name
					att.arrear_slip = 1
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
					tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
					sc = tr/10
					att.total_amount = tr + sc 
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = amt[0]['amt']/att.cgst_payable
							sgst_payable_amount = amt[0]['amt']/att.sgst_payable
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = amt[0]['amt']/att.igst_payable
							att.igst_payable_amount = igst_payable_amount
							total = amt[0]['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
	else:
		invoice = frappe.db.sql("""select * from `tabInvoice Name` where active = 1 and name = '%s' """%(doc.invoice_name),as_dict = True)
		for i in invoice:
			# frappe.errprint(i.name)
			if i.travel_allowance == 0:
				if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':0}):
					att = frappe.new_doc("Monthly Invoice")
					att.from_date = from_date
					att.to_date = to_date
					att.invoice_name = i.name
					att.arrear_slip = 0
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 0 and docstatus = 1 """%(i.name,from_date,to_date),as_dict=1)[0]
					att.total_amount = amt['amt'] or 0
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
							sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = (amt['amt']*(att.igst_payable))/100
							att.igst_payable_amount = igst_payable_amount
							total = amt['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
				else:
					att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':0})
					att.from_date = from_date
					att.to_date = to_date
					att.arrear_slip = 0
					att.invoice_name = i.name
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(total_payable_to_mvl)as amt from `tabSalary Slip` where  invoice_name = '%s' and start_date = '%s' and end_date = '%s' and arrear_slip = 0 and docstatus = 1 """%(i.name,from_date,to_date),as_dict=1)[0]
					att.total_amount = amt['amt'] or 0
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = (amt['amt']*(att.cgst_payable))/100
							sgst_payable_amount = (amt['amt']*(att.sgst_payable))/100
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = (amt['amt']*(att.igst_payable))/100
							att.igst_payable_amount = igst_payable_amount
							total = amt['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
			else:
				if not frappe.db.exists("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_slip':0}):
					att = frappe.new_doc("Monthly Invoice")
					att.from_date = from_date
					att.to_date = to_date
					att.arrear_slip = 0
					att.invoice_name = i.name
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
					tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
					sc = tr/10
					att.total_amount = tr + sc 
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = amt[0]['amt']/att.cgst_payable
							sgst_payable_amount = amt[0]['amt']/att.sgst_payable
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = amt[0]['amt']/att.igst_payable
							att.igst_payable_amount = igst_payable_amount
							total = amt[0]['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
				else:
					att = frappe.get_doc("Monthly Invoice",{'invoice_name':i.name,'from_date':from_date,'to_date':to_date,'arrear_Slip':0})
					att.from_date = from_date
					att.to_date = to_date
					att.invoice_name = i.name
					att.arrear_slip = 0
					att.other_state = i.other_state
					att.hsnsac_code = frappe.get_value("Invoice Name",{'name':i.name},['hsn__tax_code'])
					att.invoicing_date = datetime.datetime.now()
					att.company = frappe.get_value("Invoice Name",{'name':i.name},['company'])
					amt = frappe.db.sql("""select sum(transport_allowance) as amt  from `tabAttendance and OT Register` where invoice_name_for_travel_allowance ='%s' and start_date = '%s' and end_date ='%s' and docstatus = 1 """%(i.name,from_date,to_date),as_dict= True)
					tr = amt[0]['amt'] if amt and amt[0].get('amt') is not None else 0
					sc = tr/10
					att.total_amount = tr + sc 
					if att.total_amount != 0:
						if i.other_state == 0:
							att.cgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['cgst_payable'])
							att.sgst_payable = frappe.get_value("Invoice Name",{'name':i.name},['sgst_payable'])
							cgst_payable_amount = amt[0]['amt']/att.cgst_payable
							sgst_payable_amount = amt[0]['amt']/att.sgst_payable
							att.cgst_payable_amount = cgst_payable_amount
							att.sgst_payable_amount = sgst_payable_amount
							total = amt[0]['amt'] + cgst_payable_amount + sgst_payable_amount
						else:
							att.igst_payable = frappe.get_value("Invoice Name",{'name':i.name},['igst_payable'])
							igst_payable_amount = amt[0]['amt']/att.igst_payable
							att.igst_payable_amount = igst_payable_amount
							total = amt[0]['amt'] + igst_payable_amount
						rounded_number = round(total, 2)
						# frappe.errprint(amt['amt'])
						# frappe.errprint(sgst_payable_amount)
						# frappe.errprint(cgst_payable_amount)
						# frappe.errprint(rounded_number)	
						att.total = rounded_number
						value_str = str(rounded_number)
						two_digits = value_str[-2:]
						if '.' in two_digits:
							last_two_digits = value_str[-1:] + '0'
						else:
							last_two_digits = value_str[-2:]
						# frappe.errprint(last_two_digits)
						# frappe.errprint(att.name)
						if  51 > int(last_two_digits) > 0 :
							att.add_on_status = "(Decrease -)"
							rounded_down = math.floor(att.total)
							att.add_on = att.total - rounded_down
							att.roundup = rounded_down
						elif 100 > int(last_two_digits) > 50 :
							att.add_on_status = "(Increase +)"
							rounded_up = math.ceil(att.total)
							att.add_on = rounded_up - att.total 
							att.roundup = rounded_up
						elif int(last_two_digits) == 0 :
							att.add_on_status = ''
							att.add_on = ''
							att.roundup = total
					else:
						att.total = 0
						att.cgst_payable_amount = 0
						att.sgst_payable_amount = 0
						att.igst_payable_amount = 0
					att.save(ignore_permissions=True)
					frappe.db.commit()
