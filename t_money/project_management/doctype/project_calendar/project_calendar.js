// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Sessions Calendar", {
// 	refresh(frm) {

// 	},
// });



frappe.ui.form.on('Project Calendar', {
  start_timer(frm) {
    frm.set_value("start",frappe.datetime.get_datetime_as_string());
 	}
});


frappe.ui.form.on('Project Calendar', {
  end_timer(frm) {
    frm.set_value("end",frappe.datetime.get_datetime_as_string());
 	}
});


frappe.ui.form.on('Project Calendar', {
  go_back(frm) {
    history.back()
;
 	}
});
