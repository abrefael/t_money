// Check this: "https://github.com/frappe/frappe/tree/96c3b1565a6a34cb50450da4f7f0a7453a6ffa50/frappe/core/doctype/data_export"


let doct = "Expenses";
let columns = '{' + doct + ':["when","type","expense_name","actual_sum","supp"]}';
let filters = ["when", "Between", [year + "-01-01", year + "-12-31"]];
let file_type = "Excel";


const export_data = (frm) => {
	let get_template_url = "/api/method/frappe.core.doctype.data_export.exporter.export_data"; //need to change
	var export_params = () => {
		let columns = {};
		Object.keys(frm.fields_multicheck).forEach((dt) => {
			const options = frm.fields_multicheck[dt].get_checked_options();
			columns[dt] = options;
		});
		return {
			doctype: doct,
			select_columns: columns,
			filters: filters,
			file_type: file_type,
			template: false,
			with_data: 1,
			export_without_column_meta: true,
		};
	};

	open_url_post(get_template_url, export_params());
};

//import xlsxwriter
//
//workbook = xlsxwriter.Workbook("demo.xlsx")
//worksheet = workbook.add_worksheet()
//worksheet.set_column("A:A", 20)
//cell_format = workbook.add_format()
//cell_format.set_text_wrap()
//cell_format.set_align(center)
