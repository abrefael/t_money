// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Sales", {
// 	refresh(frm) {

// 	},
// });



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
        frappe.call({method:'small_business_accounting.%D7%94%D7%A0%D7%94%D7%97%D7%A9.doctype.sales.sales.Create_Quotation',
        args: {
        'q_num': q_num,
        'objective':"הצעת מחיר מס'",
        'notes': notes
        }
        }).then(r => {
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
