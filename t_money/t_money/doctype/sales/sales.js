// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Sales", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Sales', {
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
						"reqd": 1
					},
					{
						label: 'נושא',
						fieldname: 'subject',
						fieldtype: 'Data',
						"reqd": 1
					},
					{
						label: 'תוכן',
						fieldname: 'mail_text',
						fieldtype: 'Text Editor',
						default: ''
					}
				],
				size: 'small', // small, large, extra-large 
				primary_action_label: 'שלח',
				primary_action(values) {
					values.q_num = q_num;
					console.log(values);
					frappe.call({method:'t_money.t_money.doctype.sales.sales.send_mail',
						args: values
						});
					d.hide();
				}
			});
			d.show();
		})
	}
});

frappe.ui.form.on('Sales', {
	quotation(frm) {
	    var notes;
	    if (!frm.doc.notes){
	        notes='';
	    }
	    else{
	        notes = frm.doc.notes;
	    }
	    var q_num = frm.doc.name;
        frappe.call({method:'t_money.t_money.doctype.sales.sales.Create_Quotation',
        args: {
        'q_num': q_num,
        'objective':"הצעת מחיר מס'",
        'notes': notes
        }
        }).then(r => {
			location.reload();
            window.open(`${window.location.origin}/files/accounting/${q_num}.pdf`, '_blank').focus();
        });
	}
});


frappe.ui.form.on('Sales', {
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

frappe.ui.form.on('Sales', {
	discount(frm) {
		calculate_sum(frm);
	}
});



frappe.ui.form.on('Sales', {
	invoice(frm) {
	    var items = frm.doc.item_list;
	    var item_list = [];
		var sum = 0;
		var discounted_sum = 0;
		var discount = frm.doc.discount;
	    for (let i = 0; i < items.length; i++){
			let row = items[i];
			let quant = row.quant;
			let price = row.price;
			sum += quant * price;
	        item_list.push({
	            'item' : row.item,
	            'quant' : quant,
	            'price' : price
	        });
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
	    frappe.db.insert({
            doctype: 'Invoice',
            client: frm.doc.client,
            item_list: item_list,
            discount: frm.doc.discount,
			discounted_sum: discounted_sum,
			sum: sum,
            h_p: frm.doc.h_p
        }).then(function(doc) {
            window.open(`${window.location.origin}/app/${doc.doctype.toLowerCase()}/${doc.name}`, '_blank').focus();
        });
	}
});
