# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Expenses(Document):
	pass



@frappe.whitelist()
def add_expenss(fisc_year, actual_sum, sum_var, ex_type):
	type_dic = {'משרדיות ואחזקה':'office','הוצאות רכב':'car','ביטוח מקצועי והשתלמויות':'insurance','קבלני משנה':'subconturctors','נסיעות (תחב"ץ)':'transport'}
#	If there is no Income loss report already for the specific year, create it.
	if not frappe.db.exists("Income Loss Report", fisc_year):
		doc = frappe.new_doc("Income Loss Report")
		doc.insert(
			ignore_permissions=True,
			ignore_links=True, # ignore Link validation in the document
			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True # insert even if mandatory fields are not set
		)
		title = doc.get_title()
		frappe.rename_doc('Income Loss Report', title, fisc_year)
#		doc.db_set("name",fisc_year)
		doc.db_set("year", int(fisc_year), commit=True)
	doc = frappe.get_doc('Income Loss Report', fisc_year)
	ex_type = type_dic[ex_type]
	curr_val = frappe.db.get_value('Income Loss Report', fisc_year, ex_type)
#	Add the relative price payed to the relevant expense type
	doc.db_set(ex_type, actual_sum, commit=True)
	if ex_type == 'car':
#	adds the payments for car expenses to the "non-deductable car expenses"
		curr_val = frappe.db.get_value('Income Loss Report', fisc_year, 'car_non')
		doc.db_set('car_non', sum_var + curr_val - actual_sum, commit=True)

