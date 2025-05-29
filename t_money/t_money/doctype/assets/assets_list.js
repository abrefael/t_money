frappe.listview_settings['Assets'] = {

	onload: function (listview) {
		listview.page.add_inner_button(__("מחיקת חישוב פחת"), function () {
			$.each(listview.get_checked_items(), function(key, value) {
				let frm_name = value.name;
				frappe.db.get_value('Assets', frm_name, 'loss_requested');
					.then(r => {
						if (flt(r.message.loss_requested) > 0) {
							frappe.call({
								method:'t_money.t_money.doctype.assets.assets.del_frm',
								args: {
									frm_name: frm_name
								}
								callback: function() {
									listview.refresh();
								}
							})
						}
						else {
							frappe.db.delete_doc('Assets', frm_name);
							listview.refresh();
						}
					});
			});
		});
	}
}
