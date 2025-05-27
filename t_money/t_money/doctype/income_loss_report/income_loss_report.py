# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IncomeLossReport(Document):
	pass

#@frappe.whitelist()
#def get_data(fisc_year):
#	fisc_year = str(fisc_year)
#	expenses = frappe.db.get_list('Expenses',filters={'when': ['between', [fisc_year+'-01-01', fisc_year+'-12-31']]},fields=['type', 'sum', 'actual_sum'],as_list=True)
#	ass_db = frappe.db.get_list('Assets',filters={'fiscal_year':int(fisc_year)},fields=['loss_requested'],as_list=True)
#	asset = 0
#	for itm in ass_db:
#		asset += itm[0]
#	receipts = frappe.db.get_list('Receipt',filters={'receipt_date': ['between', [fisc_year+'-01-01', fisc_year+'-12-31']],'caceled':0},fields=['most_impact', 'total'],as_list=True)
#	ex_dic = {}
#	car_non = 0
#	for itm in expenses:
#		val = itm[1]
#		typ = itm[0]
#		sum = itm[2]
#		if typ in ex_dic:
#			ex_dic[typ] += val
#		else:
#			ex_dic[typ] = itm[1]
#		car_non = car_non + val - sum
#	rec_dic = {}
#	for itm in receipts:
#		typ = itm[0]
#		val = itm[1]
#		if typ in rec_dic:
#			rec_dic[typ] += val
#		else:
#			rec_dic[typ] = val
#	db = [car_non,ex_dic, asset,rec_dic]
#	return db

