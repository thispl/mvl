# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class AttendanceandOTRegister(Document):
	pass

	def validate(self):
		frappe.errprint ("HI")
		date_str1 = self.start_date
		date_str2 = self.end_date
		formatted_string1 = date_str1.strftime("%Y-%m-%d")
		formatted_string2 = date_str2.strftime("%Y-%m-%d")

		date_obj1 = datetime.strptime(formatted_string1, "%Y-%m-%d")
		date_obj2 = datetime.strptime(formatted_string2, "%Y-%m-%d")
		date_difference = date_obj2 - date_obj1
		self.non_contribution_days = date_difference

