# Copyright (c) 2024, Alon Ben Refael and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Signature(Document):
	pass



@frappe.whitelist()
def build_template():
	from frappe import cstr
	final = 0
	discount_segment = ""
	origin = "לדוגמה"
	def save_new():
		from weasyprint import HTML
		tmp_path = 'assets/t_money/temp/' + TARGET
		HTML(string=receipt_data, base_url=".").write_pdf(tmp_path)
		return tmp_path
	
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
	q_num = signature_doc.initials + "00265"
	h_p = "55555555"
	discount = 0.2
	notes = "הערות: " + "כמה הערות לקבלה"
	items_data=""
	itms = [
			{
				'item': 'פריט אחת',
				'desc': 'פירוט בנוגע לפריט אחת',
				'quant': 2.0, 'price': 200.0
			},
			{
				'item': 'פריט שתיים',
				'desc': 'פירוט בנוגע לפריט שתיים',
				'quant': 1.0,
				'price': 100.0
			},
			{
				'item': 'פריט שלוש',
				'desc': 'פירוט בנוגע לפריט שלוש',
				'quant': 2.0,
				'price': 500.0
			}
		]
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
	template = open("assets/t_money/R_template", "r").read()
	receipt_data = template.format(
		date = '01/05/2028',
		q_num = q_num,
		email_add = email_add,
		logo_img = logo_img,
		signature = signature,
		sign_img = sign_img,
		company_name = company_name,
		phone_num = phone_num,
		op_num = op_num,
		origin = origin,
		client= "לקוח מספר 346",
		h_p = h_p,
		items_data = items_data,
		discount_segment = discount_segment,
		total = f"{total:,.2f}",
		final = f"{final:,.0f}",
		notes = notes,
		bank = "",
		pay_method = "מזומן",
		receipt_date = '01/05/2028',
		brench = "",
		account_num = "",
		reference = ""
	)
	TARGET = q_num + "(" + origin + ").pdf"
	f_url = save_new()
	return "/assets/t_money/temp/" + TARGET

