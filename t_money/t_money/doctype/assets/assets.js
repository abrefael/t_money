// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Assets", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Assets', {
	calculate(frm) {
		if ((!frm.doc.fiscal_year) || ((frm.doc.original_price == 0) && (frm.doc.canges_price == 0))){
			frappe.throw(__('יש לציין שנת כספים לחישוב וגם מחיר מקורי ו/או מחיר שינויים'));
			return;
		}
		if (frm.doc.total == 0){
			frm.set_value ('total', frm.doc.original_price + frm.doc.canges_price);
		}
		var prev_total_loss = frm.doc.total_loss;
		perform_calc(frm, prev_total_loss);
		frm.set_value ('prev_total_loss', prev_total_loss);
		frm.save();
	}
});

frappe.ui.form.on('Assets', {
	re_calc(frm) {
		var prev_total_loss = frm.doc.prev_total_loss;
		perform_calc(frm, prev_total_loss)
		frm.save();
	}
});


function perform_calc(frm, prev_total_loss){
	var purcahse_year = frm.doc.purchase_date.split('-')[0];
	if (frm.doc.fiscal_year == purcahse_year){
		var purchase_date = new Date(frm.doc.purchase_date);
		var start = new Date(purchase_date.getFullYear(), 0, 0);
		var diff = purchase_date - start;
		var oneDay = 1000 * 60 * 60 * 24;
		var day = Math.floor(diff / oneDay);
		frm.set_value ('loss_requested', frm.doc.total * (frm.doc.rate_loss / 100) * ((365-day) / 365));
	}
	else{
		frm.set_value ('loss_requested', frm.doc.total * frm.doc.rate_loss  / 100);
	}
	frappe.db.set_value(
		'Income Loss Report',
		String(frm.doc.fiscal_year),
		'asset_loss',
		frm.doc.loss_requested + frappe.db.get_value(
			'Income Loss Report',
			String(frm.doc.fiscal_year),
			'asset_loss')
		)
	frm.set_value('total_loss', frm.doc.loss_requested + prev_total_loss);
	frm.set_value('current_value', frm.doc.total - frm.doc.total_loss);
}


