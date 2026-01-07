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
var ratio = cur_frm.doc.width/cur_frm.doc.height;
console.log([cur_frm.doc.width , cur_frm.doc.height]);

frappe.ui.form.on("Signature", {
	width(frm) {
		if (frm.doc.keep_ratio){
			frm.set_value("height",frm.doc.width*ratio);
		}
		else{
			ratio = frm.doc.width/frm.doc.height;
		}
	}
});

frappe.ui.form.on("Signature", {
	height(frm) {
		if (frm.doc.keep_ratio){
			frm.set_value("width",frm.doc.height/ratio)
		}
		else{
			ratio = frm.doc.width/frm.doc.height;
		}
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
