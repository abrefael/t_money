frappe.listview_settings['Clients'] = {
		listview.page.add_inner_button(__("יצא לגליון נתונים"), function () {
			export_to_ods(listview);
		})
	}
};

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


