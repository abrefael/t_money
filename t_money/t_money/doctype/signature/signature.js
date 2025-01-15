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
			}).then(r => {
				if(r.message == '1'){
					frappe.warn('<p style="direction: rtl">סוג קובץ לא מתאים</p>','<p style="direction: rtl; text-align: right;">סוג הקובץ אינו מתאים. יש צורך בקובץ מסוג ODT או OTT. </p><p style="direction: rtl; text-align: right;">דוגמה לקובץ מתאים ניתן להוריד מכאן</p>',
					() => {
						window.open('https://github.com/abrefael/t_money/raw/refs/heads/main/t_money/public/template.odt', '_blank').focus();
					},
					'כאן'
					);
				}
			});
		}
	}
});
