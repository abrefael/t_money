# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Signature(Document):
	pass


@frappe.whitelist()
def update_template(f_uri):
	from frappe import cstr
	def check_the_file(f_uri):
		import odfdo
		try:
			odfdo.Document(cstr(frappe.local.site) + f_uri)
		except:
			return 1
	
	if not 'private' in f_uri:
		f_uri = '/public' + f_uri
	if check_the_file(f_uri) == 1:
		return('1')
	else:
		return('0')



@frappe.whitelist()
def build_template():
	import odfdo, json, os
	from datetime import datetime
	OUTPUT_DIR = cstr(frappe.local.site) + '/public/files/temp'
	q_num="DD00265"
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
	def save_new(document: Document, name: str, q_num):
		new_path = '/tmp/' + name
		document.save(new_path, pretty=True)
		os.makedirs((OUTPUT_DIR), exist_ok=True)
		os.system(f"/usr/bin/soffice --headless --convert-to pdf:writer_pdf_Export --outdir {OUTPUT_DIR} '{new_path}'")
		f_url = '/files' + new_path.split('.')[0] + '.pdf'
		return f_url
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
	TARGET = q_num + "(לדוגמה).odt"
	f_uri = frappe.db.get_single_value("Signature", "reupload")
	if f_uri == '' or f_uri is None:
		f_uri = "assets/t_money/template.odt"
	else:
		if f_uri.split('/')[0] != 'private':
			f_uri = cstr(frappe.local.site) + '/public' + f_uri
	document = Document(f_uri)
	body = document.body
	paragraph = (Paragraph('01/05/2028'), style="head_of_file")
	body.append(paragraph)
	title1 = Header(1, f"קבלה: {q_num}")
	body.append(title1)
	title1 = Header(2, f"עבור: לקוח מספר 346")
	body.append(title1)
	title1 = Header(2, f"ע.מ/ת.ז/ע\"ר: 55555555")
	body.append(title1)
	body.append(Paragraph(""))
	body.append(Paragraph(""))
	itms = [
			{
				'item': 'פריט אחת',
				'desc': 'פירוט בנוגע לפריט אחת',
				'quant': 2.0, 'price': 200.0
			},
			{
				'item': 'פריט שתיים',
				'desc': 'פירוט בנוגע לפריט שתיים',
				'quant': 1.0,
				'price': 100.0
			},
			{
				'item': 'פריט שלוש',
				'desc': 'פירוט בנוגע לפריט שלוש',
				'quant': 2.0,
				'price': 500.0
			}
		]
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
	high_price = 0
	most_impact = ''
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
	discount = 0.2
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
	row_number = populate_totals('מע"מ', "0.00", row_number)
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
	widths = ["3.5cm","3cm","1cm","1.43cm","2.94cm","2.93cm","2.2cm"]
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
	row.set_value(0, 'מזומן')
	row.set_value(1, '01/05/2028'))
	row.set_value(6, f"{total:,.0f}")
	table.set_row(1, row)
	row = Row()
	row.set_value(5, 'סה"כ שולם:')
	row.set_value(6, f"{total:,.0f}")
	table.set_row(2, row)
	table.set_span('A3:F3', merge=True)
	if frappe.db.get_value('File',{'attached_to_name':'Signature'},'is_private') == 1:
		uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + frappe.db.get_single_value('Signature','sign_img'))
	else:
		uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + '/public/' + frappe.db.get_single_value('Signature','sign_img'))
	image_frame = Frame.image_frame(
		uri,
		size=(
			str(frappe.db.get_single_value(
				'Signature',
				'width'
			)) +
			frappe.db.get_single_value(
				'Signature',
				'u_width'
			),
			str(frappe.db.get_single_value(
				'Signature',
				'height'
			)) +
			frappe.db.get_single_value(
				'Signature',
				'u_height'
			)
		),
		position=("0cm", "0cm"),
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
	f_url = save_new(document,TARGET,q_num)
	return f_url



































	from odfdo import (
		Cell,
		Frame,
		Document,
		Header,
		Paragraph,
		Row,
		Table,
		Style
	)
	import os
	from frappe import cstr
	f_uri = frappe.db.get_single_value("Signature", "reupload")
	if f_uri == '' or f_uri is None:
		f_uri = "frontend/public/templates/template.odt"
	else:
		if f_uri.split('/')[1] == 'files':
			f_uri = cstr(frappe.local.site) + '/public/' + f_uri
	document = Document(f_uri)
	e = document.styles.root.get_elements('office:master-styles')[0].get_elements('style:master-page')[0].get_elements('style:header')[0]
	i=0
	head_in_temp = e.children[i]
	while not isinstance(head_in_temp,Paragraph):
		i+= 1
		head_in_temp = e.children[i]
	head_in_temp.replace('HEADER',frappe.utils.get_fullname())
	i=0
	head_in_temp = e.children[i]
	while not isinstance(head_in_temp,Table):
		i+= 1
		head_in_temp = e.children[i]
	row = head_in_temp.rows[0]
	row.set_value('B',frappe.db.get_single_value('Signature','op_num'))
	head_in_temp.set_row(row.y, row)
	row = head_in_temp.rows[1]
	row.set_value('B',frappe.db.get_single_value('Signature','phone_num'))
	head_in_temp.set_row(row.y, row)
	row = head_in_temp.rows[2]
	row.set_value('B',frappe.db.get_single_value('Signature','email_add'))
	head_in_temp.set_row(row.y, row)
	document.save(pretty=True)
	os.system(f"/usr/bin/soffice --headless --convert-to pdf:writer_pdf_Export --outdir 'frontend/public/templates' '{f_uri}'")

