// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Invoice", {
// 	refresh(frm) {

// 	},
// });small_business_accounting

frappe.ui.form.on('Invoice', {
	onload(frm) {
		if((!frm.doc.r_name)||(frm.doc.name.includes("new-sales"))){
		frappe.db.count('Invoice')
			.then(count => {
					var name = 'I' + String(count+6).padStart(5, '0');
					frm.set_value('r_name', name);
				});
			});
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
				size: 'large', // small, large, extra-large 
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

frappe.ui.form.on('Invoice', {
	calc_sum(frm) {
		calculate_sum(frm);
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
	if (discount > 1){
		discounted_sum = sum - discount;
	}
	else {
		discounted_sum = sum * (1 - discount);
	}
	frm.set_value('discounted_sum',discounted_sum);
	frm.save();
}


frappe.ui.form.on('Invoice', {
	discount(frm) {
		calculate_sum(frm);
	}
});



frappe.ui.form.on('Invoice', {
	create_invoice(frm) {
	    var notes;
	    if (!frm.doc.notes){
	        notes='';
	    }
	    else{
	        notes = frm.doc.notes;
	    }
	    var q_num = frm.doc.name;
        frappe.call({method:'t_money.t_money.doctype.invoice.invoice.Create_Invoice',
        args: {
        'q_num': q_num,
        'objective':"חשבונית עסקה מס'",
        'notes': notes
        }
        }).then(r => {
            location.reload();
            window.open(`${window.location.origin + r.message}`, '_blank').focus();
        });
	}
});

