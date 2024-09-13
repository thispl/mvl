// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Arrear Salary Updation', {
	payment_days(frm) {
		// if(frm.doc.from_date && frm.doc.to_date){
		//     var pd = frm.doc.payment_days;
		//     var end = frappe.datetime.obj_to_str(frm.doc.to_date);
        //     var start = frappe.datetime.obj_to_str(frm.doc.from_date);
        //     var datediff = frappe.datetime.get_day_diff(end,start);
        //     console.log(datediff+1);
        //     var ncp = (datediff+1) - pd ;
		// 	frm.set_value("total_working_days",datediff+1);
        //     console.log(ncp);
        //     frm.set_value("ncp",ncp);
		// }
		frappe.call({
			method: "mvl.mvl.doctype.arrear_salary_updation.arrear_salary_updation.get_tott_ncp",
			args: {
				from_date: frm.doc.from_date,
				to_date: frm.doc.to_date,
				invoice_name: frm.doc.invoice_name,
				payment_days: frm.doc.payment_days,
				employee:frm.doc.employee,
				ba :frm.doc.revised_basic,
				hra :frm.doc.revised_house_rent_allowance,
				da :frm.doc.revised_dearness_allowance,
				spl :frm.doc.revised_special_allowance,
				wa :frm.doc.revised_washing_allowance,
				ma :frm.doc.revised_medical_allowance,
				ca :frm.doc.revised_conveyance_allowance,
			},
			callback(r) {
				if (r.message) {
					console.log(r.message)
					frm.set_value('ncp', r.message[0] )
					frm.set_value('total_working_days', r.message[1])
				}
			}
		})
	}
});
