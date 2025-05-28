# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Assets(Document):
	pass
	
	
@frappe.whitelist()
def del_frm(frm_name):
	fisc_year, loss_requested = frappe.db.get_value('Assets', frm_name, ['fiscal_year','loss_requested'])
	curr_val = frappe.db.get_value('Income Loss Report', fisc_year, 'asset_loss')
	doc = frappe.get_doc('Income Loss Report', fisc_year)
	doc.db_set('asset_loss', curr_val - loss_requested, commit=True)
	frappe.delete_doc('Assets', frm_name)
