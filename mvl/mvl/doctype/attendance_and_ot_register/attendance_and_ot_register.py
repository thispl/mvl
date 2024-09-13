# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
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

class AttendanceandOTRegister(Document):
	pass

@frappe.whitelist()
def update_ncp(doc,method):
		tot = date_diff(doc.end_date, doc.start_date) + 1
		ncp = tot - doc.payment_days
		frappe.db.set_value("Attendance and OT Register",doc.name,"non_contribution_days",ncp)



	