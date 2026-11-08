# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from t_money.api.api import populate_items
from t_money.api.api import calc_discount
from t_money.api.api import collect_client_data
from t_money.api.api import create_pdf
from t_money.api.api import get_file_uri


class Receipt(Document):
	
	def autoname(self):
		self.name = frappe.db.get_single_value('Signature','initials') + "{:06d}".format(frappe.db.count('Receipt') + 1)
	
	def on_trash(self):
		if self.created:
			frappe.throw(
				title='שגיאה!',
				msg='אסור למחוק קבלה שהופקה!!'
			)



def collect_data(doc, origin):
	
	itms = frappe.db.sql(f"SELECT * FROM `tabItem Child List` WHERE parent='{doc.name}'",as_dict=1)
	notes = doc.notes
	if len(notes) > 1:
		notes = "הערות: " + notes
	return {
		"date": doc.creation.strftime('%d/%m/%Y'),
		"client": doc.client,
		"h_p": doc.h_p,
		"notes": notes,
		"discount": doc.discount,
		"sum": frappe.utils.flt(doc.sum),
		"total": frappe.utils.flt(doc.total),
		"pay_method": doc.pay_method,
		"reference": doc.reference,
		"inv_lst": doc.inv_lst,
		"quot_lst": doc.quot_lst,
		"origin": origin,
		"receipt_date": doc.receipt_date.strftime('%d/%m/%Y')
	}


ILR = "Income Loss Report"


@frappe.whitelist()
def Create_Receipt(q_num, origin, fisc_year):
	
	def get_year_doc(fisc_year):
		if frappe.db.exists(ILR, fisc_year):
			return frappe.get_doc(ILR, fisc_year)
		else:
			doc = frappe.new_doc(ILR)
			doc.insert(
				ignore_permissions=True,
				ignore_links=True, # ignore Link validation in the document
				ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
				ignore_mandatory=True # insert even if mandatory fields are not set
			)
			title = doc.get_title()
			doc = frappe.get_doc(ILR, frappe.rename_doc(ILR, title, fisc_year))
			doc.set("year", int(fisc_year))
			frappe.db.commit()
			return doc
	
	doc = frappe.get_doc('Receipt', q_num)
	data = collect_data(doc, origin)
	itms = frappe.db.sql(f"SELECT * FROM `tabItem Child List` WHERE parent='{q_num}'",as_dict=1)
	items_data=""
	for itm in itms:
		items_data += populate_items(itm)
	data["items_data"] = items_data
	data["discount_segment"], final = calc_discount(data["discount"], data["total"])
	data["final"] = final
	c_data = collect_client_data(data["client"],["bank", "brench", "account_num"])
	for key in c_data.keys():
		data[key] = c_data[key]
	data["bank"] = data["bank"].split(' ')[0]
	data["q_num"] = q_num
	f_url = create_pdf(data, "Receipt", q_num, q_num + "(" + origin + ").pdf", "Receipt")
	if origin == 'מקור':
		doc.db_set("attached_file", get_file_uri(f_url))
		doc.db_set('created', 1, commit=True)
		doc = get_year_doc(str(fisc_year))
		doc.total_profit = doc.total_profit + final
		doc.save()
		frappe.db.commit()
		if len(inv_lst) > 0:
			invs = {inv.inv for inv in inv_lst}
			client_doc.bills = [elm for elm in client_doc.bills if elm.inv not in invs]
			client_doc.debt -= sum([elm.final for elm in inv_lst])
			client_doc.save()
	return f_url


@frappe.whitelist()
def cancel_receipt(q_num):
	from pypdf import PdfWriter, PdfReader
	import os
	frappe.db.set_value('Receipt', q_num, 'caceled', 1)
	frappe.db.commit()
	receipt_date, total, r_name = frappe.db.get_value('Receipt', q_num, ['receipt_date','total','attached_file'])
	fisc_year = receipt_date.year
	total = frappe.utils.flt(total)
	doc = frappe.get_doc("ILR", str(fisc_year))
	doc.total_profit = doc.total_profit - total
	doc.save()
	frappe.rename_doc('Receipt', q_num, q_num+'(מבוטלת)', merge=False)
	try:
		src_file = get_file_uri(r_name)
		cancel_file = "assets/t_money/canceled.pdf"
		stamp = PdfReader(cancel_file).pages[0]
		writer = PdfWriter(clone_from=src_file)
		for page in writer.pages:
			page.merge_page(stamp, over=False)
		writer.write(src_file)
	except:
		pass

@frappe.whitelist()
def send_mail(recipient, subject, mail_text, q_num):
	import os
	f_url = frappe.db.get_value('Receipt', q_num,'attached_file')
	sender, sender_mail = frappe.db.get_list("Email Account", ['email_id','name'], filters = [["email_id", "NOT LIKE", "%example.com"]],as_list=True)[0]
	frappe.sendmail(
		recipients=[recipient],
		sender=sender + '<' + sender_mail + '>',
		subject=subject,
		message=mail_text,
		attachments=[{"file_url": f_url}],
		as_markdown=True,
		delayed=False
		)
