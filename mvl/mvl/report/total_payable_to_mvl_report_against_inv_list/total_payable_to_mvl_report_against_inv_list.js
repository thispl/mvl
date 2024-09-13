// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Payable to MVL Report Against INV List"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Payroll From Date"),
			"fieldtype": "Date",
			// "default": "",
			"reqd": 1,
			"width": "100px",
			on_change: function () {
				var from_date = frappe.query_report.get_filter_value('from_date')
				frappe.call({
					method: "mvl.mvl.report.monthwise_salary_register.monthwise_salary_register.get_to_date",
					args: {
						from_date: from_date
					},
					callback(r) {
						frappe.query_report.set_filter_value('end_date', r.message);
						frappe.query_report.refresh();
					}
				})
			}
		},
		{
			"fieldname":"end_date",
			"label": __("Payroll End Date"),
			"fieldtype": "Date",
			// "default": "",
			"reqd": 1,
			"width": "100px",
			"read_only":1
		},

	]
};
