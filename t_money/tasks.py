import frappe
import datetime


def check_year():
	TODAY = datetime.date.today()
	if TODAY.month == 1:
		for doc in frappe.db.get_list("Assets", pluck='name')
			frappe.get_doc("Assets", doc).calc_assets()
