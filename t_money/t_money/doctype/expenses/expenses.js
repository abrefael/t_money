// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Expenses", {
// 	refresh(frm) {

// 	},
// });

var old_sum = 0;
var old_type = '';
var old_when = '';
var old_actual_sum = 0;
var flag = false;

frappe.ui.form.on('Expenses', {
	before_save(frm) {
		if ((frm.is_new())||(flag)) {
	//Every expense has a precentage aknowladged by the IRS as deductable, thus the impact on the losses calculated.
			var sum_var = frm.doc.sum;
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
					"ex_type": frm.doc.type,
					"old_sum": old_sum,
					"old_type":old_type,
					"old_when":old_when,
					"old_actual_sum":old_actual_sum
				}
			});
	//Once Income Loss Report is updated, we need to reset global variables.
			old_sum = 0;
			old_type = '';
			old_when = '';
			old_actual_sum = 0;
			flag = false;
		}
	}
})


frappe.ui.form.on('Expenses', {
	sum(frm) {
		if (!frm.is_new()) {
			frappe.db.get_value('Expenses', frm.doc.name, ['sum','actual_sum']
			).then(r => {
				old_sum = r.message.sum;
				old_actual_sum = r.message.actual_sum;
				flag = true;
			 })
		}
	}
});


frappe.ui.form.on('Expenses', {
	when(frm) {
		if (!frm.is_new()) {
			frappe.db.get_value('Expenses', frm.doc.name, 'when'
			).then(r => {
				let when = r.message.when.split('-')[0];
				if (frm.doc.when != when){
					old_when = when;
					flag = true;
				}
			 })
		}
	}
});



frappe.ui.form.on('Expenses', {
	type(frm) {
		if (!frm.is_new()) {
			frappe.db.get_value('Expenses', frm.doc.name, 'type'
			).then(r => {
				old_type = r.message.type;
				flag = true;
			 })
		}
	}
});
