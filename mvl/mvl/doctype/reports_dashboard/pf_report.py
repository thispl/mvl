# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import math
import frappe
import json
import requests
# import pandas as pd
import openpyxl
from six import BytesIO
from frappe.utils import gzip_decompress

@frappe.whitelist()

def get_data_pf():
    data = []
    name = frappe.db.get_value('Prepared Report', {'report_name': 'PF Report', 'status': 'Completed'}, 'name')
    attached_file_name = frappe.db.get_value(
        "File",
        {"attached_to_doctype": 'Prepared Report',
            "attached_to_name": name},
        "name",
    )
    attached_file = frappe.get_doc("File", attached_file_name)
    compressed_content = attached_file.get_content()
    # frappe.errprint(compressed_content)
    uncompressed_content = gzip_decompress(compressed_content)
    dos = json.loads(uncompressed_content.decode("utf-8"))
    result = ""  
    # frappe.errprint(dos)   
    frappe.log_error(title='do',message=dos['result'])
    for do in dos['result']:
        
        result += str(do['employee']) + "#~#" + str(do['employee_name']) + "#~#" + str(do['bank_account_number']) + "#~#" + str(do['ifsc_code']) + "#~#" + str(do['gross_pay']) + "#~#" + str(do['pf']) or 0
        # result += ''
    frappe.response["result"] = result
    frappe.response["type"] = "txt"
    frappe.response["doctype"] = "Salary Slip PF"
    return data

@frappe.whitelist()
def get_data_esi():
    data = []
    name = frappe.db.get_value('Prepared Report', {'report_name': 'ESI Report', 'status': 'Completed'}, 'name')
    attached_file_name = frappe.db.get_value(
        "File",
        {"attached_to_doctype": 'Prepared Report',
            "attached_to_name": name},
        "name",
    )
    attached_file = frappe.get_doc("File", attached_file_name)
    compressed_content = attached_file.get_content()
    uncompressed_content = gzip_decompress(compressed_content)
    dos = json.loads(uncompressed_content.decode("utf-8"))
    result = ""
    for do in dos['result']:
        result +=  str(do['employee']) + "#~#" + str(do['employee_name']) + "#~#" + str(do['bank_account_number']) + "#~#" + str(do['ifsc_code']) + "#~#" + str(do['gross_pay']) + "#~#" + str(do['esi_number']) + "#~#" + str(do['esi']) or 0
    frappe.response["result"] = result
    frappe.response["type"] = "txt"
    frappe.response["doctype"] = "Salary Slip ESI"

    return data