// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt




frappe.ui.form.on('Income Loss Report', {
	calc(frm) {
		var total_income = 0;
		var incoms = frm.doc.items;
//	Calculate the total incom from receipts.
		for (let i = 0; i < incoms.length; i++) {
			total_income += flt(incoms[i].sum);
		}
//	Calculate the total losses due to: expenses (office, car, subcontructors and insurenses)
//	plus the travel expenses and the losses on assets.
		var losses = flt(frm.doc.office) + flt(frm.doc.insurance) + flt(frm.doc.subconturctors) + flt(frm.doc.travel) + flt(frm.doc.transport) + flt(frm.doc.car) + flt(frm.doc.asset_loss);
//	Calculate the "רווח נקי לא מתואם", whatever that means...
		var net_non = total_income - losses;
//	Calculate the "רווח נקי מתואם", whatever that means...
		var net_adj = net_non + flt(frm.doc.car_non);
		frm.set_value('total_profit', total_income);
		frm.set_value('profit_pre', net_non);
		frm.set_value('profit_adj', net_adj);
		frm.refresh();
		frm.save();
	}
});
