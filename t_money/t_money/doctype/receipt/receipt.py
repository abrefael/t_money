# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Receipt(Document):
	pass
	

@frappe.whitelist()
def Create_Receipt(q_num, origin, fisc_year):
	import os
	final = 0
	discount_segment = ""
	def save_new():
		from weasyprint import HTML
		from frappe.utils.file_manager import save_file
		tmp_path = 'assets/t_money/temp/' + TARGET
		HTML(string=html_string, base_url=".").write_pdf(tmp_path)
		with open(tmp_path, "rb") as f:
			content = f.read()
		pdf_f = save_file(
			fname = TARGET,
			content = content,
			dt = "Receipt",
			dn = q_num,
			is_private = 0
		)
		os.remove(tmp_path)
		return pdf_f.file_url
	
	def update_income_loss()
		if not frappe.db.exists("Income Loss Report", fisc_year):
		doc = frappe.new_doc("Income Loss Report")
		doc.title = fisc_year
		doc.insert(
			ignore_permissions=True,
			ignore_links=True, # ignore Link validation in the document
			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True # insert even if mandatory fields are not set
		)
		frappe.rename_doc("Income Loss Report",doc.get_title(), fisc_year)
		doc.db_set("year", int(fisc_year), commit=True)
	
	def populate_items():
		item = f"""
		<tr>
			<td>{prod}</td>
			<td>{description}</td>
			<td>{price:,.2f}</td>
			<td>{quantity:,.1f}</td>
			<td>{cost:,.2f} ₪</td>
		</tr>
		"""
		return (
			item.format(
				prod = prod,
				description = desc,
				price = val,
				quantity = quant,
				cost = cost,
			)
	
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
		<td class="two" >{final:,.0f ₪}</td>
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
	doc = frappe.get_doc('Receipt', q_num)
	date = doc.creation.strftime('%d/%m/%Y')
	client = doc.client
	h_p = doc.h_p
	notes = doc.notes
	discount = doc.discount
	calc_discount()
	if len(notes) > 1:
		notes = "הערות: " + notes.replace("\\n","<br>")
	items_data=""
	itms = frappe.db.sql(f"SELECT * FROM `tabItem Child List` WHERE parent='{q_num}'",as_dict=1)
	total = 0
	high_price = 0
	most_impact = ''
	for itm in itms:
		prod = itm.item
		desc = itm.desc
		price = itm.price
		quant = itm.quant
		cost = price * quant
		if cost > high_price:
			high_price = cost
			most_impact = prod
		items_data += populate_items()
		total += cost
	pay_method = doc.pay_method.split(' (')[0]
	reference = doc.reference
	receipt_date = doc.receipt_date.strftime('%d/%m/%Y')
	doc = frappe.get_doc('Clients', client)
	bank = doc.bank.split(' ')[0]
	template = open("assets/t_money/R_template", "r").read()
	receipt_data = template.format(
		date = date,
		q_num = q_num,
		origin = origin,
		client= client,
		h_p = h_p,
		items_data = items_data,
		discount_segment = discount_segment,
		total = f"{total:,.2f ₪}",
		final = f"{final:,.0f}",
		notes = notes,
		pay_method = pay_method,
		receipt_date = receipt_date,
		brench = doc.brench,
		account_num = doc.account_num,
		reference = reference
	)
	TARGET = q_num + "(" + origin + ").pdf"
	f_url = save_new()
	if origin == 'מקור':
		update_income_loss()
		doc.db_set('created', 1, commit=True)
		incoms = frappe.db.get_all("Income Child Table", {'parent':fisc_year},['item','sum'])
		for inc in incoms:
			if inc['item'] == most_impact:
				frappe.db.set_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum',final + frappe.utils.flt(inc['sum']))
				frappe.db.commit()
				return f_url
		doc = frappe.get_doc("Income Loss Report", fisc_year)
		doc.append("items", {
			"item": most_impact,
			"sum": total,
		})
		doc.save()
		frappe.db.commit()
	return f_url


@frappe.whitelist()
def cancel_receipt(q_num):
	frappe.db.set_value('Receipt', q_num, 'caceled', 1)
	frappe.db.commit()
	receipt_date,most_impact, total, r_name = frappe.db.get_value('Receipt', q_num, ['receipt_date','most_impact','total','attached_file'])
	fisc_year = receipt_date.year
	total = frappe.utils.flt(total)
	total = frappe.utils.flt(frappe.db.get_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum')) - total
	frappe.db.set_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum', total)
	frappe.db.commit()
	frappe.rename_doc('Receipt', q_num, q_num+'(מבוטלת)', merge=False)
	from pypdf import PdfWriter, PdfReader
	import os
	try:
		src_file = os.getcwd() + '/' + frappe.cstr(frappe.local.site) + "/public" + r_name
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
