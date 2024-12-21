src_fldr = '../apps/small_business_accounting/apps'
dest_fldr = '/home/frappe/apps'
csv_file = '/asset_type_list.csv'

import frappe
import shutil, os, csv

def after_install():
	from getpass import getpass
	import subprocess
	frappe.db.sql("""
	INSERT
	INTO `tabCustom HTML Block`
	SET
		name='Project_Management',
		creation=NOW(),
		modified=NOW(),
		modified_by='Administrator',
		owner='Administrator',
		docstatus=0,
		private=0,
		html='<iframe src="/app/project-calendar/view/calendar" style="width:100%;height: 850px;"></iframe>',
		script='',
		style='';
	""")
	os.system("cp -rf '" + src_fldr + "' '" + dest_fldr + "'")
	file = open(dest_fldr + csv_file,'r')
	reader = csv.reader(file, delimiter=',')
	for row in reader:
		doc = frappe.new_doc('Asset Type List')
		type = row[0]
		doc.name = type
		doc.asset_type = type
		doc.percent = float(row[1])
		doc.insert()



def after_migrate():
	import filecmp
	if not filecmp.cmp(src_fldr + csv_file, dest_fldr + csv_file):
		os.system("cp -rf '" + src_fldr + csv_file + "' '" + dest_fldr + csv_file + "'")
		file = open(dest_fldr + csv_file,'r')
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
