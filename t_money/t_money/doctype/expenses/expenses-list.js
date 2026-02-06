frappe.listview_settings['Expenses'].onload = function(listview) {
    listview.page.add_action_item(__("הצג שנה"), function() {
    	filter_year( listview );
});
};

function filter_year( listview )
{
curr_year = new Date().getFullYear();
let d = new frappe.ui.Dialog({
    title: 'בחר שנה',
    fields: [
        {
            label: 'שנה לתצוגה',
            fieldname: 'year',
            fieldtype: 'select',
            options: 'curr_year+1\ncurr_year\ncurr_year-1\ncurr_year-2\ncurr_year-3\ncurr_year-4\ncurr_year-5\ncurr_year-6\ncurr_year-7'
        }
    ],
    size: 'small', // small, large, extra-large 
    primary_action_label: 'בחר',
    primary_action(values) {
        location.href + '?when=["Between"%2C["' + String(values) + '-01-01"%2C"' + String(values) + '-31-12"]]';
        d.hide();
    }
});

d.show();
}
