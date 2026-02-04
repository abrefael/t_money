// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

frappe.ui.form.on("Signature", {
	build(frm) {
		frappe.call({method:'t_money.t_money.doctype.signature.signature.build_template'
	}).then(r => {
			window.open(r.message, '_blank').focus();
		});
	}
});


