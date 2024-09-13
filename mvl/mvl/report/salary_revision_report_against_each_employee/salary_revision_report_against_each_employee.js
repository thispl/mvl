// Copyright (c) 2024, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Revision Report against Each Employee"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"reqd": 1,
			"width": "100px",
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"label": __("Employee"),
			"width": "50px",
			// "reqd": 1,
		},
	]
};
