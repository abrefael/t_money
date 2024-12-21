// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Item", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Asset Type List', {
	additional_information(frm) {
            const URL = 'https://www.nevo.co.il/law_html/law01/255_001.htm';
            window.open(URL, '_blank').focus();
	}
});
