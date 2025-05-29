frappe.listview_settings['Assets'] = {

    onload: function (listview) {

        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Button"), function () {
                        console.log("Yes");
        })
//        .addClass("btn-warning").css({'color':'darkred','font-weight': 'normal'});
        // The .addClass above is optional.  It just adds styles to the button.
    }
};
