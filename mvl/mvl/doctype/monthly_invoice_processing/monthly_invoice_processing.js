// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Invoice Processing', {
	refresh: function(frm) {
		frm.disable_save()
	},
	process_invoice(frm){
		console.log("HI")
		frappe.call({
			"method": "mvl.mvl.doctype.monthly_invoice_processing.monthly_invoice_processing.process_invoice",
			"args":{
				"from_date" : frm.doc.start_date,
				"to_date" : frm.doc.end_date,
			},
			freeze: true,
			freeze_message: 'Processing Invoice....',
			callback(r){
				console.log(r.message)
				if(r.message == "ok"){
					frappe.msgprint("Invoice Created Successfully")
				}
			}
		})
	},
	start_date(frm){
		frappe.call({
			method: 'mvl.mvl.doctype.monthly_invoice.monthly_invoice.get_end_date',
			args: {
				frequency: "Monthly",
				start_date: frm.doc.start_date
			},
			callback: function (r) {
				console.log("HI")
				if (r.message) {
					frm.set_value('end_date', r.message.end_date);
					frm.set_df_property("end_date","read_only",1)
				}
			}
		});
	},
	
});
