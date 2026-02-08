// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Receipt", {
// 	refresh(frm) {

// 	},
// });small_business_accounting




frappe.ui.form.on('Receipt', {
	send_mail(frm) {
		frappe.db.get_value(
			'Clients',
			frm.doc.client,
			'email'
		).then(r =>{
			let email;
			if (!(r.message.email)){
				email = "";
			}
			else {
				email = r.message.email;
			}
			let q_num = frm.doc.name;
			let d = new frappe.ui.Dialog({
				title: 'פרטי שליחה',
				fields: [
					{
						label: 'שלח אל',
						default: email,
						fieldname: 'recipient',
						fieldtype: 'Data',
						options: "Email",
						reqd: 1
					},
					{
						label: 'נושא',
						fieldname: 'subject',
						fieldtype: 'Data',
						reqd: 1,
						default: "קבלה " + q_num
					},
					{
						label: 'תוכן',
						fieldname: 'mail_text',
						fieldtype: 'Text Editor',
						default: ''
					}
				],
				size: 'large', // small, large, extra-large 
				primary_action_label: 'שלח',
				primary_action(values) {
					values.q_num = q_num;
					console.log(values);
					frappe.call({method:'t_money.t_money.doctype.receipt.receipt.send_mail',
						args: values
						});
					d.hide();
				}
			});
			d.show();
		})
	}
});

frappe.ui.form.on('Receipt', {
	onload(frm) {
		if((!frm.doc.r_name)||(frm.doc.name.includes("new-receipt"))){
		frappe.db.count('Receipt')
			.then(count => {
				frappe.db.get_single_value('Signature','initials')
					.then(inits => {
						var name = inits + String(count+1).padStart(5, '0');
						frm.set_value('r_name', name);
						frm.set_value('caceled', 0);
					});
			});
		}
	}
});





frappe.ui.form.on('Receipt', {
	before_save(frm) {
		calculate_sum(frm);
	}
});

var sum_discount = 0;


frappe.ui.form.on('Receipt', {
	load_lst(frm) {
		var inv_lst = frm.doc.inv_lst;
		var quot_lst = frm.doc.quot_lst;
		var invs_n_quots=[];
		var N = inv_lst.length;
		if (N > 0){ 
			for (let i = 0; i < N; i++){
				invs_n_quots.push(inv_lst[i].inv);
			}
		}
		N = quot_lst.length;
		if (N > 0){ 
			for (let i = 0; i < N; i++){
				invs_n_quots.push(quot_lst[i].quot);
			}
		}
		N = invs_n_quots.length;
		console.log(N);
		if (N == 0){
			frappe.throw(__('קודם צריך לבחור הצעות מחיר ו/או חשבוניות עסקה'));
		}
		for (let i = 0; i < N; i++){
			var total_discounts = '<p style="direction: rtl; text-align: right">שימו לב!<p style="direction: rtl; text-align: right">';
			let itm = invs_n_quots[i];
			var dtype;
			var dtype_heb;
			if (itm[0] == 'Q'){
				dtype = 'Sales';
				dtype_heb = "הצעת מחיר ";
			}
			else{
				dtype = 'Invoice';
				dtype_heb = "חשבונית עסקה ";
			}
			frappe.model.with_doc(dtype, itm, function () {
				let source_doc = frappe.model.get_doc(dtype, itm);
				let src_lst = source_doc.item_list;
				let discount = source_doc.discount;
				if (N == 1){
					frm.set_value('discount', discount);
					frm.refresh_field('discount');
					sum_discount = discount;
				}
				else{
					if (discount > 1){
						total_discounts += '<p style="direction: rtl; text-align: right">' + dtype_heb + itm + ' כוללת הנחה בסך: ' + discount + ' ש"ח.';
					}
					else {
						total_discounts += '<p style="direction: rtl; text-align: right">' + dtype_heb + itm + ' כוללת הנחה בערך של ' + discount + '% מהסכום הכולל.';
					}
					frappe.msgprint({
						title: __('הנחה'),
						indicator: 'blue',
						message: __(total_discounts)
					});
				}
				for (let i = 0; i < src_lst.length; i++){
					var addChild = frm.add_child("item_list");
					addChild.item = src_lst[i].item;
					addChild.quant = src_lst[i].quant;
					addChild.price = src_lst[i].price;
					frm.refresh_field('item_list');
				}
			});
		}
	}
});

function calculate_sum(frm){
	var items = frm.doc.item_list;
	var sum = 0;
	var row_sum = 0;
	var highest_sum = 0;
	var discounted_sum = 0;
	var discount = frm.doc.discount;
	if (discount == 0){
		discount = sum_discount;
	}
	for (let i = 0; i < items.length; i++){
		let row = items[i];
		let quant = row.quant;
		let price = row.price;
		row_sum = quant * price;
		sum += row_sum;
		if (row_sum > highest_sum){
			frm.set_value("most_impact",row.item);
			refresh_field("most_impact");
			highest_sum = row_sum;
		}
	}
	if (discount > 1){
		discounted_sum = sum - discount;
	}
	else {
		discounted_sum = sum * (1 - discount);
	}
	frm.set_value('total',discounted_sum);
}

frappe.ui.form.on('Receipt', {
	discount(frm) {
		calculate_sum(frm);
	}
});


frappe.ui.form.on('Receipt', {
	calc_sum(frm) {
		calculate_sum(frm);
		frm.save();
	}
});



frappe.ui.form.on('Receipt', {
	create_draft(frm) {
		frm.save();
		var pay_method = frm.doc.pay_method;
		if (((pay_method != "מזומן")||(pay_method.includes("אפליקציה להעברת כסף")))&&(frm.doc.reference == "000")){
			frappe.msgprint({
				title: __('שימו לב'),
				indicator: 'green',
				message: __('יש לרשום מספר אסמכתא!')
			});
		}
		else {
			build_the_receipt(frm,'טיוטה',frm.doc.name);
		}
	}
});


function build_the_receipt(frm,origin,q_num){
	function call_Create_Receipt(frm){
		frappe.call({method:'t_money.t_money.doctype.receipt.receipt.Create_Receipt',
			args: {
				'q_num': q_num,
				'origin': origin,
				"fisc_year": when
			}
		}).then(r => {
			location.reload();
			window.open(`${window.location.origin + r.message}`, '_blank').focus();
		});
	}
	var items = frm.doc.item_list;
	var highest_sum = 0;
	var discount = frm.doc.discount;
	var when = frm.doc.receipt_date;
	when = when.split('-')[0];
	call_Create_Receipt(frm);
}




frappe.ui.form.on('Receipt', {
	creat_receipt(frm) {
		if (frm.doc.caceled){
			frappe.throw(__('<p style="direction: rtl; text-align: right">זו קבלה מבוטלת! אין להפיקה מחדש! נא לשכפל את הקבלה מתפריט "..." ולהפיק קבלה חדשה.'));
			return;
		}
		var pay_method = frm.doc.pay_method;
		if (((pay_method != "מזומן")||(pay_method.includes("אפליקציה להעברת כסף")))&&(frm.doc.reference == "000")){
			frappe.msgprint({
				title: __('שימו לב'),
				indicator: 'red',
				message: __('יש לרשום מספר אסמכתא!')
			});
			return;
		}
		var origin;
		var q_num = frm.doc.name;
		if (frm.doc.created){
			origin = 'העתק נאמן למקור';
			frappe.confirm('<p style="direction: rtl; text-align: right">קבלת מקור הופקה, האם להפיק עותק?<p style="direction: rtl; text-align: right">(בחירה ב-No תציג את הקבלה המקורית)',
			() => {
				build_the_receipt(frm,origin,q_num);
				return;
			}, () => {
				origin = 'מקור';
				window.open(`${window.location.origin}/files/${q_num}(${origin}).pdf`, '_blank').focus();
				return;
			});
		}
		else{
			origin = 'מקור';
			frm.save();
			build_the_receipt(frm,origin,q_num);
		}
	}
});


frappe.ui.form.on('Receipt', {
	validate: function(frm) {
		if (frm.doc.caceled) {
			frappe.throw(__('זו קבלה מבוטלת! אין לשנותה!'));
			validated = false;
		}
		if (frm.doc.created) {
			frappe.throw(__('קבלה זו כבר הופקה. אין לשנותה!'));
			validated = false;
		}
		let pay_method = frm.doc.pay_method;
		if ((pay_method == "העברה בנקאית") || (pay_method == "המחאה") || (pay_method == "כרטיס דביט")){
			client = frm.doc.client;
			frappe.db.get_value('Clients', client, ['bank','brench','account_num'])
			.then(r => {
				let values = r.message;
				if ((values.bank.length < 2) || (values.brench == 0) || (values.account_num == "00")){
					frappe.throw(__('<div style="direction: rtl; text-align: right">הוגדר אמצעי תשלום: ' + pay_method + ', אך חסרים נתוני חשבון בנק של לקוח.</div><br><a href="/app/clients/' + client + '">לחצו כאן</a> לתיקון'));
			validated = false;
				}
			})
		}
	}
});



frappe.ui.form.on('Receipt', {
	cancel_r(frm) {
		var when = frm.doc.receipt_date;
		when = when.split('-')[0];
		frappe.call({method:'t_money.t_money.doctype.receipt.receipt.cancel_receipt',
		args: {
		"fisc_year": when,
		'q_num': frm.doc.name
		}
		}).then(r => {
			location.reload();
			window.open(`${window.location.href}(מבוטלת)`, '_blank').focus();
		});
	}
});



frappe.ui.form.on('Receipt', {
	pay_method(frm) {
		var pay_method = frm.doc.pay_method;
		if ((pay_method != "מזומן")||(pay_method.includes("אפליקציה להעברת כסף"))){
			frappe.msgprint({
				title: __('שימו לב'),
				indicator: 'green',
				message: __('האם יש לרשום מספר אסמכתא?')
			});
		}
	}
});
