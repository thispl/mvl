// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Retirement Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.year_start(),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.year_end(),
			"reqd": 1,
			"width": "100px"
		},
	]
};
