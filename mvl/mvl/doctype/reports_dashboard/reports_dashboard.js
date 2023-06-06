// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reports Dashboard', {
	download: function (frm) {
		if (frm.doc.reports == 'PF Report Text File') {
			var path = "mvl.mvl.doctype.reports_dashboard.pf_report.get_data_pf"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s'	
		}
		if (frm.doc.reports == 'ESI Report Text File') {
			var path = "mvl.mvl.doctype.reports_dashboard.pf_report.get_data_esi"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s'	
		}
		else if  (frm.doc.reports == 'Bank Remittance Report'){
			var path = "mvl.mvl.doctype.reports_dashboard.bank_remittance_report.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&principal_employer=%(principal_employer)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				start_date : frm.doc.start_date,
				end_date : frm.doc.end_date,
			});
		}
	}
});
