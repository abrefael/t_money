frappe.ready(() => {
    console.log("working");
    const FOOTER_ID = "global-desk-footer";

    if (document.getElementById(FOOTER_ID)) return;

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
        ">
            Created by <a href="mailto:alonbr@pm.me">Alon Ben Refael</a> ·
            
                Powered by <a href="https://frappeframework.com/homepage" target="_blank" rel="noopener">Frappe Framework
            </a>
        </div>
    `;

    const observer = new MutationObserver(() => {
        const footer = document.querySelector("footer");
        if (footer && !document.getElementById(FOOTER_ID)) {
            footer.appendChild(footer_d);
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
});

