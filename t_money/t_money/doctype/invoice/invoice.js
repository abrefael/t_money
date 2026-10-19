// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Invoice", {
// 	refresh(frm) {

// 	},
// });small_business_accounting



frappe.ui.form.on('Invoice', {
	onload_post_render(frm) {
		if (frm.doc.created){
			$('li a span:contains("⇧+Ctrl+D")').parent().hide();
		}
	}
});

frappe.ui.form.on('Invoice', {
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
						default: "חשבונית עסקה " + q_num
					},
					{
						label: 'תוכן',
						fieldname: 'mail_text',
						fieldtype: 'Text Editor',
						default: ''
					}
				],
				size: 'large',
				primary_action_label: 'שלח',
				primary_action(values) {
					values.q_num = q_num;
					console.log(values);
					frappe.call({method:'t_money.t_money.doctype.invoice.invoice.send_mail',
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
	before_save(frm) {
		if (! frm.doc.created){
			calculate_sum(frm);
		}
	}
});


function calculate_sum(frm){
	var items = frm.doc.item_list;
	var sum = 0;
	var discounted_sum = 0;
	var discount = frm.doc.discount;
	for (let i = 0; i < items.length; i++){
		let row = items[i];
		let quant = row.quant;
		let price = row.price;
		sum += quant * price;
	}
	frm.set_value('sum',sum);
	if (discount >= 1){
		discounted_sum = sum - discount;
	}
	else {
		discounted_sum = sum * (1 - discount);
	}
	frm.set_value('discounted_sum',discounted_sum);
}

frappe.ui.form.on('Invoice', {
	discount(frm) {
		calculate_sum(frm);
	}
});


frappe.ui.form.on('Receipt', {
	calc_sum(frm) {
		frm.save();
	}
});

frappe.ui.form.on('Invoice', {
	create_draft(frm) {
		build_invoice(frm,frm.doc.q_num,"טיוטא");
	}
});


function build_invoice(frm, q_num, origin){
	frappe.call({
		method:'t_money.t_money.doctype.invoice.invoice.Create_Invoice',
		args: {
			'q_num': frm.doc.name,
			'origin': origin
		}
		}).then(r => {
			let uri = window.location.origin + r.message;
			window.location.reload();
			window.open(uri, '_blank').focus();
		});
}



frappe.ui.form.on('Invoice', {
	create_invoice(frm) {
		if (frm.doc.caceled){
			frappe.throw(__('<p style="direction: rtl; text-align: right">זו חשבונית מבוטלת! אין להפיקה מחדש! נא לשכפל את החשבונית מתפריט "..." ולהפיק חשבונית חדשה.'));
			return;
		}
		build_invoice(frm,frm.doc.q_num,"מקור");
	}
});


frappe.ui.form.on('Invoice', {
	validate: function(frm) {
		if (frm.doc.caceled) {
			if (frm.is_new()){
				frm.set_value("caceled",0);
				frm.set_value("created",0);
				frm.refresh_field("canceled");
				frm.refresh_field("created");
			}
			else {
				frappe.throw(__('זו חשבונית מבוטלת! אין לשנותה!'));
			}
		}
		if (frm.doc.created) {
			if (frm.is_new()){
				frm.set_value("created",0);
			}
			else {
				frappe.throw(__('חשבונית זו כבר הופקה. אין לשנותה!'));
			}
		}
	}
});



frappe.ui.form.on('Invoice', {
	cancel_r(frm) {
		frappe.call({method:'t_money.t_money.doctype.invoice.invoice.cancel_invoice',
		args: {
		'q_num': frm.doc.name
		}
		}).then(r => {
			window.location(`${window.location.href}(מבוטלת)`);
		});
	}
});


