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
	def save_new(document: Document, name: str, q_num):
		from weasyprint import HTML
		new_path = '/tmp/' + name
		document.save(new_path, pretty=True)
		os.makedirs((OUTPUT_DIR), exist_ok=True)
		os.system(f"/usr/bin/soffice --headless --convert-to pdf:writer_pdf_Export --outdir {OUTPUT_DIR} '{new_path}'")
		f_name = name.split('.')[0] + '.pdf'
		f_path = OUTPUT_DIR + '/' + f_name
		f_url = '/files/temp/' + f_name
		doc = frappe.new_doc('File')
		doc.file_url = f_url
		doc.file_name = f_name
		doc.is_private = 0
		doc.insert()
		frappe.db.commit()
		frappe.db.set_value('Receipt', q_num,'attached_file', doc.file_url)
		frappe.db.commit()
		os.remove(f_path)
		return doc.file_url
	
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
		global final
		global discount_segment
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
			final = final - final*100%100
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
	
	signature_doc = frappe.db.get_singles_dict("Signature")
	company_name = signature_doc.company_name
	op_num = signature_doc.op_num
	phone_num = signature_doc.phone_num
	email_add = signature_doc.email_add
	# logo_img = signature_doc.logo_img # <- Doesn't exist yet.
	signature = signature_doc.signature.replace("\\n","<br>")
	sign_img = signature_doc.sign_img #needs some luven
	doc = frappe.get_doc('Receipt', q_num)
	date = doc.creation.strftime('%d/%m/%Y')
	client = doc.client
	h_p = doc.h_p
	notes = doc.notes
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
	receipt_date = doc.receipt_date.strftime('%d/%m/%Y')
	# bank = doc.bank.split(' ')[0]  # <- Doesn't exist yet.
	# brench = doc.brench  # <- Doesn't exist yet.
	# account_num = doc.account_num  # <- Doesn't exist yet.
	# client = frappe.get_doc('Clients', client)
	
	from datetime import datetime
	OUTPUT_DIR = cstr(frappe.local.site) + '/public/files/temp'
	TARGET = q_num + "(" + origin + ").odt"
	if frappe.db.get_value('File',{'attached_to_name':'Signature'},'is_private') == 1:
		uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + frappe.db.get_single_value('Signature','sign_img'))
	else:
		uri = document.add_file(os.getcwd() + '/' + cstr(frappe.local.site) + '/public/' + frappe.db.get_single_value('Signature','sign_img'))
	image_frame = Frame.image_frame(
		uri,
		size=(
			str(frappe.db.get_single_value(
				'Signature',
				'width'
			)) +
			frappe.db.get_single_value(
				'Signature',
				'u_width'
			),
			str(frappe.db.get_single_value(
				'Signature',
				'height'
			)) +
			frappe.db.get_single_value(
				'Signature',
				'u_height'
			)
		),
		position=("0cm", "0cm"),
		anchor_type = "as-char",
	)
	if not notes == "":
		body.append(Paragraph(""))
		body.append(Paragraph('הערות:'))
		body.append(Paragraph(f"{notes}"))
	body.append(Paragraph(""))
	body.append(Paragraph(""))
	paragraph = Paragraph("", style="sign")
	paragraph.append_plain_text(frappe.db.get_single_value('Signature','signature'))
	body.append(paragraph)
	paragraph = Paragraph("", style="ltr")
	paragraph.append(image_frame)
	body.append(paragraph)
	f_url = save_new(document,TARGET,q_num)
	if origin == 'מקור':
		doc.db_set('created', 1, commit=True)
		incoms = frappe.db.get_all("Income Child Table", {'parent':fisc_year},['item','sum'])
		for inc in incoms:
			if inc['item'] == most_impact:
				frappe.db.set_value("Income Child Table", {'parent':fisc_year,'item':most_impact},'sum',total + frappe.utils.flt(inc['sum']))
				frappe.db.commit()
				return
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
