// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Payable to MVL Report Against INV List"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Payroll From Date"),
			"fieldtype": "Date",
			"default": "",
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"end_date",
			"label": __("Payroll End Date"),
			"fieldtype": "Date",
			"default": "",
			"reqd": 1,
			"width": "100px"
		},

	]
};
