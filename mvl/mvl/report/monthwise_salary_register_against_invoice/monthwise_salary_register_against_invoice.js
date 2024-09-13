// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthwise Salary Register Against Invoice"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
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
						frappe.query_report.set_filter_value('to_date', r.message);
						frappe.query_report.refresh();
					}
				})
			}
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			// "default": "",
			"reqd": 1,
			"width": "100px",
			"read_only":1
		},
		{
			"fieldname": "invoice_name",
			"fieldtype": "Link",
			"options": "Invoice Name",
			"label": __("Invoice Name"),
			"width": "50px",
			get_query: () => {
				var invoice_name = frappe.query_report.get_filter_value('invoice_name');
				return {
					filters: {
						'active': 1
					}
				};
			}
		},
		{
			"fieldname": "invoice_name_for_travel_allowance",
			"fieldtype": "Link",
			"options": "Invoice Name",
			"label": __("Invoice Name  for Travel"),
			"width": "50px",
			get_query: () => {
				var invoice_name_for_travel_allowance = frappe.query_report.get_filter_value('invoice_name_for_travel_allowance');
				return {
					filters: {
						'active': 1
					}
				};
			}
		},
		{
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"label": __("Currency"),
			"default": erpnext.get_currency(frappe.defaults.get_default("Company")),
			"width": "50px",
			"read_only":1
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": "Mercantile Ventures Limited",
			"width": "50px",
			"read_only":1
		},
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default": "Draft",
			"width": "100px"
		}
	],
};
