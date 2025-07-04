# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Expenses(Document):
	pass



@frappe.whitelist()
def add_expenss(fisc_year, actual_sum, sum_var, ex_type, old_sum, old_actual_sum, old_type, old_when):
	type_dic = {'משרדיות ואחזקה':'office','הוצאות רכב':'car','ביטוח מקצועי והשתלמויות':'insurance','קבלני משנה':'subconturctors','נסיעות (תחב"ץ)':'transport'}
	sum_var = frappe.utils.flt(sum_var)
	actual_sum = frappe.utils.flt(actual_sum)
	old_sum = frappe.utils.flt(old_sum)
	old_actual_sum = frappe.utils.flt(old_actual_sum)
	ex_type = type_dic[ex_type]
#	If there is no Income loss report already for the specific year, create it.
	def create_doc(fisc_year):
		doc = frappe.new_doc("Income Loss Report")
		doc.insert(
			ignore_permissions=True,
			ignore_links=True, # ignore Link validation in the document
			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True # insert even if mandatory fields are not set
		)
		title = doc.get_title()
		frappe.rename_doc('Income Loss Report', title, fisc_year)
		doc.db_set("year", int(fisc_year), commit=True)
		return(doc)
	
	def add_it(fisc_year, ex_type,actual_sum,sum_var):
		if not frappe.db.exists("Income Loss Report", fisc_year):
			doc = create_doc(fisc_year)
			curr_val = 0.0
		else:
			doc = frappe.get_doc('Income Loss Report', fisc_year)
			curr_val = frappe.utils.flt(frappe.db.get_value('Income Loss Report', fisc_year, ex_type))
#	Add the relative price payed to the relevant expense type
		doc.db_set(ex_type, actual_sum + curr_val, commit=True)
		if ex_type == 'car':
#	adds the payments for car expenses to the "non-deductable car expenses"
			curr_val = frappe.utils.flt(frappe.db.get_value('Income Loss Report', fisc_year, 'car_non'))
			doc.db_set('car_non', sum_var + curr_val - actual_sum, commit=True)
	if not old_type == '':
		old_type = type_dic[old_type]
		if not old_actual_sum == 0.0:
			if not old_when == '': #User changed expense type & the price & the date of the invoice (different year)
				add_it(old_when, old_type,(-1) * old_actual_sum,(-1) * old_sum)
			else: #User changed expense type & the price on the invoice
				add_it(fisc_year, old_type,(-1) * old_actual_sum,(-1) * old_sum)
		else: #User changed expense type
			add_it(fisc_year, old_type,(-1) * actual_sum,(-1) * sum_var)
	elif not old_actual_sum == 0.0:
		if not old_when == '': #User changed the price & the date of the invoice (different year)
			add_it(old_when, ex_type,(-1) * old_actual_sum,(-1) * old_sum)
		else: #User changed the price on the invoice
			add_it(fisc_year, ex_type,(-1) * old_actual_sum,(-1) * old_sum)
	elif not old_when == '': #User changed the date of the invoice (different year)
		add_it(old_when, ex_type,(-1) * actual_sum,(-1) * old_sum)
	add_it(fisc_year, ex_type,actual_sum,sum_var)






































