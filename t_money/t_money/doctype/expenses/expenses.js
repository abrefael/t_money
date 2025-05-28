// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Expenses", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Expenses', {
	before_save(frm) {
//Every expense has a precentage aknowladged by the IRS as deductable, thus the impact on the losses calculated.
		var sum_var = flt(frm.doc.sum);
		console.log(sum_var);
		var actual_sum = sum_var * frm.doc.impact;
//We need to update the Income Loss Report...
		frm.set_value('actual_sum', actual_sum);
		var when = frm.doc.when;
		when = when.split('-')[0];
		frappe.call({
			method: 't_money.t_money.doctype.expenses.expenses.add_expenss',
			args: {
				"fisc_year": when,
				"actual_sum": actual_sum,
				"sum_var": sum_var,
				"ex_type": frm.doc.type
			}
		})
	}
})
