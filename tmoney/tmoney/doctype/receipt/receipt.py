# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Receipt(Document):
	pass
	

@frappe.whitelist()
def Create_Receipt(q_num, origin, objective, notes):
	import odfdo, json, os
	from datetime import datetime
	OUTPUT_DIR = os.getcwd() + '/' + cstr(frappe.local.site) + '/public/files/accounting/'
								  
	from odfdo import (
		Cell,
		Frame,
		Document,
		Header,
		Paragraph,
		Row,
		Table,
		Style,
		create_table_cell_style,
	)
	def save_new(document: Document, name: str):
		new_path = OUTPUT_DIR + name
		document.save(new_path, pretty=True)
		os.system(f"/usr/bin/soffice --headless --convert-to pdf:writer_pdf_Export --outdir {OUTPUT_DIR} '{new_path}'")
	def populate_items(prod, desc, val, quant, cost, row_number):
		row = Row()
		row.set_value("A", prod)
		row.set_value("B", desc)
		row.set_value("C", val)
		row.set_value("D", quant)
		row.set_value("E", cost)
		row_number += 1
		table.set_row(row_number, row)
		return row_number
	def populate_totals(head, val, row_number):
		row = Row()
		row.set_value(column - 1, head)
		cell = Cell()
		cell.set_value(val)
		cell.style = style_name
		row.set_cell(column, cell)
		row_number += 1
		table.set_row(row_number, row)
		table.set_span((column - 4, row_number, column - 1, row_number), merge=True)
		return row_number
	TARGET = q_num + "(" + origin + ").odt"
	document = Document("/home/frappe/frappe-bench/apps/small_business_accounting/apps/template.odt")
	e = document.styles.root.get_elements('office:master-styles')[0].get_elements('style:master-page')[0].get_elements('style:header')[0]
	e.children[0].replace('HEADER',frappe.utils.get_fullname())
	table = e.children[1]
	row = table.rows[0]
	row.set_value('B',frappe.db.get_single_value('Signature','op_num'))
	table.set_row(row.y, row)
	row = table.rows[1]
	row.set_value('B',frappe.db.get_single_value('Signature','phone_num'))
	table.set_row(row.y, row)
	row = table.rows[2]
	row.set_value('B',frappe.db.get_single_value('Signature','email_add'))
	table.set_row(row.y, row)
	del e
	body = document.body
	doc = frappe.get_doc('Receipt', q_num)
	paragraph = Paragraph(doc.creation.strftime('%d/%m/%Y'), style="head_of_file")
	body.append(paragraph)
	title1 = Header(1, f"{objective}: {q_num}")
	body.append(title1)
	paragraph = Paragraph(origin, style="head_of_file")
	body.append(paragraph)
	title1 = Header(2, f"עבור: {doc.client}")
	body.append(title1)
	title1 = Header(2, f"ע.מ/ת.ז/ע\"ר: {doc.h_p}")
	body.append(title1)
	body.append(Paragraph(""))
	body.append(Paragraph(""))
	itms = frappe.db.sql(f"SELECT * FROM `tabItem Child List` WHERE parent='{q_num}'",as_dict=1)
	table = Table("Table")
	body.append(table)
	row = Row()
	row.set_values(['שם פריט/מק"ט', 'תיאור', 'מחיר', 'כמות', 'לתשלום'])
	table.set_row("A1", row)
	row_number = 0
	cell_style = create_table_cell_style(
		color="black",
		padding_right="1mm"
	)
	style_name = document.insert_style(style=cell_style, automatic=True)
	total = 0
	for itm in itms:
		prod = itm.item
		desc = itm.desc
		price = itm.price
		quant = itm.quant
		cost = price * quant
		row_number = populate_items(prod, desc, f"{price:,.2f} ₪", str(quant), f"{cost:,.2f} ₪", row_number)
		total = total + cost
	cols = table.width
	column = cols - 1
	row = Row()
	row_number += 1
	table.set_row(row_number, row)
	table.set_span((0, row_number, 3, row_number))
	row_number = populate_totals('סה"כ',f"{total:,.2f}  ₪", row_number)
	discount = float(doc.discount)
	if discount > 0 and discount < 1:
		discount = discount*100
		row_number = populate_totals('הנחה (%)',f"{discount:,.0f}", row_number)
		total = float(total) *(1 - discount/100)
		row_number = populate_totals('סה"כ אחרי הנחה',f"{total:,.2f}  ₪", row_number)
	elif discount > 1:
		row_number = populate_totals('הנחה',f"{discount:,.2f}  ₪", row_number)
		total = float(total) - discount
		row_number = populate_totals('סה"כ אחרי הנחה',f"{total:,.2f}  ₪", row_number)
	row_number = populate_totals('סה"כ פטור ממע"מ',f"{total:,.2f} ₪", row_number)
	row_number = populate_totals('ממע"מ', "0.00", row_number)
	if total*100%100 > 0:
		row_number = populate_totals('עיגול אגורות',f"{total:,.0f}  ₪", row_number)
	row_number = populate_totals('סה"כ',f"{total:,.0f}  ₪", row_number)
	cell_style = create_table_cell_style(
		color="black",
		background_color=(210, 210, 210),
		padding_right="1mm"
	)
	style_name = document.insert_style(style=cell_style, automatic=True)
	row = table.get_row(0)
	for cell in row.traverse():
		cell.style = style_name
		row.set_cell(x=cell.x, cell=cell)
	table.set_row(row.y, row)
	widths = ["4cm","5.5cm","3cm","1.5cm","3cm"]
	i = 0
	for column in table.columns:
		col_style = Style("table-column" , width=widths[i])
		name = document.insert_style(style=col_style, automatic=True)
		i = i+1
		column.style = col_style
		table.set_column(column.x, column)
	table = Table("Table",width=7)
	body.append(Paragraph("שולם באמצעות:"))
	body.append(table)
	widths = ["3.5cm","3cm","1cm","1.43cm","2.94cm","2.93	cm","2.2cm"]
	i = 0
	for column in table.columns:
		col_style = Style("table-column" , width=widths[i])
		name = document.insert_style(style=col_style, automatic=True)
		column.style = col_style
		table.set_column(i, column)
		i = i+1
	row = Row()
	row.set_values(['אמצעי תשלום','תאריך','בנק','סניף','מס’ חשבון','אסמכתא','סכום (₪)'])
	table.set_row("A1", row)
	cell_style = create_table_cell_style(background_color="#eeeeee")
	style_name = document.insert_style(style=cell_style, automatic=True)
	for cell in row.traverse():
		cell.style = style_name
		row.set_cell(x=cell.x, cell=cell)
	table.set_row(row.y, row)
	row = Row()
	pay_m = doc.pay_method
	row.set_value(0, pay_m.split(' (')[0])
	row.set_value(1, doc.receipt_date.strftime('%d/%m/%Y'))
	client = frappe.get_doc('Clients', doc.client)
	if pay_m == "העברה בנקאית" or pay_m == "המחאה" or pay_m == "כרטיס דביט":
		bank = client.bank
		if not bank == "יש לבחור בנק":
			bank = bank.split(' ')[0]
			row.set_value(2, bank)
			row.set_value(3, client.brench)
			row.set_value(4, client.account_num)
	if not doc.reference == "000":
		row.set_value(5, doc.reference)
	row.set_value(6, f"{total:,.0f}")
	table.set_row(1, row)
	row = Row()
	row.set_value(5, 'סה"כ שולם:')
	row.set_value(6, f"{total:,.0f}")
	table.set_row(2, row)
	table.set_span('A3:F3', merge=True)
	uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + '/public/' + frappe.db.get_single_value('Signature','sign_img'))
	image_frame = Frame.image_frame(
		uri,
		size=("2.2cm", "1cm"),
		position=("6cm", "10cm"),
		anchor_type = "as-char",
	)
	if not notes == "":
		body.append(Paragraph(""))
		body.append(Paragraph('הערות:'))
		body.append(Paragraph(f"{notes}"))
	body.append(Paragraph(""))
	body.append(Paragraph(""))
	paragraph = Paragraph("", style="sign")
	paragraph.append_plain_text(frappe.db.get_single_value('Signature','signature'))
	body.append(paragraph)
	paragraph = Paragraph("", style="ltr")
	paragraph.append(image_frame)
	body.append(paragraph)
	save_new(document,TARGET)
	if origin == 'מקור':
		frappe.db.set_value('Receipt', q_num, 'created', 1)
		frappe.db.commit()


@frappe.whitelist()
def cancel_receipt(q_num):
	frappe.db.set_value('Receipt', q_num, 'caceled', 1)
	frappe.db.commit()
	frappe.rename_doc('Receipt', q_num, q_num+'(מבוטלת)', merge=False)
	from pypdf import PdfWriter, PdfReader
	import os
	try:
		OUTPUT_DIR = os.getcwd() + '/' + cstr(frappe.local.site) + '/public/files/'
		src_file = OUTPUT_DIR + "accounting/" + q_num + '(מקור).pdf'
		cancel_file = "/home/frappe/frappe-bench/apps/small_business_accounting/apps/canceled.pdf"
		stamp = PdfReader(cancel_file).pages[0]
		writer = PdfWriter(clone_from=src_file)
		for page in writer.pages:
			page.merge_page(stamp, over=False)
		writer.write(src_file)
	except:
		pass
