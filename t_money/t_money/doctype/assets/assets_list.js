frappe.listview_settings['Assets'] = {

	onload: function (listview) {
		listview.page.add_inner_button(__("Button"), function () {
			console.log(listview.get_checked_items());
//			frappe.call({
//				method:'t_money.t_money.doctype.assets.assets.del_frm',
//				args: {
//					frm_name: frm.doc.name
//				}
//			});
//        .addClass("btn-warning").css({'color':'darkred','font-weight': 'normal'});
        // The .addClass above is optional.  It just adds styles to the button.
    });
}
}
