csv_file = 'assets/t_money/asset_type_list.csv'

import frappe
import shutil, os, csv

def after_install():
	doc = frappe.get_doc({
		"doctype":"Custom HTML Block",
		"title":"Project_Management",
		"name":"Project_Management",
		"html":'<iframe src="/app/project-calendar/view/calendar" style="width:100%;height: 850px;"></iframe>'
	})
	doc.insert(ignore_if_duplicate=True)
	frappe.db.set_value("Website Settings", None, "app_name", "T-Money")
	frappe.db.set_value("Website Settings", None, "show_footer_on_login", 1)
	frappe.db.set_value("Website Settings", None, "copyright", "Created by Alon Ben Refael")
	frappe.db.set_value("Website Settings", None, "footer_powered", 'Powered By <a href="https://frappeframework.com/homepage">Frappe Framework</a>')
	frappe.db.set_value("Desktop Icon", "T-Money", "logo_url","/assets/t_money/images/T-money-logo.svg")
	frappe.db.commit()
	file = open(csv_file, 'r')
	reader = csv.reader(file, delimiter=',')
	for row in reader:
		doc = frappe.new_doc('Asset Type List')
		type = row[0]
		doc.name = type
		doc.asset_type = type
		doc.percent = float(row[1])
		doc.insert(ignore_if_duplicate=True)



def after_migrate():
	frappe.db.set_value("Website Settings", None, "app_name", "T-Money")
	frappe.db.set_value("Website Settings", None, "show_footer_on_login", 1)
	frappe.db.set_value("Website Settings", None, "copyright", "Created by Alon Ben Refael")
	frappe.db.set_value("Website Settings", None, "footer_powered", 'Powered By <a href="https://frappeframework.com/homepage">Frappe Framework</a>')
	frappe.db.set_value("Desktop Icon", "T-Money", "logo_url","/assets/t_money/images/T-money-logo.svg")
	frappe.db.commit()
	file = open(csv_file, 'r')
	reader = csv.reader(file, delimiter=',')
	for row in reader:
		type = row[0]
		percent = float(row[1])
		try:
			doc = frappe.get_doc('Asset Type List', type)
		except:
			doc = frappe.new_doc('Asset Type List')
			doc.name = type
			doc.asset_type = type
			doc.percent = percent
			doc.insert()
		else:
			if not percent == doc.percent:
				doc.percent = percent
				doc.save()
