const FOOTER_ID = "footer_div";
const FOOTER_HTML = `
<div id="footer_div" style="
    width:100%;
    padding:6px 12px;
    font-size:12px;
    text-align:center;
    color:#6b7280;
    border-top:1px solid var(--border-color);
    background: var(--bg-color);
"><div style="text-align:left; width: 50%; float: left;">
Created by<br>
<a href="mailto:alonbr@bitum.co.il">
	<img src="/assets/t_money/images/a-logo.svg" alt="Alon Ben Refael"/>
</a> </div>
    <div style="text-align:right; width: 50%; float: right;">
    Powered by<br>
<a href="https://frappeframework.com/homepage" target="_blank" rel="noopener">
	<img src="/assets/frappe/images/frappe-logo.png" alt="Frappe Framework" style="height: 58px" />
    </a></div>
</div>
`;

function frappe_ready() {
	let footer;
	if (window.location.href.includes("view/calendar/")){
		footer = document.querySelector("footer");
		if (footer) {
			footer.innerHTML = "";
			return;
		}
	}
	if (document.getElementById(FOOTER_ID)) return;
	if (window.self !== window.top) return;
	footer = document.querySelector("footer");
	if (footer) {
		footer.innerHTML = FOOTER_HTML;
	}
}


$(document).on("page-change", () => {
	frappe_ready();
});





//$("#svg1").attr("transform", "rotate(0)")
//$("#svg1").attr("transform", "rotate(270)")
