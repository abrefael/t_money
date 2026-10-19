// Copyright (c) 2024, Alon Ben Refael and contributors
// For license information, please see license.txt

const itms = [
	{
		'item': 'פריט אחת',
		'desc': 'פירוט בנוגע לפריט אחת',
		'quant': 2.0,
		'price': 200.0
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
];
const client= "לקוח מספר 346";
const h_p = "55555555";
const pay_method = "מזומן";
const receipt_date = "19/09/1983";
const origin = "מקור";
const notes = `
הערות:
<div class="ql-editor read-mode">
<p style="text-align:right" class="ql-direction-rtl">כמה הערות לקבלה.</p>
<p style="text-align:right" class="ql-direction-rtl">למשל: בהתאם לחשבונית עסקה מספר I000586</p>
</div>
`;
const html_render=`
	<style>
		.a4-preview-container {
			width: 210mm;
			min-height: 297mm;
			margin: 20px auto;
			padding: 20mm;
			background: white;
			box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
			box-sizing: border-box;
			font-family: "DejaVu Sans", sans-serif;
			direction: rtl;
			text-align: right;
			font-size: 12pt;
			position: relative;
		}
		.no_bo{
			border: none;
		}
		.a4-preview-header {
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			text-align: center;
			margin-top: 5mm;
		}
		.a4-preview-footer {
			position: absolute;
			bottom: 0;
			left: 0;
			right: 25mm;
			text-align: right;
			margin-bottom: 5mm;
			font-size: 9pt;
		}
		.a4-preview-container th,
		.a4-preview-container td {
			border: 1px solid #D2D2D2;
			padding: 6px;
			text-align: right;
		}
		.a4-preview-container th {
		background-color:#D2D2D2;
		}
		.a4-preview-container table {
			border-collapse: collapse;
			width: 100%;
			text-align:right;
		}
		.a4-preview-container thead {
			display: table-header-group;
		}
		.a4-preview-container tr {
			break-inside: avoid;
		}
		.head1 {
			font-size: 18pt;
			font-weight:bold;
			text-align: center;
		}
		.a4-preview-container h1 {
			font-size: 22pt;
		}
		.one{
			width:80%
		}
		.two{
			width:20%;
			text-align:left
		}
		#headding{
			text-align:center
		}
		.head_tbl{
			width:100%;
			border-style:none;
		}
		#about{
			font-size: 14pt;
			font-weight:bold;
		}
		#signature{
			text-align:left;
		}
	</style>
<div class="a4-preview-container">
<p class="head1">{company_name}</p>
<table class="head_tbl">
	<tr>
		<td style="border: none;">
			<table class="head_tbl">
				<tr><td style="border: none;">ע.פ.:</td><td style="border: none;">{op_num}</td></tr>
				<tr><td style="border: none;">מספר טלפון:</td><td style="border: none;">{phone_num}</td></tr>
				<tr><td style="border: none;">דואר אלקטרוני:</td><td style="border: none;">{email_add}</td></tr>
			</table>
		</td>
		<td style="width:15%;border: none;" ><img src="{logo_img}" style="width:80px;"></td>
	</tr>
</table>
<div id="headding">
<br>
${receipt_date}
<h1>קבלה מס': {q_num}</h1>
${origin}
</div>
<div id="about">
<br>
עבור: 
${client} <br><br>
ע.מ/ת.ז/ע"ר: 
${h_p}<br><br>
</div>
<br>
<table>
	<thead>
		<tr>
			<th style="width:20%;">שם פריט/מק"ט</th>
			<th style="width:35%;">תיאור</th>
			<th style="width:17%;">מחיר</th>
			<th style="width:8%;">כמות</th>
			<th class="two">לתשלום</th>
		</tr>
	</thead>
		<tr>
			<td>${itms[0].item}</td>
			<td>${itms[0].desc}</td>
			<td>${itms[0].price.toFixed(2)}</td>
			<td>${itms[0].quant.toFixed(1)}</td>
			<td>400.00</td>
		</tr>
		<tr>
			<td>${itms[1].item}</td>
			<td>${itms[1].desc}</td>
			<td>${itms[1].price.toFixed(2)}</td>
			<td>${itms[1].quant.toFixed(1)}</td>
			<td>100.00</td>
		</tr>
		<tr>
			<td>${itms[2].item}</td>
			<td>${itms[2].desc}</td>
			<td>${itms[2].price.toFixed(2)}</td>
			<td>${itms[2].quant.toFixed(1)}</td>
			<td>1000</td>
		</tr>
</table>
<table class="summ"><tr><td class="one" ></td>
		<td class="two" ></td></tr>
</table>
<table class="summ">
	<tr>
		<td class="one" >סה"כ</td>
		<td class="two" >1500 ₪</td>
	</tr>
	<tr>
		<td class="one" >הנחה</td>
		<td class="two" dir=ltr>20 %</td>
	</tr>
	<tr>
		<td class="one" >סה"כ אחרי הנחה</td>
		<td class="two" >1200 ₪</td>
	</tr>
	<tr>
		<td class="one" >סה"כ פטור ממע"מ</td>
		<td class="two" >1200 ₪</td>
	</tr>
	<tr>
		<td class="one" >מע"מ</td>
		<td class="two" >0.00</td>
	</tr>
	<tr>
		<td class="one" >סה"כ לתשלום</td>
		<td style="text-align:left;" >1200 ₪</td>
	</tr>
</table>${notes}<br>
שולם באמצעות
<table>
	<thead>
		<tr>
			<th style="width:20%;">אמצעי תשלום</th>
			<th style="width:18%;">תאריך</th>
			<th style="width:5%;">בנק</th>
			<th style="width:8%;">סניף</th>
			<th style="width:16%;">מס' חשבון</th>
			<th style="width:16%;">אסמכתא</th>
			<th style="width:17%;">סכום (₪)</th>
		</tr>
	</thead>
	<tr>
		<td>${pay_method}</td>
		<td>${receipt_date}</td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td class="two">1200</td>
	</tr>
</table>
<br>
<div id="signature">
	{signature}
	<img src="{sign_img}" style="height:50px; margin-top:-25px;">
</div>
	<div class="a4-preview-footer">
עמוד 1 מתוך 1
	</div>
</div>
`;


frappe.ui.form.on ("Signature",{
	refresh(frm) {
			let html = html_render
				.replace('{q_num}', ((frm.doc.initials + "00265") || ""))
				.replace('{op_num}',frm.doc.op_num || "")
				.replace('{company_name}',frm.doc.company_name || "")
				.replace('{phone_num}',frm.doc.phone_num || "")
				.replace('{email_add}',frm.doc.email_add || "")
				.replace('{sign_img}',frm.doc.sign_img || "")
				.replace('{signature}',frm.doc.signature || "")
				.replace('{logo_img}',frm.doc.logo_img || "");
			console.log(html);
			frm.set_df_property("sample_receipt", "options",html );
	}
});
