frappe.listview_settings['Assets'] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("מחיקת חישוב פחת"), function () {
			$.each(listview.get_checked_items(), function(key, value) {
				let frm_name = value.name;
				frappe.db.get_value('Assets', frm_name, 'loss_requested')
					.then(r => {
						if (flt(r.message.loss_requested) > 0) {
							frappe.call({
								method:'t_money.t_money.doctype.assets.assets.del_frm',
								args: {
									frm_name: frm_name
								},
								callback: function() {
									listview.refresh();
								}
							});
						}
						else {
							frappe.db.delete_doc('Assets', frm_name);
							setTimeout(() => {
								listview.refresh();
							}, 1000);
						}
					});
			});
		});
		const year = (new Date()).getFullYear();
		const assets_report_section =
`<div id="assets-report-section" class="frappe-card p-4 mb-3" dir="rtl" style="text-align: right;">
	<h4>דוחות פחת שנתיים (טופס 1342)</h4>
	<p>
	נכס - פריט שנרכש בעל ערך גבוה, הנועד לשימוש לאורך הרבה שנים (למשל: מחשב נייד).<br>
	ברשימה זו יש לציין את כל הנכסים שנרכשו ובשימוש מרגע פתיחת העסק.<br>
	הסכום אותו שילתם עבור הנכס מוכר לניכוי מבחינת מס הכנסה ע"י הגדרת חלק מסויים ממחירו ההתחלתי בכל שנה משנת הרכישה, עד שכל ערך הפריט הוכר למס.<br>
	ניתן לראות את רשימת הפריטים המוכרים למס ב<a href="https://mag.calltext.co.il/storage/8514/Misim%20Book2025.pdf#page=81" target="blank"><u>פרק ד', סעיף 17</u></a> של המדריך "דע זכויותיך וחובותיך" (נכון לשנת 2025).<br>
	בעת רכישת פריט ניתן להוסיפו לרשימה. המערכת מחשבת את הערך היחסי המוכר למס אחת לשנה ביום ה-1 בינואר.<br>
	במידה ופריט הוסף לאחר ה- 1 בינואר, יש לציין את פרטי הרכישה וללחוץ על חישוב ערכי הפחת בתוך טופס ההוספה.
	לאחר וידוא שכל הפריטים הרלוונטיים נמצאים, בעת הכנת הניירת הדרושה להגשה למס הכנסה, ניתן להפיק את דוח הפחת (טופס 1342) במסך זה.
	</p>
</div>
<div id="assets-report-prep" class="frappe-card p-4 mb-3" dir="rtl" style="text-align: right;">
נא לבחור שנת מס רלוונטית:
<select name="year" id="year">
	<option value="${year - 1}">${year - 1}</option>
	<option value="${year}">${year}</option>
</select>
<button class="btn btn-default ellipsis" onclick="window.open('/api/method/t_money.api.build?year=' + document.getElementById('year').value)"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-down" data-d-component="icon" style="color: rgb(0, 0, 0); font-size: 16px;"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path><path d="M14 2v4a2 2 0 0 0 2 2h4"></path><path d="M12 18v-6"></path><path d="m9 15 3 3 3-3"></path></svg> הפק דוח</button>
</div>
`;
		const $page = $('[data-page-route="List/Assets/List"]');
		if (!$page.children('#assets-report-section').length) {
			$page.children('.page-head').after(assets_report_section);
		}
	}
}



























