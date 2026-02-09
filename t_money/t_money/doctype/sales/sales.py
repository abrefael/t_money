# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Sales(Document):
	pass


@frappe.whitelist()
def Create_Quotation(q_num):
	import os
	final = 0
	discount_segment = ""
	
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
	if notes:
		if len(notes) > 1:
			notes = "הערות: " + notes.replace("\\n","<br>")
		else:
			notes = ""
	else:
		notes = ""
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
		total += cost
	calc_discount()
	template = open("assets/t_money/Q_template", "r").read()
	receipt_data = template.format(
		date = date,
		q_num = q_num,
		client= client,
		h_p = h_p,
		op_num = op_num,
		items_data = items_data,
		company_name = company_name,
		discount_segment = discount_segment,
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
	f_url = "/files/" + TARGET
	from weasyprint import HTML
	pdf_bytes = HTML(string=receipt_data, base_url=".").write_pdf(os.getcwd() + "/" + cstr(frappe.local.site) + "/public/files/" + TARGET)
	file_doc = frappe.get_doc({
		"doctype": "File",
		"file_name": TARGET
	})
	file_doc.insert(ignore_permissions=True)
	file_doc.file_url = f_url
	file_doc.save()
	frappe.db.commit()
	file_doc.attached_to_doctype = "Receipt"
	file_doc.attached_to_name = q_num
	file_doc.save()
	frappe.db.commit()
	doc.db_set('attached_file', f_url, commit=True)
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
