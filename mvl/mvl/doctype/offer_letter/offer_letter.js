// Copyright (c) 2023, veeramayandi.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Offer Letter', {
	from_date(frm) {
		frappe.call({
			method: 'mvl.mvl.doctype.offer_letter.offer_letter.get_end_date',
			args: {
				frequency: "Yearly",
				start_date: frm.doc.from_date
			},
			callback: function (r) {
					if (r.message) {
						frm.set_value('to_date', r.message.end_date);
					}
				}
	}
		)}
});
