// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Expenses", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Expenses', {
	before_save(frm) {
	    frm.set_value('actual_sum', frm.doc.sum * frm.doc.impact);
		// your code here
	}
})
