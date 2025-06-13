# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Receipt(Document):
	pass
	

@frappe.whitelist()
def Create_Receipt(q_num, origin, objective, fisc_year, notes):
	import os
	if not frappe.db.exists("Income Loss Report", fisc_year):
		doc = frappe.new_doc("Income Loss Report")
		doc.title = fisc_year
		doc.insert(
			ignore_permissions=True,
			ignore_links=True, # ignore Link validation in the document
			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True # insert even if mandatory fields are not set
		)
		frappe.rename_doc("Income Loss Report",doc.get_title(), fisc_year)
		doc.db_set("year", int(fisc_year), commit=True)
	import odfdo, json, os
	from datetime import datetime
	OUTPUT_DIR = cstr(frappe.local.site) + '/public/files/temp'
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
		os.makedirs(OUTPUT_DIR), exist_ok=True))
		os.system(f"/usr/bin/soffice --headless --convert-to pdf:writer_pdf_Export --outdir {OUTPUT_DIR} '{new_path}'")
		f_name = name.split('.')[0] + '.pdf'
		f_path = OUTPUT_DIR + '/' + f_name
		f_url = '/files/temp/' + f_name
		doc = frappe.new_doc('File')
		doc.file_url = f_url
		doc.file_name = f_name
		doc.is_private = 0
		doc.insert()
		frappe.db.set_value('Receipt', q_num,'attached_file', '/files/' + f_name)
		frappe.db.commit()
		os.remove(f_path)

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
	f_uri = frappe.db.get_single_value("Signature", "reupload")
	if f_uri == '' or f_uri is None:
		f_uri = "assets/template.odt"
	else:
		if f_uri.split('/')[1] == 'files':
			f_uri = cstr(frappe.local.site) + '/public/' + f_uri
	document = Document(f_uri)
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
	high_price = 0
	most_impact = ''
	for itm in itms:
		prod = itm.item
		desc = itm.desc
		price = itm.price
		quant = itm.quant
		cost = price * quant
		if cost > high_price:
			high_price = cost
			most_impact = prod
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
	save_new(document,TARGET,q_num)
	if origin == 'מקור':
		doc.db_set('created', 1, commit=True)
		doc.db_set('attached_file', '/files/' + q_num + "(" + origin + ").pdf", commit=True)
		incoms = frappe.db.get_all("Income Child Table", {'parent':fisc_year},['item','sum'])
		for inc in incoms:
			if inc['item'] == most_impact:
				frappe.db.set_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum',total + frappe.utils.flt(inc['sum']))
				frappe.db.commit()
				return
		doc = frappe.get_doc("Income Loss Report", fisc_year)
		doc.append("items", {
			"item": most_impact,
			"sum": total,
		})
		doc.save()
		frappe.db.commit()


@frappe.whitelist()
def cancel_receipt(q_num, fisc_year):
	frappe.db.set_value('Receipt', q_num, 'caceled', 1)
	frappe.db.commit()
	most_impact, total = frappe.db.get_value('Receipt', q_num, ['most_impact','total'])
	total = frappe.utils.flt(total)
	total = frappe.utils.flt(frappe.db.get_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum')) - total
	frappe.db.set_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum', total)
	frappe.db.commit()
	frappe.rename_doc('Receipt', q_num, q_num+'(מבוטלת)', merge=False)
	from pypdf import PdfWriter, PdfReader
	import os
	try:
		OUTPUT_DIR = os.getcwd() + '/' + cstr(frappe.local.site) + '/public/files/'
		src_file = OUTPUT_DIR + q_num + '(מקור).pdf'
		cancel_file = "assets/t_money/canceled.pdf"
		stamp = PdfReader(cancel_file).pages[0]
		writer = PdfWriter(clone_from=src_file)
		for page in writer.pages:
			page.merge_page(stamp, over=False)
		writer.write(src_file)
	except:
		pass
		
@frappe.whitelist()
def send_mail(recipient, subject, mail_text, q_num):
	import os
	f_url = frappe.db.get_value('Receipt', q_num,'attached_file')
	sender, sender_mail = frappe.db.get_list("Email Account", ['email_id','name'], filters = [["email_id", "NOT LIKE", "%example.com"]],as_list=True)[0]
	frappe.sendmail(
		recipients=[recipient],
		sender=sender + '<' + sender_mail + '>',
		subject=subject,
		message=mail_text,
		attachments=[{"file_url": f_url}],
		as_markdown=True,
		delayed=False
		)
