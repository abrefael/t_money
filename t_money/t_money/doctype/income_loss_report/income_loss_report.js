// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt



frappe.ui.form.on('Income Loss Report', {
	copy_car(frm) {
		const FIELD_LST = ["car_desc", "car_producer", "car_model", "car_vol", "car_price_point", "car_lic", "car_no_of_months"];
		frappe.call({
			method:"frappe.client.get",
			args: {
				doctype: "Income Loss Report",
				name: String(frm.doc.year - 1)
			},
			callback: function(r) {
				const doc = r.message;
				const n = doc.new_car ? "new_" : "";
				if (!doc.car_desc){
					frappe.throw(__('לא קיים רכב עבור שנה שעברה'));
				}
				frm.set_value("car_milage_init", doc[n + "car_milage_end"]);
				FIELD_LST.forEach((fld) => {
					frm.set_value(fld, doc[n + fld]);
					frm.refresh_field(fld);
				});
			},
			error: function(err) {
				frappe.throw(__('דוח לא קיים עבור שנה שעברה'));
			}
		});
	}
});


frappe.ui.form.on('Income Loss Report', {
	onload_post_render(frm) {
		function build(frm) {
			console.log(frm.doc); //Build Income Loss Report file
		}
		$(frm.fields_dict.build_btn.wrapper).find('button').off('click').on('click', function() {
			build(frm);
		});
	}
});












