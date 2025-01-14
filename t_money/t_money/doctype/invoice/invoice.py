# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Invoice(Document):
	pass
	

@frappe.whitelist()
def Create_Invoice(q_num, objective, notes):
	import odfdo, json, os
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
	TARGET = q_num + ".odt"
	f_uri = frappe.db.get_single_value("Signature", "reupload")
	if f_uri == '' or f_uri is None:
		document = Document("frontend/public/templates/template.odt")
	else:
		if f_uri.split('/')[1] == 'files':
			document = cstr(frappe.local.site) + '/public/' + f_uri
	body = document.body
	doc = frappe.get_doc('Invoice', q_num)
	paragraph = Paragraph(doc.creation.strftime('%d/%m/%Y'), style="head_of_file")
	body.append(paragraph)
	title1 = Header(1, f"{objective}: {q_num}")
	body.append(title1)
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
		price = itm.price
		quant = itm.quant
		cost = price * quant
		row_number = populate_items(itm.item, itm.desc, f"{price:,.2f} ₪", str(quant), f"{cost:,.2f} ₪", row_number)
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
	row_number = populate_totals('סה"כ פטור ממע"מ',f"{total:,.2f}  ₪", row_number)
	row_number = populate_totals('מע"מ', "0.00", row_number)
	if total*100%100 > 0:
		row_number = populate_totals('עיגול אגורות',f"{total:,.0f}  ₪", row_number)
	row_number = populate_totals('סה"כ לתשלום',f"{total:,.0f}  ₪", row_number)
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
	if frappe.db.get_value('File',{'attached_to_name':'Signature'},'is_private') == 1:
		uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + frappe.db.get_single_value('Signature','sign_img'))
	else:
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
	frappe.db.set_value('Invoice', q_num,'attached_file', '/files/accounting/' + q_num + '.pdf')
	frappe.db.commit()

@frappe.whitelist()
def send_mail(recipient, subject, mail_text, q_num):
	import os
	f_url = 'frontend/public/files/accounting/' + q_num + '.pdf'
	doc = frappe.new_doc('File')
	f_name = f_url.split("/")[-1]
	doc.file_name = f_name
	file_url = "/files/accounting/" + f_name
	doc.file_url = file_url
	doc.insert()
	name = frappe.db.get_value("File", {"file_name":f_name},'name')
	frappe.db.set_value("File", name,'file_url','/files/accounting/' + f_name)
	frappe.db.set_value('Sales', q_num,'attached_file', file_url)
	frappe.db.commit()
	os.remove(f_url.replace("/accounting",""))
	frappe.sendmail(
		recipients=[recipient],
		sender="Yaft Ben Refael <yfatfrechter@gmail.com>",
		subject=subject,
		message=mail_text,
		attachments=[{"file_url": "/files/accounting/" + q_num + ".pdf"}],
		as_markdown=False,
		delayed=False
		)
