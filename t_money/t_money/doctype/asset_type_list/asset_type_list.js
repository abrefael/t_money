// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Item", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Asset Type List', {
	additional_information(frm) {
            const URL = 'https://mag.calltext.co.il/storage/8514/Misim%20Book2025.pdf#page=81';
            window.open(URL, '_blank').focus();
	}
});
