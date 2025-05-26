# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Expenses(Document):
	pass



@frappe.whitelist()
def add_expenss(fisc_year, actual_sum, sum_var, ex_type):
	type_dic = {"משרדיות ואחזקה":'office',}
	if not frappe.db.exists("Income Loss Report", fisc_year):
		doc.insert("Income Loss Report",
			fisc_year,
			ignore_permissions=True,
			ignore_links=True, # ignore Link validation in the document
			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True # insert even if mandatory fields are not set
		)
	curr_val = frappe.db.get_value('Income Loss Report', fisc_year, type_dic[ex_type])
	nex_val = curr_val + actual_sum
	






	fisc_year = str(fisc_year)
	expenses = frappe.db.get_list('Expenses',filters={'when': ['between', [fisc_year+'-01-01', fisc_year+'-12-31']]},fields=['type', 'sum', 'actual_sum'],as_list=True)
	ass_db = frappe.db.get_list('Assets',filters={'fiscal_year':int(fisc_year)},fields=['loss_requested'],as_list=True)
	asset = 0
	for itm in ass_db:
		asset += itm[0]
	receipts = frappe.db.get_list('Receipt',filters={'receipt_date': ['between', [fisc_year+'-01-01', fisc_year+'-12-31']],'caceled':0},fields=['most_impact', 'total'],as_list=True)
	ex_dic = {}
	car_non = 0
	for itm in expenses:
		val = itm[1]
		typ = itm[0]
		sum = itm[2]
		if typ in ex_dic:
			ex_dic[typ] += val
		else:
			ex_dic[typ] = itm[1]
		car_non = car_non + val - sum
	rec_dic = {}
	for itm in receipts:
		typ = itm[0]
		val = itm[1]
		if typ in rec_dic:
			rec_dic[typ] += val
		else:
			rec_dic[typ] = val
	db = [car_non,ex_dic, asset,rec_dic]
	return db

