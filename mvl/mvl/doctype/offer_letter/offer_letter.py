# Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	get_link_to_form,
	getdate,
)
from dateutil.relativedelta import relativedelta


class OfferLetter(Document):
	pass
@frappe.whitelist()
def get_end_date(start_date, frequency):
        start_date = getdate(start_date)
        frequency = frequency.lower() if frequency else "yearly"  
        kwarg = get_frequency_kwargs(frequency)
        end_date = add_to_date(start_date, **kwarg) - relativedelta(days=1)
        return dict(end_date=end_date.strftime(DATE_FORMAT))
        
def get_frequency_kwargs(frequency_name):
    frequency_dict = {
        "yearly": {"years": 1},  # Adjusted for yearly frequency
        "monthly": {"months": 1},
        "fortnightly": {"days": 14},
        "weekly": {"days": 7},
        "daily": {"days": 1},
    }
    return frequency_dict.get(frequency_name, {})
