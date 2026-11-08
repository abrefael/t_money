import frappe


def create_pdf(data, doctype, doc_name, filename, template):
	
	from weasyprint import HTML
	from frappe.utils.file_manager import save_file
	data["style"] = get_asset(template, "css")
	temp = get_asset(template,"templates")
	temp = temp.format(**{**data, **collect_personal_data()})
	print (temp)
	attached_file = save_file(
		filename,
		HTML(
			string=temp,
			base_url="."
		).write_pdf(), doctype, doc_name, is_private=0)
	return attached_file.file_url


def populate_items(itm):
	price = itm["price"]
	quant = itm["quant"]
	item = f"""
	<tr>
		<td>{itm["item"]}</td>
		<td>{itm["desc"]}</td>
		<td>{price:,.2f}</td>
		<td>{quant:,.1f}</td>
		<td>{price * quant:,.2f} ₪</td>
	</tr>
	"""
	return item


def collect_personal_data():
	signature_doc = frappe.db.get_singles_dict("Signature")
	return {
		"company_name": signature_doc.company_name,
		"op_num": signature_doc.op_num,
		"phone_num": signature_doc.phone_num,
		"email_add": signature_doc.email_add,
		"logo_img": get_file_uri(signature_doc.logo_img),
		"signature": signature_doc.signature,
		"sign_img": get_file_uri(signature_doc.sign_img)
	}


def get_file_uri(uri):
	from frappe.utils import cstr
	if uri:
		if "private/" in uri:
			return frappe.get_site_path() + uri
		else:
			return frappe.get_site_path("public") + uri
	else:
		return ""


def calc_discount(discount, total):
	if discount > 1:
		disc = f"{discount:,.2f} ₪"
	elif discount > 0 and discount < 1:
		disc = f"{discount*100:,.0f} %"
	else:
		final = total
		return "", final
	if total*100%100 > 0:
		ag_round = f"""
<tr>
	<td class="one" >עיגול אגורות</td>
	<td class="two" >{total:,.0f } ₪</td>
</tr>
		"""
		final = float(f"{total:,.0f}")
	else:
		ag_round = ""
		return f"""
<tr>
	<td class="one" >הנחה</td>
	<td class="two" >{disc}</td>
</tr>
<tr>
	<td class="one" >סה"כ אחרי הנחה</td>
	<td class="two" >{total:,.2f}  ₪</td>
</tr>
{ag_round}
""", final


def collect_client_data(client, request):
	client_doc = frappe.get_doc('Clients', client)
	reply = {}
	for rqst in request:
		reply [rqst] = client_doc.get(rqst)
	return reply


def get_asset(asset,asset_type):
	
	if asset_type == "css":
		asset += ".css"
	asset = f"assets/t_money/{asset_type}/{asset}"
	return open(asset, "r").read()





