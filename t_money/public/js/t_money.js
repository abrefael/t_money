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
    Powered by 
<a href="https://frappeframework.com/homepage" target="_blank" rel="noopener">
	<img src="/assets/frappe/images/frappe-logo.png" alt="Frappe Framework" style="height: 58px" />
</a> </div>
    <div style="text-align:right; width: 50%; float: right;">
    Powered by 
<a href="https://frappeframework.com/homepage" target="_blank" rel="noopener">
	<img src="/assets/frappe/images/frappe-logo.png" alt="Frappe Framework" style="height: 58px" />
    </a></div>
</div>
`;

function frappe_ready() {
    if (document.getElementById(FOOTER_ID)) return;
    console.log("trying");
    let footer = document.querySelector("footer");
    if (footer) {
        footer.innerHTML = FOOTER_HTML;
    }
}

    
$(document).on("page-change", () => {
    frappe_ready();
});

