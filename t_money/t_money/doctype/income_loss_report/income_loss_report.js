// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt




frappe.ui.form.on('Income Loss Report', {
	calc(frm) {
		frappe.call({
			method: 't_money.t_money.doctype.income_loss_report.income_loss_report.get_data',
			args: {
				"fisc_year": frm.doc.year
			}
		}).then(r => {
			var travels = 0;
			frappe.db.get_value('Travels', {fiscal_year: frm.doc.year}, 'total')
			.then(r => {
				let values = r.message;
				if (values.length > 0){
					travels = values.reduce((partialSum, a) => partialSum + a, 0);
					frm.set_value('travel', travels);
					losses += travels;
				}
			})
			const EXPENSES = r.message[1];
			const asset_loss = r.message[2];
			const RECEIPT = r.message[3];
			const CAR_NON = r.message[0];
			var losses = 0;
			var total_income = 0;
			var car = 0;
			var insurance = 0;
			var office = 0;
			var subconturctors = 0;
			for (const key of Object.keys(EXPENSES)) {
				let val = EXPENSES[key];
				if (key == 'הוצאות רכב'){
					car = val;
				} else if (key == 'ביטוח מקצועי והשתלמויות'){
					insurance = val;
				} else if (key == 'משרדיות ואחזקה'){
					office = val;
				} else if (key == 'קבלני משנה'){
					subconturctors = val;
				}
				losses += val;
			}
			losses += travels;
			for (const key of Object.keys(RECEIPT)) {
				let row = frm.add_child("items");
				let val = RECEIPT[key];
				row.item = key;
				row.sum = val;
				refresh_field("items");
				total_income += val;
			}
			var net_non = total_income - losses - asset_loss;
			frm.set_value('asset_loss', asset_loss);
			frm.set_value('subconturctors',subconturctors);
			frm.set_value('office',office);
			frm.set_value('insurance',insurance);
			frm.set_value('car',car);
			frm.set_value('car_non', CAR_NON);
			frm.set_value('total_profit', total_income);
			frm.set_value('profit_pre', net_non);
			frm.set_value('profit_adj', total_income + net_non);
			frm.refresh();
			frm.save();
		});
	}
});
