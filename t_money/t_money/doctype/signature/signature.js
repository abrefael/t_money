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


frappe.ui.form.on ("Signature",{
	onload(frm) {
		if (!(frm.doc.company_name)){
			var user_id = frappe.session.user;
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'User',
					name: user_id
				},
				callback: function (data) {
					frm.set_value("company_name",data.message.full_name);
				}
			});
		}
	}
});
