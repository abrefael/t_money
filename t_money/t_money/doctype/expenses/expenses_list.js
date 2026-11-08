frappe.listview_settings['Expenses'] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("הצג שנה"), function () {
			filter_year(listview);
		})
		listview.page.add_inner_button(__("יצא לגליון נתונים"), function () {
			export_to_ods(listview);
		})
	}
};



var when;

function export_to_ods(listview){
	let filters = listview.filter_area.get()
	if (filters.length > 0) {
		filters = filters[0];
		filters[2] = filters[2].toLowerCase();
		filters = [filters[0],[[filters[1],filters[2],filters[3]]]];
		window.open('/api/method/t_money.api.export_excel?filters=' + encodeURIComponent(JSON.stringify(filters)));
	}
	else {
		let ref = window.location.href.split('/');
		window.open('/api/method/t_money.api.export_excel?filters=' + ref[ref.length -1]);
	}
};



function filter_year( listview )
{
	let curr_year = new Date().getFullYear();
	let d = new frappe.ui.Dialog({
		title: 'בחר שנה',
		fields: [
			{
				label: 'שנה לתצוגה',
				fieldname: 'year',
				fieldtype: 'Select',
				options: `${curr_year+1}
					${curr_year}
					${curr_year-1}
					${curr_year-2}
					${curr_year-3}
					${curr_year-4}
					${curr_year-5}
					${curr_year-6}
					${curr_year-7}`,
				default:curr_year
			}
		],
		size: 'small',
		primary_action_label: 'בחר',
		primary_action(values) {
			when = ['between',[String(values.year) + '-01-01',String(values.year) + '-12-31']];
			'["Between"%2C["' + String(values.year) + '-01-01"%2C"' + String(values.year) + '-12-31"]]';
			window.location.href = location.href.split("?")[0] + '?when=["' + when[0] + '"%2C["' + when[1][0] + '"%2C"' + when[1][0] + '"]]';
			d.hide();
		}
	});

	d.show();
}
