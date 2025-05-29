//frappe.listview_settings['Assets'].onload = function(listview) {
//    refresh: function(listview) {
//        listview.page.add_inner_button("Button Name", function() {
//            ButtonFunction(listview);
//        });
//    }
// };

//function ButtonFunction(listview) {
//     console.log("ButtonFunction");
//     frappe.msgprint("ButtonFunction");
//}
////	let names=[];
////	$.each(listview.get_checked_items(), function(key, value) {
////		names.push(value.name);
////	});
////	if (names.length === 0) {
////		frappe.throw(__("No rows selected."));
////	}
////			
////	frappe.msgprint( names );
////}

frappe.listview_settings["Assets"] = {
    hide_name_column: true,
    add_fields: ["total_loss","name"],

    button: {
      show: function(doc) {
        return doc.reference_name;
      },
      get_label: function() {
        return __("Open", null, "Access");
      },
      get_description: function(doc) {
        return __("Open {0}", [
          `${__(doc.total_loss)}: ${doc.name}`
        ]);
      },
      action: function(doc) {
        frappe.set_route("Form", doc.total_loss);
      },
    }
}
