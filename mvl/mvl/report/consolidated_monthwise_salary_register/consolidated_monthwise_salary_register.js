// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consolidated Monthwise Salary Register"] = {
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
			"fieldname": "unit",
			"fieldtype": "Link",
			"options": "Unit",
			"label": __("Unit"),
			"width": "50px",
			// "reqd": 1,
		},
	]
};
