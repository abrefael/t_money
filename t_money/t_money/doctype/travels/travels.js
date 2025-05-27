// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Travels", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Travels', {
	build_report(frm) {
		frm.save();
		var fiscal_year = 0;
		var dests = frm.doc.lst_of_dest;
		var N = dests.length;
		var trip_name = frm.doc.trip_name;
		trip_name = trip_name.replace(' ','_');
		if (N == 0){
		frappe.throw(__('נדרש יעד אחד לפחות'));
		return;
		}
		var dest_lst = "[";
		var year_flag = false;
		if (frm.doc.fiscal_year == 0){
			year_flag = true;
		}
		for (let i = 0; i < N; i++){
			let dest = dests[i];
			let left = dest.left;
			dest_lst += '["' + dest.dest.replace('"','\\"') + '","' + dest.arrive + '","' + left + '"] "';
			if (year_flag){
				let year = left.split('-')[0];
				if (fiscal_year < year) {
					fiscal_year = year;
					frm.set_value("fiscal_year",Number(fiscal_year));
					frm.refresh_feild("fiscal_year");
				}
			}
		}
		frappe.confirm('עלות הנסיעה הנוכחית ישוקללו לשנת המס:' + fiscal_year + 'ניתן לשנות זאת בשדה "שנה פיסקלית"\nנמשיך?',
		() => {
			console.log('continue');
		}, () => {
	return;
		})
		dest_lst = dest_lst.replace('"] ["','"],["');
		dest_lst += "]";
		var objective = frm.doc.objective;
		if (frm.doc.objective_more_I){
			objective += ' ' + objective_more_I;
		}
		if (frm.doc.objective_more_II){
			objective += ' ' + objective_more_II;
		}
		var expenses = frm.doc.expenses;
		N = expenses.length;
		if (N == 0){
			frappe.throw(__('שכחתם להוסיף הוצאות לרשימה...'));
			return;
		}
		var ex_lst = "{";
		for (let i = 0; i < N; i++){
			let ex = expenses[i];
			let expense = ex.expense;
			if (expense == 'אש"ל ללא קבלות'){
				expense += ' (' + frm.doc.no_rct + ' ימים)'
			}
			expense = expense.replace('"','\\"');
			let sum_matach = ex.sum_matach;
			if (sum_matach == 0.00) {
				sum_matach = '-';
			}
			else {
				sum_matach += ' ' + ex.matach;
			}
			ex_lst += "'" + expense + "':[" + expense.sum + ",'" + sum_matach + "'] ";
		}
		ex_lst = ex_lst.replace("'] '","'],'");
		ex_lst += "}";
	frappe.call({
			method:'t_money.t_money.doctype.travels.travels.Create_Travel_Report',
			args: {
				'objective': objective,
				'lst_of_dest': dest_lst,
				'expenses': ex_lst,
				'trip_name': trip_name
			}
	}).then(r => {
			let tot = Number(r.message)
			frm.set_value("total",tot);
			refresh_field("total");
//We need to update the Income Loss Report...
			frappe.call({
				method:'t_money.t_money.doctype.travels.travels.add_travel_expenss',
				args: {
					'fisc_year': String(fisc_year),
					'total': tot
				}
			})
			frm.save();
		window.open(`${window.location.origin}/files/accounting/${trip_name}.pdf`, '_blank').focus();
	});
	}
});


