frappe.listview_settings['Assets'] = {

	onload: function (listview) {
		listview.page.add_inner_button(__("Button"), function () {
			$.each(listview.get_checked_items(), function(key, value) {
				console.log(value.name);
				frappe.call({
					method:'t_money.t_money.doctype.assets.assets.del_frm',
					args: {
						frm_name: frm.doc.name
					}
				});
			});
		});
	}
}
