# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Travels(Document):
	pass

@frappe.whitelist()

def Create_Travel_Report(objective, lst_of_dest, expenses, trip_name):
	import odfdo, json, os
	OUTPUT_DIR = os.getcwd() + '/' + cstr(frappe.local.site) + '/public/files/accounting/'
	fullName = frappe.get_fullname
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
		make_table_cell_border_string,
	)
	total = 0
	
	def save_new(document: Document, name: str):
		new_path = OUTPUT_DIR + name
		document.save(new_path, pretty=True)
		os.system(f'/usr/bin/soffice --headless --convert-to pdf:writer_pdf_Export --outdir {OUTPUT_DIR} {new_path}')
	def draw_table(table):
		border = make_table_cell_border_string(thick="0.01cm", color="black")
		cell_style = create_table_cell_style(
			color="black",
			background_color=(210, 210, 210),
			border_right=border,
			border_left=border,
			border_bottom=border,
			border_top=border,
		)
		style_name = document.insert_style(style=cell_style, automatic=True)
		row = table.get_row(0)
		for cell in row.traverse():
			cell.style = style_name
			row.set_cell(x=cell.x, cell=cell)
			table.set_row(row.y, row)

	def empty_line():
		paragraph = Paragraph('')
		body.append(paragraph)

	def add_travel_dest_table(lst_of_dest):
		import datetime
		table = Table("Table")
		body.append(table)
		row = Row()
		row.set_values(["", "יעדי הנסיעה", "ימי שהייה עסקיים", "", ""])
		row_number = 0
		table.set_row(row_number, row)
		table.set_span((2, row_number, 4, row_number))
		row = Row()
		row.set_values(['', '', 'מתאריך', 'עד תאריך', 'סה"כ ימים'])
		row_number = 1
		table.set_row(row_number, row)
		for dest in lst_of_dest:
			row_number += 1
			row = Row()
			row.set_value(0, str(row_number - 1) + '.')
			row.set_value(1, dest[0])
			arrive = dest[1]
			left = dest[2]
			row.set_value(2, arrive)
			row.set_value(3, left)
			arrive_date = datetime.datetime.strptime(arrive, "%d-%m-%Y")
			left_date = datetime.datetime.strptime(left, "%d-%m-%Y")
			row.set_value(4, str((left_date - arrive_date).days))
			table.set_row(row_number, row)
			draw_table(table)

	def add_expens_table(expenses):
		global total
		table = Table("Table")
		body.append(table)
		row = Row()
		row.set_values(['הוצאות עבור', 'סכום ההוצאה במט"ח', 'סכום ההוצאה בש"ח'])
		row_number = 0
		table.set_row(row_number, row)
		row_number += 1
		for ex in expenses:
			row.set_value(0, ex)
			expense = expenses[ex]
			row.set_value(1, expenses[ex][0])
			row.set_value(2, expense[1])
			total += expense[1]
			table.set_row(row_number, row)
			row_number += 1
		row.set_value(0, 'סה"כ הוצאות')
		row.set_value(1, '')
		row.set_value(2, total)
		table.set_row(row_number, row)
		draw_table(table)

	document = Document("text")
	body = document.body
	document.delete_styles()
	STYLE_SOURCE = "/home/frappe/apps/travel_temp.odt"
	style_document = Document(STYLE_SOURCE)
	document.merge_styles_from(style_document)
	body = document.body
	paragraph = Paragraph("שם החברה/העסק: " + fullName)
	body.append(paragraph)
	paragraph = Paragraph("שם הנוסע: " + fullName)
	body.append(paragraph)
	paragraph = Paragraph("תפקיד: בעלים")
	body.append(paragraph)
	paragraph = Paragraph("מטרת הנסיעה: ")
	body.append(paragraph)
	paragraph = Paragraph(objective)
	body.append(paragraph)
	empty_line()
	add_travel_dest_table(json.loads(lst_of_dest))
	empty_line()
	add_expens_table(json.loads(expenses))
	empty_line()
	added_text='נא לצרף: חשבונית בגין רכישת כרטיסי טיסה , מלונות, פרוספקטים, חשבוניות יבוא/יצוא, כרטיסים לתערוכה, פרוט עסקאות שנחתמו כפועל יוצא מהנסיעה, פרוט שמות לקוחות/ספקים בחו"ל וכרטיסי ביקור.'
	paragraph = Paragraph(added_text)
	empty_line()
	empty_line()
	empty_line()
	uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + '/public/files/sign.png')
	image_frame = Frame.image_frame(
		uri,
		size=("2.2cm", "1cm"),
		position=("6cm", "10cm"),
		anchor_type = "as-char",
	)
	paragraph = Paragraph("", style="sign")
	paragraph.append(image_frame)
	body.append(paragraph)
	paragraph = Paragraph("__________", style="sign")
	body.append(paragraph)
	paragraph = Paragraph("חתימה", style="sign")
	body.append(paragraph)
	save_new(document, trip_name + '.odt')
	return total


@frappe.whitelist()
def add_travel_expenss(fisc_year, total):
#	If there is no Income loss report already for the specific year, create it.
	if not frappe.db.exists("Income Loss Report", fisc_year):
		doc = frappe.new_doc({"doctype":"Income Loss Report"})
		doc.title = fisc_year
		doc.insert(
			ignore_permissions=True,
			ignore_links=True, # ignore Link validation in the document
			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True # insert even if mandatory fields are not set
		)
		doc.db_set("year", int(fisc_year), commit=True)
	doc = frappe.get_doc('Income Loss Report', fisc_year)
	curr_val = frappe.db.get_value('Income Loss Report', fisc_year, 'travel')
#	Add the relative price payed to the relevant expense type
	doc.db_set('travel', curr_val + total, commit=True))














