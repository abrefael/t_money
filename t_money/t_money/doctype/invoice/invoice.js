// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Invoice", {
// 	refresh(frm) {

// 	},
// });small_business_accounting

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
            window.open(`${window.location.origin}/files/accounting/${q_num}.pdf`, '_blank').focus();
        });
	}
});

