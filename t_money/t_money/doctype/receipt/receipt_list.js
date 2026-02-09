frappe.listview_settings.Receipt = {
	onload(listview) {
		listview.page.add_inner_button("הפעל פילטר שנתי", () => filter_year());
	}
};

function filter_year()
{
const curr_year = new Date().getFullYear();
const YEARS = String(curr_year+1) + '\n' + String(curr_year) + '\n' + String(curr_year-1) + '\n' + String(curr_year-2) + '\n' + String(curr_year-3) + '\n' + String(curr_year-4) + '\n' + String(curr_year-5) + '\n' + String(curr_year-6) + '\n' + String(curr_year-7);
let d = new frappe.ui.Dialog({
    title: 'בחר שנה',
    fields: [
        {
            label: 'שנה לתצוגה',
            fieldname: 'year',
            default: curr_year,
            fieldtype: 'Select',
            options: YEARS
        }
    ],
    size: 'small',
    primary_action_label: 'בחר',
    primary_action(values) {
        window.location.href = location.href.split("?")[0] + '?when=["Between"%2C["' + values.year + '-01-01"%2C"' + values.year + '-12-31"]]';
        d.hide();
    }
});

d.show();
}

