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
	if f_uri.split('/')[1] == 'files':
		f_uri = '/public/' + f_uri
	try:
		odfdo.Document(cstr(frappe.local.site) + f_uri)
	except:
		return 1