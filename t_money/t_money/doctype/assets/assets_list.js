frappe.listview_settings['Assets'].onload = function(listview) {
    refresh: function(listview) {
        listview.page.add_inner_button("Button Name", function() {
            ButtonFunction(listview);
        });
    }
 };

function test( listview )
{
    refresh: function(listview) {
        listview.page.add_inner_button("Button Name", function() {
            ButtonFunction(listview);
        });;
    }
//	let names=[];
//	$.each(listview.get_checked_items(), function(key, value) {
//		names.push(value.name);
//	});
//	if (names.length === 0) {
//		frappe.throw(__("No rows selected."));
//	}
//			
//	frappe.msgprint( names );
}
