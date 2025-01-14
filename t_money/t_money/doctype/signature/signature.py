# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Signature(Document):
	pass


@frappe.whitelist()
def update_template(f_uri):
	import odfdo
	from frappe import cstr
	if not 'private' in f_uri:
		frappe.flags.mute_messages = True
		f_uri = '/public/' + f_uri
	try:
		odfdo.Document(cstr(frappe.local.site) + f_uri)
	except:
		pass




@frappe.whitelist()
def build_template():
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

