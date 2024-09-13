// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly PF Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.month_start(),
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
						frappe.query_report.set_filter_value('to_date', r.message);
						frappe.query_report.refresh();
					}
				})
			}
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.month_end(),
			"reqd": 1,
			"width": "100px",
			"read_only":1
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
