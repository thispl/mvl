// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Invoice', {
	from_date(frm) {
		frappe.call({
			method: 'mvl.mvl.doctype.monthly_invoice.monthly_invoice.get_end_date',
			args: {
				frequency: "Monthly",
				start_date: frm.doc.from_date
			},
			callback: function (r) {
				console.log("HI")
				if (r.message) {
					frm.set_value('to_date', r.message.end_date);
				}
			}
		});
	},
	refresh(frm) {
		if(!frm.doc.__islocal){
			frm.add_custom_button(__('Print Annexture'), function (){
				var path = "mvl.mvl.doctype.monthly_invoice.monthly_invoice.download"
				var args = 'from_date=%(from_date)s&to_date=%(to_date)s&invoice_name=%(invoice_name)s&name=%(name)s'
				if (path) {
					window.location.href = repl(frappe.request.url +
						'?cmd=%(cmd)s&%(args)s', {
						cmd: path,
						args: args,
						from_date : frm.doc.from_date,
						to_date : frm.doc.to_date,
						invoice_name : frm.doc.invoice_name,
						name : frm.doc.name
					});
				}
			})
		}
	}
});
