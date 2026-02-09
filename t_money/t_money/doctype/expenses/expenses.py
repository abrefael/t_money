# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Expenses(Document):
	pass






@frappe.whitelist()
def add_expenss(doc_name,fisc_year, actual_sum, sum_var, ex_type, old_sum, old_actual_sum, old_type, old_when):
	return (frappe.get_doc("Expenses", doc_name))
