// Copyright (c) 2024, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary for Specific Components against employee"] = {
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
		{
			"fieldname": "salary_component",
			"fieldtype": "Link",
			"options": "Salary Component",
			"label": __("Salary Component"),
			"width": "50px",
			"reqd": 1,
			"get_query": function() {
				return {
					"filters": {
						"need_to_check_the_report_separately": 1
					}
				};
			}
		},
	]
};
