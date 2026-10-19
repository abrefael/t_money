# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.model.naming import getseries

class Invoice(Document):
	def autoname(self):
		self.name = "I" + "{:06d}".format(frappe.db.count('Invoice')+1)
	

def get_file_uri(uri):
	if uri:
		if "private/" in uri:
			return cstr(frappe.local.site) + uri
		else:
			return cstr(frappe.local.site) + "/public" + uri
	else:
		return ""


@frappe.whitelist()
def Create_Invoice(q_num, origin):
	import os
	final = 0
	discount_segment = ""
	def save_new():
		from weasyprint import HTML
		from frappe.utils.file_manager import save_file
		tmp_path = 'assets/t_money/temp/' + TARGET
		HTML(string=receipt_data, base_url=".").write_pdf(tmp_path)
		with open(tmp_path, "rb") as f:
			content = f.read()
		file_doc = frappe.new_doc("File")
		file_doc.file_name = TARGET
		file_doc.attached_to_doctype = "Receipt"
		file_doc.attached_to_name = q_num
		file_doc.is_private = 0
		file_doc.content = content
		file_doc.insert(ignore_permissions=True)
		os.remove(tmp_path)
		return file_doc.file_url
	
	def populate_items():
		item = f"""
		<tr>
			<td>{prod}</td>
			<td>{desc}</td>
			<td>{price:,.2f}</td>
			<td>{quant:,.1f}</td>
			<td>{cost:,.2f} ₪</td>
		</tr>
		"""
		return item
	
	def calc_discount():
		nonlocal final
		if discount > 1:
			disc = f"{discount:,.2f} ₪"
		elif discount > 0 and discount < 1:
			disc = f"{discount*100:,.0f} %"
		else:
			return ""
		if final*100%100 > 0:
			ag_round = f"""
	<tr>
		<td class="one" >עיגול אגורות</td>
		<td class="two" >{final:,.0f } ₪</td>
	</tr>
			"""
			final = float(f"{final:,.0f}")
		else:
			ag_round = ""
		return f"""
	<tr>
		<td class="one" >הנחה</td>
		<td class="two" >{disc}</td>
	</tr>
	<tr>
		<td class="one" >סה"כ אחרי הנחה</td>
		<td class="two" >{final:,.2f}  ₪</td>
	</tr>
	{ag_round}
		"""
	
	
	signature_doc = frappe.db.get_singles_dict("Signature")
	company_name = signature_doc.company_name
	op_num = signature_doc.op_num
	phone_num = signature_doc.phone_num
	email_add = signature_doc.email_add
	logo_img = get_file_uri(signature_doc.logo_img)
	signature = signature_doc.signature
	sign_img = get_file_uri(signature_doc.sign_img)
	doc = frappe.get_doc('Invoice', q_num)
	date = doc.creation.strftime('%d/%m/%Y')
	client = doc.client
	h_p = doc.h_p
	notes = doc.notes
	discount = doc.discount
	if len(notes) > 1:
		notes = "הערות: " + notes
	items_data=""
	itms = frappe.db.sql(f"SELECT * FROM `tabItem Child List` WHERE parent='{q_num}'",as_dict=1)
	total = 0
	for itm in itms:
		prod = itm["item"]
		desc = itm["desc"]
		price = itm["price"]
		quant = itm["quant"]
		cost = price * quant
		items_data += populate_items()
	total = frappe.utils.flt(doc.sum)
	final = frappe.utils.flt(doc.discounted_sum)
	template = open("assets/t_money/I_template", "r").read()
	receipt_data = template.format(
		date = date,
		q_num = q_num,
		origin = origin,
		client= client,
		h_p = h_p,
		op_num = op_num,
		items_data = items_data,
		company_name = company_name,
		discount_segment = calc_discount(),
		total = f"{total:,.2f}",
		final = f"{final:,.0f}",
		signature = signature,
		notes = notes,
		logo_img = logo_img,
		sign_img = sign_img,
		phone_num = phone_num,
		email_add = email_add
	)
	TARGET = q_num + "(" + origin + ").pdf"
	f_url = save_new()
	if origin == 'מקור':
		doc.db_set("attached_file", '/files' + f_url.split('/files')[1])
		doc.db_set('created', 1, commit=True)
		doc = frappe.get_doc("Clients", client)
		bill = frappe.new_doc("List of Invoices")
		bill.inv = q_num
		doc.bills.append(bill)
		doc.debt += final
		doc.save()
		frappe.db.commit()
	return f_url


@frappe.whitelist()
def cancel_invoice(q_num):
	from pypdf import PdfWriter, PdfReader
	import os
	frappe.db.set_value('Invoice', q_num, 'caceled', 1)
	frappe.db.commit()
	client, total, r_name = frappe.db.get_value('Invoice', q_num, ['client', 'total', 'attached_file'])
	total = frappe.utils.flt(total)
	client_doc = frappe.get_doc('Clients', client)
	client_doc.bills = [elm for elm in client_doc.bills if not elm.inv == q_num]
	client_doc.debt -= total
	client_doc.save()
	doc.save()
	frappe.rename_doc('Invoice', q_num, q_num+'(מבוטלת)', merge=False)
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
	f_url = frappe.db.get_value('Invoice', q_num,'attached_file')
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
