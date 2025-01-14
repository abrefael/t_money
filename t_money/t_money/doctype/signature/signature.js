// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

frappe.ui.form.on("Signature", {
	build(frm) {
		frappe.call({method:'t_money.t_money.doctype.signature.signature.build_template'
        }).then(r => {
            window.open('/templates/template.pdf', '_blank').focus();
		});
	}
});


frappe.ui.form.on("Signature", {
	validate(frm) {
		f_uri = frm.doc.reupload;
		if (!(f_uri == '')){
			frappe.call({method:'t_money.t_money.doctype.signature.signature.update_template',
				args: {
				'f_uri': frm.doc.reupload
				},
				error: function(r) {
						frappe.throw(__('You need to use LibreOffice writer (.odt) or template (.ott) file.<br>I recommand you try to use the original file from: <a href="https://github.com/abrefael/t_money/raw/refs/heads/main/t_money/public/template.odt">here</a>'))
						validate = false;
				}
			});
		}
	}
});
