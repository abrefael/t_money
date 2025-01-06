// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

frappe.ui.form.on("Signature", {
	build(frm) {
		frappe.call({method:'t_money.t_money.doctype.signature.signature.build_template'
        }).then(r => {
            window.open(`/assets/t_money/template.pdf`, '_blank').focus();
		});
	}
});


frappe.ui.form.on("Signature", {
	reupload(frm) {
		frappe.call({method:'t_money.t_money.doctype.signature.signature.update_template',
		args: {
        'f_uri': frm.doc.reupload
        }
		}).then(r => {
            if (r.massage == 1){
				frappe.throw(__('You need to use LibreOffice writer (.odt) or template (.ott) file'))
			}
        });
	}
});
