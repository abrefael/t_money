# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Sales(Document):
	pass

@frappe.whitelist()
def Create_Quotation(q_num):
	final = 0
	discount_segment = ""
	def save_new():
		from weasyprint import HTML
		from frappe.utils.file_manager import save_file
		import os
		tmp_path = 'assets/t_money/temp/' + TARGET
		HTML(string=receipt_data, base_url=".").write_pdf(tmp_path)
		with open(tmp_path, "rb") as f:
			content = f.read()
		pdf_f = save_file(
			fname = TARGET,
			content = content,
			dt = "Sales",
			dn = q_num,
			is_private = 0
		)
		os.remove(tmp_path)
		return pdf_f.file_url
	
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
		nonlocal discount_segment
		if discount > 1:
			final = total - discount
			disc = f"{discount:,.2f} ₪"
		elif discount > 0 and discount < 1:
			final = total * (1 - discount)
			disc = f"{discount*100:,.0f} %"
		else:
			final = total
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
		discount_segment = f"""
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
	
	def get_file_uri(uri):
		if uri:
			if "private/" in uri:
				return cstr(frappe.local.site) + uri
			else:
				return cstr(frappe.local.site) + "/public" + uri
		else:
			return ""
	
	signature_doc = frappe.db.get_singles_dict("Signature")
	company_name = signature_doc.company_name
	op_num = signature_doc.op_num
	phone_num = signature_doc.phone_num
	email_add = signature_doc.email_add
	logo_img = get_file_uri(signature_doc.logo_img)
	signature = signature_doc.signature.replace("\\n","<br>")
	sign_img = get_file_uri(signature_doc.sign_img)
	doc = frappe.get_doc('Sales', q_num)
	date = doc.creation.strftime('%d/%m/%Y')
	client = doc.client
	h_p = doc.h_p
	notes = doc.notes
	discount = doc.discount
	if len(notes) > 1:
		notes = "הערות: " + notes.replace("\\n","<br>")
	items_data=""
	itms = frappe.db.sql(f"SELECT * FROM `tabItem Child List` WHERE parent='{q_num}'",as_dict=1)
	total = 0
	high_price = 0
	most_impact = ''
	for itm in itms:
		prod = itm["item"]
		desc = itm["desc"]
		price = itm["price"]
		quant = itm["quant"]
		cost = price * quant
		if cost > high_price:
			high_price = cost
			most_impact = prod
		items_data += populate_items()
		total += cost
	receipt_date = doc.receipt_date.strftime('%d/%m/%Y')
	calc_discount()
	template = open("assets/t_money/Q_template", "r").read()
	receipt_data = template.format(
		date = date,
		q_num = q_num,
		client= client,
		h_p = h_p,
		items_data = items_data,
		discount_segment = discount_segment,
		total = f"{total:,.2f }",
		final = f"{final:,.0f}",
		notes = notes,
		logo_img = logo_img,
		op_num = op_num,
		company_name = company_name,
		signature = signature,
		sign_img = sign_img,
		phone_num = phone_num,
		email_add = email_add
	)
	TARGET = q_num + ".pdf"
	f_url = save_new()
	return f_url


@frappe.whitelist()
def send_mail(recipient, subject, mail_text, q_num):
	import os
	f_url = frappe.db.get_value('Sales', q_num,'attached_file')
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
