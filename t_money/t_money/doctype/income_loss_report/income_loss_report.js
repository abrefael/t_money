// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt




frappe.ui.form.on('Income Loss Report', {
	calc(frm) {
		var total_income = 0;
		var incoms = frm.doc.items;
//	Calculate the total incom from receipts.
		for (let i = 0; i < incoms.length; i++) {
			total_income += incoms[i].sum;
		}
//	Calculate the total losses due to: expenses (office, car, subcontructors and insurenses)
//	plus the travel expenses and the losses on assets.
		var losses = frm.doc.office + frm.doc.insurance + frm.doc.subconturctors + frm.doc.travel + frm.doc.transport + frm.doc.car + frm.doc.asset_loss;
//	Calculate the "רווח נקי לא מתואם", whatever that means...
		var net_non = total_income - losses;
//	Calculate the "רווח נקי מתואם", whatever that means...
		var net_adj = net_non + frm.doc.car_non;
		frm.set_value('total_profit', total_income);
		frm.set_value('profit_pre', net_non);
		frm.set_value('profit_adj', net_adj);
		frm.refresh();
		frm.save();
	}
});
