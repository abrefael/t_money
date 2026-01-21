const FOOTER_ID = "t-money-desk-footer";
const footer_d = document.createElement("div");
footer_d.id = FOOTER_ID;
footer_d.innerHTML = `
<div style="
    width:100%;
    padding:6px 12px;
    font-size:12px;
    text-align:center;
    color:#6b7280;
    border-top:1px solid var(--border-color);
    background: var(--bg-color);
"><div style="text-align:left; width: 50%;">
    Created by <a href="mailto:alonbr@pm.me">Alon Ben Refael</a> <div>
    <div style="text-align:right; width: 50%;">
        Powered by <a href="https://frappeframework.com/homepage" target="_blank" rel="noopener">Frappe Framework
    </a></div>
</div>
`;

function frappe_ready() {
    if (document.getElementById(FOOTER_ID)) return;
    let footer = document.querySelector("footer");
    if (footer) {
        footer.appendChild(footer_d);
    }
}

    
$(document).on("page-change", () => {
    frappe_ready();
});

