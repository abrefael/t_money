import json
import frappe
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime, date

@frappe.whitelist()
def export_excel(filters):
	filter_dict = json.loads(filters)
	doctype_name = filter_dict[0]
	if len(filter_dict) > 1:
		data = frappe.db.get_all(
			doctype_name,
			filters=filter_dict[1],
			fields=['*']
		)
	else:
		doctype_name_lst = doctype_name.split()
		for i in range(len(doctype_name_lst)):
			doctype_name_lst[i] = doctype_name_lst[i].capitalize()
		doctype_name = " ".join(doctype_name_lst)
		data = frappe.db.get_all(
				doctype_name,
				fields=['*']
			)
	wb = Workbook()
	ws = wb.active
	if data:
		headers = list(data[0].keys())
		ws.append(headers)
		for row in data:
			ws.append([
				v.isoformat() if isinstance(v, (datetime, date)) else v
				for v in row.values()
			])
	output = BytesIO()
	wb.save(output)
	output.seek(0)
	frappe.local.response['filecontent'] = output.getvalue()
	frappe.local.response['type'] = 'binary'
	frappe.local.response['filename'] = doctype_name + '.xlsx'


@frappe.whitelist()
def build(year):
	wb = Workbook()
	ws = wb.active
	ws.append([datetime.now().isoformat(), year])
	output = BytesIO()
	wb.save(output)
	output.seek(0)
	frappe.local.response['filecontent'] = output.getvalue()
	frappe.local.response['type'] = 'binary'
	frappe.local.response['filename'] = 'dlkjd.xlsx'
