// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reports Dashboard', {
	refresh(frm){
		frm.disable_save();
	},
	download: function (frm) {
		if (frm.doc.reports == 'PF Report Text File') {
			var path = "mvl.mvl.doctype.reports_dashboard.pf_report.get_data_pf"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s'	
		}
		else if  (frm.doc.reports == 'Bank Remittance Report'){
			var path = "mvl.mvl.doctype.reports_dashboard.bank_remittance_report.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&arrear_slip=%(arrear_slip)s'
		}
		else if  (frm.doc.reports == 'Bank Remittance Report with Unit'){
			var path = "mvl.mvl.doctype.reports_dashboard.bank_remittance_report_with_unit.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&unit=%(unit)s&arrear_slip=%(arrear_slip)s'
			console.log(frm.doc.arrear_slip)
		}
		else if (frm.doc.reports == 'Bulk Salary Slip') {
			if(frm.doc.start_date && frm.doc.end_date){
			frappe.call({
				method:"mvl.salary_print.enqueue_download_multi_pdf",
				args:{
					doctype:"Salary Slip",
					unit: frm.doc.unit,
					department:frm.doc.department,
					start_date: frm.doc.start_date,
					end_date: frm.doc.end_date,
					arrear_slip : frm.doc.arrear_slip	
				},
				callback(r){
					if(r){
						console.log(r)
					}
				}
			})
			}
		}
		else if (frm.doc.reports == 'Principal Employer Wise Salary Statement') {
			var path = "mvl.mvl.doctype.reports_dashboard.unitwise_salary_statement.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&arrear_slip=%(arrear_slip)s'
		}
		else if (frm.doc.reports == 'Principal Employer Wise Salary Statement - Retainer') {
			var path = "mvl.mvl.doctype.reports_dashboard.unitwise_salary_statement.download_retainer"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&arrear_slip=%(arrear_slip)s'
		}
		else if (frm.doc.reports == 'Monthly Invoice Report') {
			var path = "mvl.mvl.doctype.reports_dashboard.monthly_invoice_report.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s'
		}
		else if (frm.doc.reports == 'Monthly TDS Report') {
			var path = "mvl.mvl.doctype.reports_dashboard.monthly_tds_report.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&arrear_slip=%(arrear_slip)s'
		}
		else if (frm.doc.reports == 'ESI Report Excel File') {
			var path = "mvl.mvl.doctype.reports_dashboard.esi_report.download"
			var args = 'start_date=%(start_date)s&end_date=%(end_date)s&arrear_slip=%(arrear_slip)s'
		}
		else {
			frappe.msgprint('Fill all the Mandatory Fields to download')
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				start_date : frm.doc.start_date,
				end_date : frm.doc.end_date,
				unit : frm.doc.unit,
				arrear_slip :frm.doc.arrear_slip
			});
		}
		
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
				}
			}
		});
	}
});
