"""Content for the Managed WiFi environment sub-pages and the Smart Home
service sub-pages, plus the renderer that turns each spec into a page body.

Copy is drawn from the Managed WiFi brief (C06, C10-C12, C16, E4) and the
Smart Home brief (P04, P07-P10, P12, P21, Part 07 future-page specs), kept
to the same qualified, no-guarantee wording. Strings are HTML.
"""

# ----------------------------------------------------------- renderer ----
def _paras(ps, cls="cx-prose"):
    return f'<div class="{cls}">' + "".join(f"<p>{p}</p>" for p in ps) + "</div>"


def _aside(a):
    kind = a["kind"]
    if kind == "list":
        lis = "".join(f"<li>{i}</li>" for i in a["items"])
        note = f'<p style="margin-top: 14px;">{a["note"]}</p>' if a.get("note") else ""
        return (f'<div class="cx-card"><p class="cx-label">{a["label"]}</p>'
                f'<ul class="cx-list">{lis}</ul>{note}</div>')
    if kind == "callout":
        h = f'<h3 class="cx-h3">{a["h3"]}</h3>' if a.get("h3") else ""
        tone = " cx-callout--accent" if a.get("tone") == "accent" else ""
        body = "".join(f"<p>{p}</p>" for p in a["paras"])
        cta = (f'<div class="cx-actions" style="margin-top: 14px;"><a class="btn btn-primary" href="{a["cta"][0]}">{a["cta"][1]}</a></div>'
               if a.get("cta") else "")
        return f'<div class="cx-callout{tone}">{h}{body}{cta}</div>'
    if kind == "figure":
        return (f'<figure class="cx-fig" data-fallback="{a["fallback"]}">'
                f'<img src="[[U:{a["img"]}]]" alt="{a["alt"]}" width="1200" height="900" loading="lazy" decoding="async">'
                f'<figcaption><span>Illustrative image</span></figcaption></figure>')
    raise ValueError(kind)


def _cta(c):
    if not c:
        return ""
    href, label = c
    return f'<div class="cx-actions"><a class="btn btn-secondary" href="{href}">{label}</a></div>'


def render_section(s):
    t, sid = s["type"], s["id"]
    lead = f'<p class="cx-lead">{s["lead"]}</p>' if s.get("lead") else ""
    note = f'<p class="cx-muted" style="margin: 22px 0 0; max-width: 74ch;">{s["note"]}</p>' if s.get("note") else ""
    if t == "split":
        inner = (f'<div class="cx-split"><div><h2 class="cx-h2">{s["h2"]}</h2>{lead}{_paras(s.get("paras", []), "cx-prose cx-muted")}</div>'
                 f'<div class="cx-stack">{"".join(_aside(a) for a in s["asides"])}</div></div>{note}{_cta(s.get("cta"))}')
    elif t == "cards":
        tone = {"line": " cx-card--line", "green": " cx-card--green", "accent": " cx-card--accent"}.get(s.get("tone"), "")
        grid = "cx-grid2" if s.get("cols") == 2 else "cx-grid3"
        cards = "".join(f'<div class="cx-card{tone}"><h3 class="cx-h3">{h}</h3><p>{p}</p></div>' for h, p in s["cards"])
        inner = (f'<h2 class="cx-h2">{s["h2"]}</h2>{lead}<div class="{grid}" style="gap: 18px; margin-top: 26px;">{cards}</div>'
                 f'{note}{_cta(s.get("cta"))}')
    elif t == "scope":
        inc = "".join(f"<li>{i}</li>" for i in s["included"])
        exc = "".join(f"<li>{i}</li>" for i in s["excluded"])
        inner = (f'<h2 class="cx-h2">{s["h2"]}</h2>{lead}<div class="cx-grid2" style="gap: 18px; margin-top: 26px;">'
                 f'<div class="cx-card cx-card--green"><p class="cx-label">{s.get("inc_label", "Can be included where agreed")}</p><ul class="cx-list">{inc}</ul></div>'
                 f'<div class="cx-card cx-card--accent"><p class="cx-label cx-label--accent">{s.get("exc_label", "Not included by default")}</p><ul class="cx-list">{exc}</ul></div>'
                 f'</div>{note}{_cta(s.get("cta"))}')
    elif t == "table":
        head = "".join(f'<th scope="col">{c}</th>' for c in s["cols"])
        rows = "".join(
            "<tr><th scope=\"row\">" + r[0] + "</th>" +
            "".join(f'<td data-label="{s["cols"][i + 1]}">{c}</td>' for i, c in enumerate(r[1:])) + "</tr>"
            for r in s["rows"])
        inner = (f'<h2 class="cx-h2">{s["h2"]}</h2>{lead}<div class="cx-table-wrap" style="margin-top: 26px;">'
                 f'<table class="cx-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>{note}{_cta(s.get("cta"))}')
    elif t == "steps":
        steps = "".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in s["steps"])
        inner = (f'<h2 class="cx-h2">{s["h2"]}</h2>{lead}<ol class="cx-steps" style="margin-top: 26px;">{steps}</ol>'
                 f'{note}{_cta(s.get("cta"))}')
    elif t == "faqs":
        half = (len(s["faqs"]) + 1) // 2
        cols = [s["faqs"][:half], s["faqs"][half:]]
        html = "".join(
            '<div class="cx-faq">' + "".join(
                f'<details><summary><h3>{q}</h3></summary><div class="cx-faq-a"><p>{a}</p></div></details>' for q, a in col)
            + "</div>" for col in cols)
        inner = (f'<h2 class="cx-h2">{s["h2"]}</h2><div class="cx-grid2" style="gap: 12px 20px; margin-top: 30px;">{html}</div>'
                 f'{_cta(s.get("cta"))}')
    elif t == "related":
        arts = "".join(
            f'<article class="cx-card cx-card--line cx-card--flex"><h3 class="cx-h3">{title}</h3><p>{text}</p>'
            f'<p class="cx-card-link"><a class="cx-textlink" href="{href}">{label} <span aria-hidden="true">→</span></a></p></article>'
            for href, title, text, label in s["links"])
        inner = f'<h2 class="cx-h2">{s["h2"]}</h2><div class="cx-grid4" style="margin-top: 26px;">{arts}</div>'
    else:
        raise ValueError(t)
    panel = s.get("panel")
    if panel:
        inner = f'<div class="cx-panel">{inner}</div>'
    return f'  <section id="{sid}" class="cx-sec">\n    <div class="cx-wrap">\n      {inner}\n    </div>\n  </section>\n'


def render_body(p):
    parent_href, parent_label = p["parent"]
    hero_paras = "".join(f"<p>{x}</p>" for x in p["hero_paras"])
    second = (f'<a class="btn btn-secondary" href="[[WA:{p["wa"]}]]" data-contact="whatsapp">WhatsApp CMAXX</a>')
    jump = "".join(f'<li><a href="#{s["id"]}">{s["nav"]}</a></li>' for s in p["sections"] if s.get("nav"))
    hero = f'''  <section id="{p["prefix"]}-top" class="cx-sec" style="padding-top: 0;">
    <div class="cx-wrap">
      <nav aria-label="Breadcrumb" class="cx-crumbs">
        <a href="/">Home</a><span aria-hidden="true" class="sep">/</span><a href="{parent_href}">{parent_label}</a><span aria-hidden="true" class="sep">/</span><span aria-current="page">{p["crumb"]}</span>
      </nav>
      <div class="cx-hero-grid">
        <div style="max-width: 660px;">
          <p class="cx-eyebrow">{p["eyebrow"]}</p>
          <h1 class="cx-h1">{p["h1"]}</h1>
          <p class="cx-hero-sub">{p["sub"]}</p>
          <div class="cx-prose cx-muted">{hero_paras}</div>
          <div class="cx-actions">
            <a class="btn btn-primary" href="#{p["enquiry_id"]}">{p["cta"]}</a>
            {second}
          </div>
          <p class="cx-micro">{p["micro"]}</p>
        </div>
        <figure class="cx-fig cx-fig--tall" data-fallback="{p["fallback"]}">
          <img src="[[U:{p["img"]}]]" alt="{p["alt"]}" width="960" height="1200" fetchpriority="high">
          <figcaption><span>Illustrative image</span></figcaption>
        </figure>
      </div>
      <nav class="cx-jump" aria-label="On this page">
        <p class="cx-jump-label">On this page</p>
        <ul>{jump}<li><a class="cx-jump-cta" href="#{p["enquiry_id"]}">{p["cta"]}</a></li></ul>
      </nav>
    </div>
  </section>
'''
    body = hero + "".join(render_section(s) for s in p["sections"])
    e = p["enquiry"]
    body += f'''  <section id="{p["enquiry_id"]}" class="cx-sec" data-enquiry="">
    <div class="cx-wrap">
      <div class="cx-band">
        <div class="cx-form-grid">
          <div>
            <h2 class="cx-h2">{e["h2"]}</h2>
            <p style="font-size: 18px; max-width: 52ch;">{e["text"]}</p>
            <div class="cx-band-actions">
              <a class="btn cx-btn-light" href="tel:+27101403660" data-contact="phone">Call CMAXX · 010 140 3660</a>
              <a class="btn cx-btn-outline-light" href="[[WA:{p["wa"]}]]" data-contact="whatsapp">WhatsApp CMAXX</a>
            </div>
            <p class="cx-band-note">{e["note"]}</p>
          </div>
          {e["form"]}
        </div>
      </div>
    </div>
  </section>
'''
    return body


# ------------------------------------------------- shared managed copy ----
MANAGED_PARENT = ("/managed-wifi/", "Managed WiFi")
MANAGED_WA = "Hello CMAXX. I would like to discuss a network assessment."
MANAGED_NOTE = ("Assessment scope, any charges, access requirements and scheduling are confirmed before work is booked. "
                "No installation or managed-service agreement is created by submitting this form. "
                "Already have a managed service? Please use the support contact route in your agreement.")


def managed_process(sid, label):
    return {"type": "steps", "id": sid, "nav": "How it works", "h2": "From the first discussion to ongoing support",
            "lead": f"The same five-step route applies to every {label}; the scope and the people involved change with the property.",
            "steps": [
                ("Understand the property and priorities", "Tell us which areas and users need connectivity, what is not working and what support you expect. We confirm the assessment approach, required access and any assessment charges."),
                ("Review the network and define the scope", "We assess the relevant equipment and connections, identify limitations and outline the proposed managed responsibilities, including existing faults and optional improvements."),
                ("Agree the proposal and work arrangements", "The quotation and service agreement set out the accepted scope, responsibilities, commercial terms and support arrangements. Installation or remedial work is included only where specified."),
                ("Onboard and check the agreed environment", "We carry out approved setup or changes, check the agreed network paths and establish management access. Work that may interrupt service is planned with your contact."),
                ("Manage, support and review changes", "Support and maintenance follow the agreement. Tell us when users, buildings, applications or equipment change so that the design and support can be reviewed."),
            ],
            "note": 'See the full <a href="/managed-wifi/#managed-scope">managed network scope</a> and <a href="/managed-wifi/#support-boundaries">support boundaries</a>.'}


def managed_enquiry(h2, text, prop, prefix):
    return {"h2": h2, "text": text, "note": MANAGED_NOTE, "form": f"[[FORM_NETWORK:{prop}:{prefix}]]"}


COMMON_MANAGED_FAQ_ISP = ("Is Managed WiFi the same as buying internet?",
    "No. Your licensed ISP supplies the internet service. Managed WiFi concerns the wireless and internal network that uses that service. CMAXX is not the upstream ISP; any ISP liaison happens only where it is agreed and authorised.")
COMMON_MANAGED_FAQ_QUOTE = ("How is the quotation worked out?",
    "Relevant factors include the layout, buildings, equipment, cabling, users, applications, existing faults and the support you need. Initial remedial work and ongoing management may be priced separately, and any assessment charges are confirmed before work is booked.")

# --------------------------------------------------- managed sub-pages ----
MANAGED_SUBPAGES = [
    {
        "route": "/managed-wifi/businesses-offices/", "prefix": "mb", "prop": "business",
        "label": "Managed WiFi for Businesses & Offices", "crumb": "Businesses &amp; Offices",
        "title": "Managed WiFi for Businesses & Offices Gauteng | CMAXX",
        "desc": "Ongoing management and support for the agreed office WiFi and internal network behind your staff, meetings and devices in Gauteng.",
        "eyebrow": "Managed WiFi for workplaces",
        "h1": "Managed WiFi for Businesses &amp; Offices in Gauteng",
        "sub": "Ongoing support for the agreed network behind your staff devices, meetings and everyday operations.",
        "hero_paras": ["CMAXX WiFi Solutions looks after the WiFi and internal network your office relies on - the access points, switches, settings and support arrangements agreed with you - so that responsibility for the network is clear.",
                       "Your internet service stays with your licensed ISP. Network support can sit alongside your existing IT arrangements rather than replacing them."],
        "micro": "Tell us about the office, the number of people and the main problem. Assessment scope and any charges are confirmed before work is booked.",
        "img": "photo-1497366216548-37526070297c", "alt": "Open-plan office with desks and meeting space", "fallback": "Office networks with a clear owner",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "split", "id": "office-needs", "nav": "Office demands", "h2": "What an office network has to carry",
             "lead": "Cloud applications, video meetings, printers, staff devices and visitor access place different demands on an office network.",
             "paras": ["We consider those requirements alongside the agreed equipment and support arrangements. A meeting room that works at 08:00 can struggle at 10:00 when everyone joins a call, and a printer on an unsuitable connection can affect a whole floor.",
                       "Adding staff or another floor may require a review of capacity and cabling, not only another WiFi unit."],
             "asides": [{"kind": "list", "label": "Typical office demands", "items": ["Cloud applications and shared files", "Video meetings and calls", "Printers, scanners and shared devices", "Staff laptops and phones", "Visitor and contractor access", "Meeting rooms and additional floors"]}]},
            {"type": "cards", "id": "office-signs", "nav": "Warning signs", "h2": "Signs the office network needs a clear owner",
             "cards": [("Calls drop at predictable times", "Meetings freeze when the office is busiest, which often points to capacity or a constrained link rather than the internet package."),
                       ("Every provider points elsewhere", "The ISP, the IT provider and the equipment supplier each believe the fault belongs to someone else."),
                       ("The network grew without a plan", "Access points, switches and routers were added over time without a record of how they connect or who controls the settings."),
                       ("Staff and visitors share one network", "Guests use the same network and password as staff and business devices."),
                       ("Restarting equipment is the routine fix", "The same rooms lose connectivity and someone restarts equipment until it works again."),
                       ("A move or new floor is planned", "Changes to the workspace have not yet been checked against the network's capacity and cabling.")]},
            {"type": "scope", "id": "office-scope", "nav": "What we manage", "h2": "What can be managed - and what stays separate",
             "lead": "We define the sites, equipment and responsibilities before the service starts. The examples below can form part of a suitable agreement; they are not automatic in every service.",
             "included": ["Review of the supported router, switches and access points", "Approved network names, access settings and configuration records", "Supported staff, guest and device separation", "Firmware and configuration maintenance within the agreed scope", "Fault investigation and an agreed support route", "Authorised liaison with your ISP where included"],
             "excluded": ["Printer repairs and laptop support", "Application troubleshooting", 'Microsoft 365 administration - see <a href="/cloud-microsoft-365/">Cloud &amp; Microsoft 365</a>', "Full cybersecurity or compliance certification", "The ISP's own service and restoration", "New cabling or equipment unless specified in the proposal"]},
            {"type": "split", "id": "office-growth", "h2": "Planning for growth, moves and new floors",
             "paras": ["Tell us when staff numbers, floors or applications change so that the effect on the design and support can be reviewed. Ongoing management creates a route for those reviews rather than assuming the original setup suits every future requirement.",
                       'For a new fit-out or a substantial upgrade, start with <a href="/business-wifi-solutions/">business and office WiFi installation</a>. We can discuss the appropriate support arrangement alongside the project.'],
             "asides": [{"kind": "callout", "h3": "Installation or ongoing management?", "paras": ["Installation delivers an agreed project; management establishes continuing responsibilities after the network is in use. A once-off installation does not automatically include continuing management."], "cta": ("/managed-wifi/#installation-or-management", "Compare the two approaches")}]},
            managed_process("office-process", "office"),
            {"type": "faqs", "id": "office-faqs", "nav": "FAQs", "h2": "Office Managed WiFi questions",
             "faqs": [("Can you work alongside our existing IT provider?", "Yes. Network support can sit alongside your existing IT arrangements. The agreement defines which network components CMAXX looks after and how incidents are passed between providers."),
                      ("Do you support Microsoft 365 or our laptops?", "Not as part of Managed WiFi. Network management does not automatically include device support, application troubleshooting or Microsoft 365 administration. Those can be discussed separately through our Cloud &amp; Microsoft 365 service."),
                      ("Can staff, guests and business devices be separated?", "Where compatible equipment and the agreed design support it, access can be separated and controlled. Different WiFi names alone do not prove the networks are isolated; the configuration needs to be designed and checked."),
                      ("We are moving office. Can you help?", "We can review the new space and identify the cabling, access-point and capacity requirements. Installation at the new premises is a defined project; ongoing management can follow under a separate scope."),
                      ("Is the service suitable for a small business?", "It can be, particularly where connectivity matters and nobody has clear responsibility for the network. For a simple, isolated problem, a once-off assessment or repair may be more appropriate."),
                      COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "office-related", "h2": "Related services",
             "links": [("/business-wifi-solutions/", "Business &amp; Office WiFi", "Design and installation for a new workplace or upgrade.", "Explore installation"),
                       ("/structured-cabling/", "Structured Cabling", "Data points, cabinets and the wired foundation.", "Explore cabling"),
                       ("/cloud-microsoft-365/", "Cloud &amp; Microsoft 365", "Accounts, email and productivity administration.", "Explore cloud services"),
                       ("/public-guest-wifi/", "Public &amp; Guest WiFi", "Controlled visitor access and portals.", "Explore guest WiFi")]},
        ],
        "enquiry": managed_enquiry("Give your office network a clear support plan", "Tell us about the office, how many people and devices use the network and where responsibility is currently unclear.", "business", "mb"),
    },
    {
        "route": "/managed-wifi/restaurants-cafes/", "prefix": "mr", "prop": "restaurant",
        "label": "Managed WiFi for Restaurants & Cafes", "crumb": "Restaurants &amp; Cafes",
        "title": "Managed WiFi for Restaurants & Cafes Gauteng | CMAXX",
        "desc": "Managed WiFi for restaurants and cafes in Gauteng: keep operational connectivity separate from guest access, planned around seating and peak trading.",
        "eyebrow": "Managed WiFi for hospitality",
        "h1": "Managed WiFi for Restaurants &amp; Cafes in Gauteng",
        "sub": "Keep the network your operation relies on separate from the access you offer customers.",
        "hero_paras": ["The connection used by staff and operational devices should be considered separately from guest access. CMAXX helps look after the agreed network behind both, with responsibilities defined before the service starts.",
                       "Seating areas, outdoor tables and peak trading periods all change what the network needs to handle."],
        "micro": "Share the venue's suburb, seating areas and the main connectivity concern. Assessment scope and any charges are confirmed before booking.",
        "img": "photo-1517248135467-4c7edcad34c4", "alt": "Restaurant interior with tables and warm lighting", "fallback": "Operations first, then guest access",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "split", "id": "restaurant-needs", "nav": "Two networks", "h2": "Two networks with different jobs",
             "lead": "Your operational network and your customer WiFi serve different people and carry different risks.",
             "paras": ["Suitable separation and usage controls may help manage those different uses where the equipment supports them and the design has been agreed. Customer streaming should not compete freely with the devices your service depends on.",
                       "Managing the network does not guarantee card-payment authorisation or the availability of a payment provider. Those remain with the payment and application providers."],
             "asides": [{"kind": "list", "label": "Operational connections", "items": ["Supported point-of-sale and payment terminals", "Kitchen order screens and printers", "Staff phones and tablets", "Music, CCTV or other connected equipment", "Back-office computers"]},
                        {"kind": "callout", "tone": "accent", "paras": ["Customer WiFi is a separate requirement. Portals, vouchers and other visitor-access options are covered by <a href=\"/public-guest-wifi/\">Public &amp; Guest WiFi</a>."]}]},
            {"type": "cards", "id": "restaurant-layout", "nav": "Layout and trading", "h2": "Coverage and capacity around the way you trade",
             "cards": [("Seating areas and outdoor tables", "Patios and terraces may need outdoor-rated equipment and a suitable connection back to the network."),
                       ("Peak trading periods", "A network that copes at quiet times may struggle when every table is full and every phone joins."),
                       ("Kitchen and back-of-house", "Walls, metal surfaces and equipment can affect wireless signal where order screens and printers operate."),
                       ("Several floors or rooms", "Each area needs an agreed coverage requirement rather than one router stretched across the venue."),
                       ("Music, screens and cameras", "Connected entertainment and CCTV add their own traffic and connection requirements."),
                       ("Opening hours and maintenance", "Changes that may interrupt service are planned around trading times with your contact.")]},
            {"type": "scope", "id": "restaurant-scope", "nav": "What we manage", "h2": "What can be managed - and what stays separate",
             "included": ["Review of the supported router, switches and access points", "Separation of operational and guest access where supported", "Supported usage and bandwidth controls", "Approved configuration records and maintenance", "Fault investigation and an agreed support route", "Authorised ISP liaison where included"],
             "excluded": ["Card-payment authorisation or payment-provider availability", "Point-of-sale software support", "Guaranteed speeds for every customer device", "Visitor analytics or data collection by default", "The ISP's own service and restoration"]},
            managed_process("restaurant-process", "restaurant or cafe"),
            {"type": "faqs", "id": "restaurant-faqs", "nav": "FAQs", "h2": "Restaurant and cafe WiFi questions",
             "faqs": [("Can customers and staff use separate networks?", "Where compatible equipment and the agreed design support it, staff, operational devices and customers can use separated access. The configuration is designed and checked; displaying different WiFi names alone does not prove isolation."),
                      ("Will managing the WiFi keep card payments working?", "Managing the network does not guarantee card-payment authorisation or a payment provider's availability. We agree which network connections are managed and where responsibility stays with the payment or application provider."),
                      ("Can you limit how much customers stream?", "Supported bandwidth controls can set limits or priorities for user groups. They help manage competing demand but cannot turn an inadequate internet service into an unlimited one."),
                      ("Can you cover our outdoor seating?", "Outdoor areas can be included in the assessment. They may need outdoor-rated equipment and a suitable wired or wireless connection back to the main network."),
                      ("Do you collect customer data through the WiFi?", "Not by default. Any portal, data collection or analytics needs an agreed purpose, appropriate notices and controls, and is discussed under Public &amp; Guest WiFi."),
                      COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "restaurant-related", "h2": "Related services",
             "links": [("/public-guest-wifi/", "Public &amp; Guest WiFi", "Portals, vouchers and visitor access.", "Explore guest WiFi"),
                       ("/outdoor-wifi-solutions/", "Outdoor WiFi", "Coverage for patios, gardens and terraces.", "Explore outdoor WiFi"),
                       ("/cctv-security-solutions/", "CCTV &amp; Security", "Camera systems and their network needs.", "Explore CCTV"),
                       ("/business-wifi-solutions/", "Business WiFi Installation", "A new fit-out or a substantial upgrade.", "Explore installation")]},
        ],
        "enquiry": managed_enquiry("Discuss the network behind your venue", "Tell us about the venue, the areas that need coverage, your busiest periods and which devices your operation depends on.", "restaurant", "mr"),
    },
    {
        "route": "/managed-wifi/retail-premises/", "prefix": "mt", "prop": "retail",
        "label": "Managed WiFi for Retail Premises", "crumb": "Retail &amp; Customer-Facing Premises",
        "title": "Managed WiFi for Retail Premises Gauteng | CMAXX",
        "desc": "Managed WiFi for retail and customer-facing premises in Gauteng. Agreed support for store devices and customer access, across one site or several branches.",
        "eyebrow": "Managed WiFi for stores and branches",
        "h1": "Managed WiFi for Retail &amp; Customer-Facing Premises",
        "sub": "Plan support around the store's agreed devices, trading needs and customer-access requirements.",
        "hero_paras": ["Retail requirements may include staff devices, supported payment terminals, stock systems and customer access. We agree which network connections are managed and where responsibility remains with the payment, application or equipment provider.",
                       "Whether you trade from one store or several branches, each site's equipment, internet feed and support needs are defined clearly."],
        "micro": "Tell us how many sites you have, where they are and what the network needs to support. Assessment scope and any charges are confirmed before booking.",
        "img": "photo-1441986300917-64674bd600d8", "alt": "Retail clothing store interior with display rails", "fallback": "Store networks with defined responsibilities",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "split", "id": "retail-needs", "nav": "Store devices", "h2": "The devices a store depends on",
             "lead": "A store network carries trading activity, stock work and customer access at the same time.",
             "paras": ["We review the supported equipment and connections behind those devices and agree which of them fall inside the managed scope. Where a device belongs to a payment, stock or signage provider, that provider's responsibilities are recorded rather than assumed.",
                       "Busy trading days, seasonal peaks and promotions can change the load on the network, so the design considers how the store is actually used."],
             "asides": [{"kind": "list", "label": "Typical store connections", "items": ["Staff devices and back-office computers", "Supported payment terminals", "Stock and inventory scanners", "Digital signage and music", "CCTV and other connected equipment", "Customer WiFi"]}]},
            {"type": "cards", "id": "retail-branches", "nav": "One or many sites", "h2": "One store or several branches",
             "cards": [("A single store", "The agreed router, switches and access points, the trading floor, storeroom and any back office are defined in one scope."),
                       ("Several branches", "Each site's equipment, internet feed, permissions and support requirements need to be defined. Sites rarely start from identical setups."),
                       ("Centralised management", "Managing several sites from one place depends on compatible systems. We assess what is practical before recommending it."),
                       ("Change windows", "Work that may interrupt trading is planned outside busy periods with the authorised contact."),
                       ("New branches", "A new store can be planned as an installation project, with ongoing management agreed alongside it."),
                       ("Mall or landlord infrastructure", "Shared-building cabling, risers or landlord equipment may need permission and coordination.")]},
            {"type": "scope", "id": "retail-scope", "nav": "What we manage", "h2": "What can be managed - and what stays separate",
             "included": ["Review of the supported router, switches and access points", "Separation of store, device and customer access where supported", "Approved configuration records and maintenance", "Fault investigation and an agreed support route", "Multi-site scope where systems are compatible", "Authorised ISP liaison where included"],
             "excluded": ["Customer analytics", "Transaction processing or guaranteed payment availability", "Stock, point-of-sale or signage software support", "Repairs to third-party-owned devices", "The ISP's own service and restoration"]},
            managed_process("retail-process", "store"),
            {"type": "faqs", "id": "retail-faqs", "nav": "FAQs", "h2": "Retail Managed WiFi questions",
             "faqs": [("Can you manage the network at all our branches?", "We can assess each site and define a scope per branch. Centralised management depends on compatible equipment; where sites differ, the proposal explains what can be managed consistently and what needs site-specific work."),
                      ("Does Managed WiFi include customer analytics?", "No. Customer analytics, transaction processing and guaranteed payment availability are not standard Managed WiFi inclusions. Any visitor data function needs an agreed purpose and appropriate notices."),
                      ("Who is responsible if a payment terminal goes offline?", "We investigate the network connections covered by our scope. The payment provider remains responsible for its terminal, service and authorisation. The agreement records how those issues are passed between providers."),
                      ("Can work be done outside trading hours?", "Changes that may interrupt service are planned with your contact. Timing, access and any attendance arrangements are agreed in the proposal."),
                      COMMON_MANAGED_FAQ_ISP, COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "retail-related", "h2": "Related services",
             "links": [("/public-guest-wifi/", "Public &amp; Guest WiFi", "Customer access, portals and vouchers.", "Explore guest WiFi"),
                       ("/structured-cabling/", "Structured Cabling", "Data points and cabinets for the store.", "Explore cabling"),
                       ("/cctv-security-solutions/", "CCTV &amp; Security", "Camera systems for the shop floor.", "Explore CCTV"),
                       ("/business-wifi-solutions/", "Business WiFi Installation", "Fitting out a new store.", "Explore installation")]},
        ],
        "enquiry": managed_enquiry("Discuss support for your store network", "Tell us about your store or branches, the devices you rely on and where support is currently unclear.", "retail", "mt"),
    },
    {
        "route": "/managed-wifi/schools/", "prefix": "mc", "prop": "school",
        "label": "Managed WiFi for Schools", "crumb": "Schools &amp; Training Facilities",
        "title": "Managed WiFi for Schools & Training Facilities Gauteng | CMAXX",
        "desc": "Managed WiFi for schools and training facilities in Gauteng, planned around administration, teaching spaces, lesson-time demand and the institution's access policies.",
        "eyebrow": "Managed WiFi for education",
        "h1": "Managed WiFi for Schools &amp; Training Facilities",
        "sub": "Plan administration, teaching and shared learning spaces around access policies and lesson-time demand.",
        "hero_paras": ["Administration offices, teaching rooms and shared learning spaces can have different access and capacity needs. Learner devices and lesson-time demand should be considered alongside staff access, the existing infrastructure and the institution's network policies.",
                       "CMAXX helps assess, support and maintain the agreed network, with specialist requirements assigned explicitly."],
        "micro": "Tell us about the campus, the buildings involved and how devices are used. Assessment scope and any charges are confirmed before booking.",
        "img": "photo-1580582932707-520aed937b7b", "alt": "Classroom with desks and a board at the front", "fallback": "Networks planned around lesson time",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "split", "id": "school-spaces", "nav": "Spaces and users", "h2": "Different spaces, different users",
             "lead": "A school network serves administrators, educators, learners and visitors - often in the same building at the same time.",
             "paras": ["Administration systems usually need different access from classroom devices, and visitors should not share staff access. Access controls, maintenance windows and permitted connections need an agreed design.",
                       "We look at how each space is used during the school day rather than treating the campus as one large room."],
             "asides": [{"kind": "list", "label": "Spaces we consider", "items": ["Administration and staff offices", "Classrooms and computer labs", "Halls and shared learning spaces", "Staff rooms", "Libraries and media centres", "Agreed outdoor or sports areas"]}]},
            {"type": "cards", "id": "school-demand", "nav": "Lesson-time demand", "h2": "Planning for lesson-time demand",
             "cards": [("Many devices at once", "A full class joining at the start of a lesson is a different load from a quiet office."),
                       ("Staff and learner access", "Different groups may need different permissions and connection rules."),
                       ("Assessments and online testing", "Times when connectivity matters most should be known before changes are scheduled."),
                       ("Shared and movable spaces", "Halls and multi-purpose rooms change use during the week."),
                       ("Maintenance outside teaching time", "Firmware and configuration work is planned to avoid disrupting lessons."),
                       ("Device policies", "Whether learners bring their own devices affects capacity and access design.")]},
            {"type": "scope", "id": "school-scope", "nav": "What we manage", "h2": "What can be managed - and what stays separate",
             "lead": "Network management alone does not provide comprehensive safeguarding. Specialist requirements must be assessed and assigned explicitly.",
             "included": ["Review of the supported router, switches and access points", "Staff, learner and visitor separation where supported", "Approved configuration records and maintenance windows", "Fault investigation and an agreed support route", "Capacity reviews when buildings or device numbers change", "Authorised ISP liaison where included"],
             "excluded": ["Comprehensive safeguarding or content filtering", "Endpoint security on learner or staff devices", "Legal or regulatory compliance certification", "Learning-platform or application support", "Device repairs"]},
            managed_process("school-process", "school or training facility"),
            {"type": "faqs", "id": "school-faqs", "nav": "FAQs", "h2": "School and training-facility questions",
             "faqs": [("Does Managed WiFi include content filtering?", "Not automatically. Network management alone does not provide comprehensive safeguarding, content filtering, endpoint security or legal compliance. Where these are required, they must be assessed and assigned explicitly."),
                      ("Can learners and staff use separate networks?", "Where compatible equipment and the agreed design support it, staff, learner and visitor access can be separated and controlled. The configuration is designed and checked, not assumed from WiFi names."),
                      ("Can maintenance happen outside teaching time?", "Yes, work that may interrupt service is planned with the authorised contact. Maintenance windows are agreed as part of the service."),
                      ("Can you cover several buildings on the campus?", "Several buildings can be included. Connections between buildings may need cabling or an outdoor link, which is assessed for feasibility before it is proposed."),
                      COMMON_MANAGED_FAQ_ISP, COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "school-related", "h2": "Related services",
             "links": [("/structured-cabling/", "Structured Cabling", "Data points and cabinets across the campus.", "Explore cabling"),
                       ("/outdoor-wifi-solutions/", "Outdoor &amp; Inter-Building WiFi", "Links between buildings and outdoor areas.", "Explore outdoor WiFi"),
                       ("/business-wifi-solutions/", "WiFi Installation", "New buildings or a substantial upgrade.", "Explore installation"),
                       ("/cloud-microsoft-365/", "Cloud &amp; Microsoft 365", "Staff email and productivity tools.", "Explore cloud services")]},
        ],
        "enquiry": managed_enquiry("Discuss your school's network", "Tell us about the campus, the spaces involved, approximate users and devices, and what currently needs attention.", "school", "mc"),
    },
    {
        "route": "/managed-wifi/residential-estates/", "prefix": "me", "prop": "estate",
        "label": "Managed WiFi for Residential Estates", "crumb": "Residential Estates",
        "title": "Managed WiFi for Residential Estates Gauteng | CMAXX",
        "desc": "Managed WiFi for residential estate communal areas in Gauteng: management offices, clubhouses, guardhouses and agreed outdoor zones.",
        "eyebrow": "Managed WiFi for estate communal areas",
        "h1": "Managed WiFi for Residential Estates &amp; Communal Areas",
        "sub": "Network support for agreed estate facilities - not internet inside every home.",
        "hero_paras": ["An estate requirement may concern a management office, clubhouse, guardhouse or agreed outdoor zone. We assess those areas as a defined network project or managed environment, with the necessary property permissions and infrastructure access.",
                       "This is different from providing WiFi inside each resident's home or internet throughout an entire estate."],
        "micro": "Tell us which estate facilities need connectivity and who approves the work. Assessment scope and any charges are confirmed before booking.",
        "img": "photo-1600596542815-ffad4c1539a9", "alt": "Modern residential house with a landscaped garden", "fallback": "Communal areas, clearly scoped",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "split", "id": "estate-areas", "nav": "Communal areas", "h2": "Estate facilities we can include",
             "lead": "The scope starts with the communal facilities the estate is responsible for.",
             "paras": ["Each area has its own users, equipment and access arrangements. A guardhouse network that supports visitor processes is a different requirement from WiFi for residents relaxing at the clubhouse.",
                       "We agree which facilities are in scope, who represents the estate and how changes are approved."],
             "asides": [{"kind": "list", "label": "Typical communal areas", "items": ["Estate management office", "Clubhouse and function areas", "Guardhouse or gatehouse", "Gym, pool and recreation areas", "Agreed outdoor zones", "Network connections for estate CCTV or access equipment, within scope"]}]},
            {"type": "cards", "id": "estate-feasibility", "nav": "Feasibility", "h2": "What affects feasibility",
             "cards": [("Permissions", "Body corporate, HOA or management approvals are needed before work starts."),
                       ("Cable routes and distance", "Distances between facilities influence whether cabling, fibre or a wireless link is practical."),
                       ("Power", "Equipment at gates, guardhouses and outdoor zones needs a suitable power path."),
                       ("The upstream connection", "The internet feed available at each facility affects what the network can deliver."),
                       ("Outdoor conditions", "Exposed equipment needs suitable protection and secure mounting."),
                       ("Access for maintenance", "Equipment locations need safe, authorised access for future support.")]},
            {"type": "scope", "id": "estate-scope", "nav": "What we manage", "h2": "What is - and is not - part of an estate service",
             "included": ["Networks for agreed communal facilities", "Supported routers, switches and access points in those facilities", "Approved configuration records and maintenance", "Fault investigation and an agreed support route", "Assessment of links between facilities", "Authorised ISP liaison where included"],
             "excluded": ['WiFi inside individual homes - see <a href="/home-wifi-solutions/">Home WiFi Solutions</a>', "Internet service for every resident", "Gate motors, booms or access-control hardware repairs", "Security monitoring or armed response", "The ISP's own service and restoration"]},
            {"type": "split", "id": "estate-residents", "h2": "Residents' homes are a separate service",
             "paras": ["Residents who want better WiFi inside their own homes can use our <a href=\"/home-wifi-solutions/\">Home WiFi Solutions</a>. That keeps the estate's communal responsibilities separate from each household's private network.",
                       "For suitable outside requirements, such as links between facilities or coverage around recreation areas, see <a href=\"/outdoor-wifi-solutions/\">outdoor WiFi and inter-building connectivity</a>."],
             "asides": [{"kind": "callout", "tone": "accent", "paras": ["Building access, cable routes, distance, power and the upstream connection affect feasibility. We assess before recommending equipment, rather than promising estate-wide coverage."]}]},
            managed_process("estate-process", "estate"),
            {"type": "faqs", "id": "estate-faqs", "nav": "FAQs", "h2": "Estate network questions",
             "faqs": [("Can you provide WiFi to every home in the estate?", "That is not what this service covers. We support agreed communal facilities. Individual homeowners can discuss Home WiFi Solutions for their own property, and internet service remains with licensed ISPs."),
                      ("Who approves the work?", "The estate's authorised representative, such as the managing agent, HOA or body corporate, approves the scope, access and any changes. We record that contact in the agreement."),
                      ("Can you connect the guardhouse to the clubhouse network?", "We can assess the distance, available routes and power to recommend cabling, fibre or a suitable wireless link. Feasibility is confirmed before it is proposed."),
                      ("Do you maintain gate or access-control equipment?", "Not as part of Managed WiFi. We can look after the agreed network connections such equipment uses; motors, booms and access-control hardware are separate specialist services."),
                      COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "estate-related", "h2": "Related services",
             "links": [("/outdoor-wifi-solutions/", "Outdoor WiFi", "Links between facilities and outdoor zones.", "Explore outdoor WiFi"),
                       ("/home-wifi-solutions/", "Home WiFi Solutions", "WiFi inside an individual residence.", "Explore Home WiFi"),
                       ("/cctv-security-solutions/", "CCTV &amp; Security", "Camera systems for communal areas.", "Explore CCTV"),
                       ("/structured-cabling/", "Structured Cabling", "Cabling and cabinets for estate facilities.", "Explore cabling")]},
        ],
        "enquiry": managed_enquiry("Discuss your estate's communal network", "Tell us which facilities need connectivity, how far apart they are and who approves work on behalf of the estate.", "estate", "me"),
    },
    {
        "route": "/managed-wifi/events/", "prefix": "mv", "prop": "event",
        "label": "Managed WiFi for Event Venues & Events", "crumb": "Events",
        "title": "Managed WiFi for Event Venues Gauteng | CMAXX",
        "desc": "Managed WiFi for permanent event venues in Gauteng, and how it differs from temporary Event WiFi for a single date.",
        "eyebrow": "Managed WiFi for venues and events",
        "h1": "Managed WiFi for Event Venues &amp; Events",
        "sub": "Separate a venue's year-round network from the temporary connectivity each event needs.",
        "hero_paras": ["A permanent venue may need an ongoing management arrangement as well as separate event projects. CMAXX looks after the agreed year-round network; temporary equipment and event-day support are planned through Event WiFi Solutions.",
                       "Keeping the two apart makes it clear what the monthly service covers and what each event needs."],
        "micro": 'Planning a single event rather than a venue? Go straight to <a href="/event-wifi-solutions/">Event WiFi Solutions</a>.',
        "img": "photo-1540575467063-178a50c2df87", "alt": "Conference audience seated in a large event hall", "fallback": "Year-round venue networks",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "table", "id": "event-compare", "nav": "Venue or event?", "h2": "Permanent venue or temporary event?",
             "lead": "Event deployment, attendance and temporary equipment are not automatically included in a normal recurring management agreement.",
             "cols": ["Question", "Managed venue network", "Temporary Event WiFi"],
             "rows": [["Main purpose", "Look after the venue's agreed network over time", "Connectivity for a specific date and requirement"],
                      ["Typical customer", "Conference centres, halls and function venues", "Organisers and venue teams for one event"],
                      ["Equipment", "The venue's installed or agreed equipment", "Temporary equipment planned for the event"],
                      ["Support", "Follows the managed-service agreement", "Event support terms in the event proposal"],
                      ["Where to start", "A network assessment of the venue", '<a href="/event-wifi-solutions/">Event WiFi Solutions</a>']]},
            {"type": "cards", "id": "event-venue-needs", "nav": "Venue needs", "h2": "What a venue network may need to support",
             "cards": [("Organiser and staff access", "Connections for the venue team, organisers and production crews."),
                       ("Exhibitor and vendor connections", "Separated access for exhibitors where the design supports it."),
                       ("Guest access", "Visitor WiFi with access options agreed under Public &amp; Guest WiFi."),
                       ("AV, streaming and presentations", "Fixed connections for equipment that should not rely on crowded wireless."),
                       ("Ticketing and access scanners", "Devices that matter at doors and registration points."),
                       ("Busy-period capacity", "The difference between an empty hall and a full one.")]},
            {"type": "scope", "id": "event-scope", "nav": "What we manage", "h2": "What a managed venue service can include",
             "included": ["The venue's supported routers, switches and access points", "Approved configuration for staff, exhibitor and guest access", "Maintenance planned around the venue's calendar", "Fault investigation and an agreed support route", "Capacity reviews when rooms or uses change", "Authorised ISP liaison where included"],
             "excluded": ["Temporary equipment for individual events", "Event-day attendance, unless separately agreed", "Guaranteed performance for unknown attendance", "Additional internet capacity from the ISP", "Ticketing, AV or streaming platform support"]},
            managed_process("event-process", "venue"),
            {"type": "faqs", "id": "event-faqs", "nav": "FAQs", "h2": "Venue and event WiFi questions",
             "faqs": [("Does a managed venue service cover every event?", "No. The managed service looks after the venue's agreed network. Event deployment, attendance and temporary equipment are planned for each event under Event WiFi Solutions unless your agreement says otherwise."),
                      ("We only need WiFi for one event. Is this the right page?", "Probably not. Event WiFi Solutions plans connectivity around the date, venue access, expected usage, available internet feed, power and operational requirements."),
                      ("Can you guarantee WiFi for a full conference hall?", "No network can guarantee performance without knowing the attendance, devices, applications and internet capacity. We assess the expected use and explain the limits before an event or venue design is agreed."),
                      ("Can exhibitors have their own network?", "Where compatible equipment and the agreed design support it, exhibitor access can be separated from staff and guest access."),
                      COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "event-related", "h2": "Related services",
             "links": [("/event-wifi-solutions/", "Event WiFi Solutions", "Temporary connectivity for a specific event.", "Explore Event WiFi"),
                       ("/public-guest-wifi/", "Public &amp; Guest WiFi", "Visitor access, portals and vouchers.", "Explore guest WiFi"),
                       ("/outdoor-wifi-solutions/", "Outdoor WiFi", "Gardens, marquees and outdoor areas.", "Explore outdoor WiFi"),
                       ("/structured-cabling/", "Structured Cabling", "Fixed connections for AV and registration.", "Explore cabling")]},
        ],
        "enquiry": managed_enquiry("Discuss your venue's network", "Tell us about the venue, its spaces, typical events and what the network needs to support year-round.", "event", "mv"),
    },
    {
        "route": "/managed-wifi/public-facilities/", "prefix": "mp", "prop": "public",
        "label": "Managed WiFi for Public Facilities", "crumb": "Community &amp; Public Facilities",
        "title": "Managed WiFi for Public & Community Facilities Gauteng | CMAXX",
        "desc": "Managed WiFi for libraries, community centres and public-facing facilities in Gauteng, with defined coverage, busy-period demand and visitor-access responsibilities.",
        "eyebrow": "Managed WiFi for community and public venues",
        "h1": "Managed WiFi for Community &amp; Public Facilities",
        "sub": "Shared-area coverage, busy-period demand and clear visitor-access responsibilities.",
        "hero_paras": ["Libraries, community centres and other public-facing facilities may need access across shared spaces and support during busy periods. A workable solution defines the coverage areas, likely usage, access policies and the responsibilities of the venue, CMAXX and the ISP.",
                       "Visitor data collection and analytics are not automatic; any such function needs an agreed purpose, notices and controls."],
        "micro": "Tell us about the facility, the spaces visitors use and its busiest times. Assessment scope and any charges are confirmed before booking.",
        "img": "photo-1521587760476-6c12a4b040da", "alt": "Library interior with tall bookshelves", "fallback": "Shared spaces, clear responsibilities",
        "cta": "Request a Network Assessment", "enquiry_id": "network-assessment", "wa": MANAGED_WA, "parent": MANAGED_PARENT,
        "sections": [
            {"type": "split", "id": "public-spaces", "nav": "Facilities", "h2": "Facilities with shared spaces",
             "lead": "Public facilities serve staff, regular users and visitors who may only connect once.",
             "paras": ["The network needs to support the facility's own operations while offering appropriate visitor access. We agree the areas in scope, who manages the facility's side of access, and how faults are reported.",
                       "Halls and multi-purpose rooms change use during the week, so expected usage is discussed room by room."],
             "asides": [{"kind": "list", "label": "Typical facilities", "items": ["Libraries and reading rooms", "Community centres and halls", "Places of worship", "Sports and recreation facilities", "Shared reception and waiting areas", "Administration offices"]}]},
            {"type": "cards", "id": "public-busy", "nav": "Busy periods", "h2": "Shared spaces and busy periods",
             "cards": [("Coverage areas", "The rooms, halls and outdoor areas where access is needed are agreed in the scope."),
                       ("Busy periods", "Events, services, school holidays and peak hours change the load on the network."),
                       ("Staff and visitor access", "The facility's own systems are kept separate from visitor access where supported."),
                       ("Access policies", "Session limits, terms of use and permitted connections are agreed with the facility."),
                       ("Fair use", "Supported bandwidth controls help manage competing demand within the available internet capacity."),
                       ("Responsibilities", "The venue, CMAXX and the ISP each have a defined role.")]},
            {"type": "scope", "id": "public-scope", "nav": "What we manage", "h2": "What can be managed - and what stays separate",
             "included": ["Review of the supported router, switches and access points", "Separation of staff and visitor access where supported", "Supported usage and bandwidth controls", "Approved configuration records and maintenance", "Fault investigation and an agreed support route", "Authorised ISP liaison where included"],
             "excluded": ["Visitor data collection or analytics by default", "Content filtering or safeguarding unless separately assessed", "Support for visitors' personal devices", "Additional ISP capacity", "The ISP's own service and restoration"]},
            {"type": "split", "id": "public-data", "h2": "Visitor access and personal information",
             "paras": ["Any portal, registration or visitor-data function needs a defined purpose, appropriate notices and agreed handling. It should not be switched on simply because the equipment supports it.",
                       'Where controlled visitor access is part of the requirement, see <a href="/public-guest-wifi/">Public &amp; Guest WiFi</a> for portal and voucher options.'],
             "asides": [{"kind": "callout", "paras": ["Operational network monitoring is different from inspecting what visitors do online. It is not a promise to read messages or monitor personal browsing content."]}]},
            managed_process("public-process", "facility"),
            {"type": "faqs", "id": "public-faqs", "nav": "FAQs", "h2": "Public facility WiFi questions",
             "faqs": [("Do you collect information about visitors?", "Not by default. Visitor data collection and analytics need an agreed purpose and appropriate notices and controls before they are used."),
                      ("Can you filter what visitors access online?", "Network management alone does not provide comprehensive content filtering or safeguarding. Where a facility needs these, they must be assessed and assigned explicitly."),
                      ("Can staff and visitors use separate networks?", "Where compatible equipment and the agreed design support it, the facility's own systems and visitor access can be separated and controlled."),
                      ("Can we limit how long visitors stay connected?", "Session limits and usage controls may be possible on supported equipment. They are agreed as part of the access policy, often alongside Public &amp; Guest WiFi options."),
                      COMMON_MANAGED_FAQ_ISP, COMMON_MANAGED_FAQ_QUOTE]},
            {"type": "related", "id": "public-related", "h2": "Related services",
             "links": [("/public-guest-wifi/", "Public &amp; Guest WiFi", "Portals, vouchers and visitor access.", "Explore guest WiFi"),
                       ("/outdoor-wifi-solutions/", "Outdoor WiFi", "Sports fields and outdoor gathering areas.", "Explore outdoor WiFi"),
                       ("/structured-cabling/", "Structured Cabling", "The wired foundation for the facility.", "Explore cabling"),
                       ("/event-wifi-solutions/", "Event WiFi", "Temporary connectivity for special events.", "Explore Event WiFi")]},
        ],
        "enquiry": managed_enquiry("Discuss your facility's network", "Tell us about the facility, the spaces visitors use, its busiest periods and who manages access today.", "public", "mp"),
    },
]

# --------------------------------------------------- shared smart copy ----
SMART_PARENT = ("/smart-home/", "Smart Home Services")
SMART_NOTE = ('Please do not submit passwords, recovery codes, payment details or private camera footage. Assessment arrangements, availability and any applicable charges are confirmed before booking. Read our <a href="/policy-popia/">Privacy &amp; POPIA Notice</a>.')


def smart_process(sid):
    return {"type": "steps", "id": sid, "nav": "How it works", "h2": "From first discussion to a system you can use",
            "lead": "The steps are tailored to the agreed scope; a small setup will not need the same design work as a whole-home installation.",
            "steps": [("Discuss and assess", "Tell us what you want to improve and what you already own. Where needed, we inspect the layout, device positions and existing network."),
                      ("Design and recommend", "We define the compatible approach, dependencies, limitations and any other contractors' responsibilities, then propose the equipment and scope."),
                      ("Install and configure", "We complete the agreed network and device work, organise names and rooms, and set up authorised accounts and controls."),
                      ("Test the agreed functions", "We test the agreed functions and relevant local and remote behaviour, including recovery where it is safe to do so."),
                      ("Hand over and support", "We demonstrate everyday controls, explain limitations and confirm how to request help and what is separately chargeable.")],
            "note": 'See the full <a href="/smart-home/#process">12-step project process</a>. An enquiry does not create a confirmed appointment.'}


def smart_enquiry(h2, text, service, prefix):
    return {"h2": h2, "text": text, "note": SMART_NOTE, "form": f"[[FORM_SMART:{service}:{prefix}]]"}


SMART_FAQ_ELECTRICAL = ("Does CMAXX do the electrical work?",
    "Our integration service covers the agreed device, network and configuration work. Fixed-wiring changes and electrical installation work must be undertaken by an appropriately registered electrical contractor, identified separately in the scope.")
SMART_FAQ_COST = ("How much does it cost?",
    "Costs depend on the devices, existing network, installation access, configuration and any specialist contractor work. We define the scope before quoting and separate equipment and installation from subscriptions or optional support. Any assessment or call-out charges are confirmed before booking.")

# ----------------------------------------------------- smart sub-pages ----
SMART_SUBPAGES = [
    {
        "route": "/smart-home/connected-entertainment/", "prefix": "se", "service": "entertainment",
        "label": "Connected Entertainment", "crumb": "Connected Entertainment",
        "title": "Connected Home Entertainment Setup Gauteng | CMAXX",
        "desc": "Network and setup for compatible smart TVs, streaming devices, smart speakers and multi-room audio in Gauteng homes.",
        "eyebrow": "TVs, streaming and multi-room audio",
        "h1": "Connected Entertainment Setup in Gauteng",
        "sub": "Reliable connectivity behind your TVs, streaming devices, smart speakers and music zones.",
        "hero_paras": ["A connected entertainment system should be straightforward to use and properly connected behind the screen. CMAXX assesses the network and helps configure compatible smart TVs, streaming devices, smart speakers, network-connected receivers and supported multi-room audio equipment.",
                       "Acoustic design, specialist cinema construction, structural mounting and electronics repairs are separate services, not part of this offer."],
        "micro": "Tell us which rooms, screens and audio equipment are involved. Assessment arrangements and any charges are confirmed before booking.",
        "img": "photo-1593784991095-a205069470b6", "alt": "Television mounted in a modern living room", "fallback": "Entertainment that just works",
        "cta": "Discuss My TV or Audio Setup", "enquiry_id": "smart-enquiry", "wa": "Hello CMAXX, I would like to discuss a smart-home project in Gauteng.", "parent": SMART_PARENT,
        "sections": [
            {"type": "cards", "id": "entertainment-scope", "nav": "What we set up", "h2": "What we can help set up",
             "cards": [("Smart TVs and streaming devices", "Supported connection, app setup, updates and access to the services you use."),
                       ("Network-connected receivers", "Configuration of supported receivers and their network connection."),
                       ("Smart speakers", "Setup of compatible speakers, rooms and supported voice control."),
                       ("Multi-room audio", "Useful zones with supported grouping, sources and volume controls."),
                       ("Wired points for fixed equipment", 'Ethernet for TVs, streamers and receivers through <a href="/structured-cabling/">structured cabling</a>.'),
                       ("A clear handover", "Everyday controls explained so the household can use the system without the installer.")]},
            {"type": "split", "id": "entertainment-connection", "nav": "Ethernet or WiFi", "h2": "Ethernet or WiFi for your screens?",
             "paras": ["For fixed equipment, Ethernet can reduce dependence on wireless conditions. Good WiFi can also work well where the device supports it and signal and capacity are suitable. A cable is not an automatic speed upgrade: the device's network port and the rest of the connection also matter.",
                       'We check the device\'s supported connection rather than assuming. If coverage is the problem, start with <a href="/smart-home/reliable-connectivity/">reliable connectivity</a> or <a href="/home-wifi-solutions/">Home WiFi Solutions</a>.'],
             "asides": [{"kind": "callout", "tone": "accent", "h3": "About 4K streaming", "paras": ["4K streaming needs a stable connection and enough capacity for simultaneous use. For example, Netflix recommends 15 Mbps or higher for a 4K stream. That is a service-specific example, not a whole-house sizing rule or a promise that any connection at that speed will perform perfectly."]}]},
            {"type": "split", "id": "entertainment-audio", "nav": "Music zones", "h2": "Music zones and multi-room audio",
             "paras": ["Compatible audio equipment can be configured into useful rooms or zones, with supported grouping, sources and volume controls. Wireless audio still needs suitable connectivity, power and platform support.",
                       "Equipment appearing on the same WiFi network does not mean that different brands can automatically play synchronised audio together. Voice control, available music services and the commands you can use vary by device, platform, subscription and region."],
             "asides": [{"kind": "figure", "img": "photo-1586023492125-27b2c045efd7", "alt": "Living room with sofa and lamps", "fallback": "Rooms and zones that suit the household"}]},
            {"type": "scope", "id": "entertainment-boundaries", "h2": "What is included - and what is a separate service",
             "included": ["Network readiness for entertainment equipment", "Configuration of compatible TVs, streamers and receivers", "Supported smart-speaker and multi-room setup", "Wired connections through an agreed cabling scope", "Testing and a practical handover"],
             "excluded": ["Acoustic design or specialist cinema construction", "Structural mounting", "Repair of electronics", "Synchronising brands that do not support it", "Streaming subscriptions and service availability"]},
            smart_process("entertainment-process"),
            {"type": "faqs", "id": "entertainment-faqs", "nav": "FAQs", "h2": "Connected entertainment questions",
             "faqs": [("Can my existing receiver be used?", "Often, if it supports the connection and functions you want. We check the model, its network features and inputs before recommending anything new."),
                      ("Can different brands of speakers play together?", "Only where the products and software support the intended grouping or playback method. Sharing a WiFi network does not make unrelated speakers a synchronised system."),
                      ("What needs an Ethernet connection?", "Nothing needs one by default, but fixed equipment such as TVs, streamers and receivers often benefits from a cable. We consider signal, simultaneous use and the device's own port or radio capabilities."),
                      ("Will voice control work for every source?", "No. Voice commands depend on the device, platform, subscription and region. We confirm the commands you actually need before setup."),
                      ("Are streaming subscriptions included?", "No. Subscriptions are separate and remain in your name. The proposal identifies any known recurring requirements."),
                      ("Do you design home cinemas or acoustics?", "No. Acoustic design, specialist cinema construction, structural mounting and electronics repairs are separate services."),
                      SMART_FAQ_COST]},
            {"type": "related", "id": "entertainment-related", "h2": "Related services",
             "links": [("/smart-home/reliable-connectivity/", "Reliable Connectivity", "The network behind your entertainment.", "Explore connectivity"),
                       ("/home-wifi-solutions/", "Home WiFi Solutions", "Coverage and capacity across the home.", "Explore Home WiFi"),
                       ("/structured-cabling/", "Structured Cabling", "Wired points for fixed equipment.", "Explore cabling"),
                       ("/smart-home/setup-troubleshooting/", "Setup &amp; Troubleshooting", "Existing devices that are not working.", "Get support")]},
        ],
        "enquiry": smart_enquiry("Discuss your TV or audio setup", "Tell us which rooms, screens, speakers and receivers are involved, and what you would like to work better.", "entertainment", "se"),
    },
    {
        "route": "/smart-home/smart-security-access/", "prefix": "sc", "service": "security",
        "label": "Smart Security & Access", "crumb": "Smart Security &amp; Access",
        "title": "Smart Security & Access Integration Gauteng | CMAXX",
        "desc": "Configure compatible smart cameras, video doorbells, intercoms and selected access integrations in Gauteng homes, within a clear scope.",
        "eyebrow": "Cameras, doorbells and intercoms",
        "h1": "Smart Security &amp; Access Integration in Gauteng",
        "sub": "Connect supported cameras, doorbells and intercoms, with clear viewing, notification and user-access settings.",
        "hero_paras": ["Smart security brings supported viewing, notifications and visitor communication into a more usable system. CMAXX can assess camera connectivity and configure compatible cameras, video doorbells, intercoms and selected access-related integrations within an agreed installation scope.",
                       "Remote viewing and mobile alerts are not a staffed monitoring or armed-response service."],
        "micro": 'For full camera systems and recording, see <a href="/cctv-security-solutions/">CCTV &amp; Security Solutions</a>.',
        "img": "photo-1557597774-9d273605dfa9", "alt": "Security camera mounted on an exterior wall", "fallback": "Connected security, clearly scoped",
        "cta": "Discuss Connected Security", "enquiry_id": "smart-enquiry", "wa": "Hello CMAXX, I would like to discuss a smart-home project in Gauteng.", "parent": SMART_PARENT,
        "sections": [
            {"type": "cards", "id": "security-what", "nav": "What we connect", "h2": "What we can connect and configure",
             "cards": [("Smart cameras", "Compatible WiFi and PoE cameras, with supported viewing and notifications."),
                       ("Video doorbells", "Visitor communication and alerts from a supported doorbell."),
                       ("Intercoms", "Supported intercom setup and app access for authorised users."),
                       ("Notifications", "Person detection, motion zones and sensor events where the device offers them."),
                       ("Selected access integrations", "Gate-related functions assessed against the existing controller and safety arrangements."),
                       ("User permissions", "Who can view, receive alerts and grant access - and how to remove them.")]},
            {"type": "split", "id": "security-connection", "nav": "Cameras and network", "h2": "Cameras and the connection behind them",
             "paras": ["WiFi cameras need suitable signal at the actual mounting position and still need an appropriate power source or battery arrangement. Compatible PoE cameras use a network cable for data and power. We assess the network, recording requirements and supported remote-viewing options rather than treating every camera as interchangeable.",
                       "Selected devices provide person detection, motion zones, mobile alerts or sensor events. Availability, detection accuracy, scheduling, recording and camera tracking differ between models and may depend on a hub, firmware or subscription. Where a platform exposes the function, a supported event can form part of a routine, such as turning on an entrance light."],
             "asides": [{"kind": "callout", "paras": ['Our <a href="/cctv-security-solutions/">CCTV &amp; Security Solutions</a> pages cover camera installation, wireless and smart cameras, recording and remote viewing in detail. For signal at gates and outbuildings, see <a href="/outdoor-wifi-solutions/">Outdoor WiFi Solutions</a>.']}]},
            {"type": "split", "id": "security-access", "nav": "Doorbells and access", "h2": "Doorbells, intercoms and access",
             "paras": ["A compatible video doorbell or intercom can help you communicate with visitors and manage authorised access. Gate-related integration is assessed against the existing controller and safety arrangements.",
                       "Permissions and the behaviour after power or network loss must remain clear. Camera placement, access to footage and visitor privacy also need consideration."],
             "asides": [{"kind": "callout", "tone": "accent", "h3": "Safety and contractor boundaries", "paras": ["Gate-related integration does not include motor repairs, gate mechanics or bypassing safety devices. Locksmith, motor and specialist electrical work belongs with the appropriate contractor."]}]},
            {"type": "scope", "id": "security-boundaries", "h2": "What is included - and what is a separate service",
             "included": ["Camera and doorbell connectivity assessment", "Configuration of compatible cameras, doorbells and intercoms", "Supported notifications and routines", "User permissions and account setup", "Testing and a practical handover"],
             "excluded": ["Staffed monitoring or armed response", "Gate motor repairs, mechanics or locksmith work", "Bypassing safety devices", "Features a device or platform does not support", "Cloud recording subscriptions"]},
            smart_process("security-process"),
            {"type": "faqs", "id": "security-faqs", "nav": "FAQs", "h2": "Smart security questions",
             "faqs": [("Can my existing gate motor remain?", "Often, if its controller exposes a suitable, supported interface. We assess it against the existing safety arrangements before proposing any integration."),
                      ("Do you repair gate motors?", "No. Motor repairs, gate mechanics and safety hardware are specialist services outside this integration scope."),
                      ("Is a video doorbell the same as access control?", "No. A doorbell helps you see and speak to visitors. Access control decides who can enter, and needs its own equipment, permissions and safety checks."),
                      ("What happens without internet or power?", "Remote viewing and off-site alerts usually need the internet. Mains-powered equipment needs power unless suitably backed up. We explain the behaviour of the agreed equipment and test it where safe."),
                      ("Can family members have separate access?", "Most supported platforms allow separate users and permissions. We set them up during handover and show you how to remove a user."),
                      ("Is someone watching my cameras?", "No. Remote viewing and mobile alerts are not a staffed monitoring or armed-response service."),
                      SMART_FAQ_COST]},
            {"type": "related", "id": "security-related", "h2": "Related services",
             "links": [("/cctv-security-solutions/", "CCTV &amp; Security Solutions", "Camera systems, recording and remote viewing.", "Explore CCTV"),
                       ("/outdoor-wifi-solutions/", "Outdoor WiFi", "Signal at gates and outbuildings.", "Explore outdoor WiFi"),
                       ("/smart-home/reliable-connectivity/", "Reliable Connectivity", "The network behind your cameras.", "Explore connectivity"),
                       ("/smart-home/setup-troubleshooting/", "Setup &amp; Troubleshooting", "Existing devices that are not working.", "Get support")]},
        ],
        "enquiry": smart_enquiry("Discuss connected security", "Tell us which cameras, doorbells or intercoms you have or are considering, and what you would like them to do.", "security", "sc"),
    },
    {
        "route": "/smart-home/climate-control/", "prefix": "sm", "service": "climate",
        "label": "Climate Control", "crumb": "Climate Control",
        "title": "Smart Climate Control Integration Gauteng | CMAXX",
        "desc": "Assess and configure compatible smart control for existing air conditioners, thermostats and climate controllers in Gauteng homes.",
        "eyebrow": "Compatible heating and cooling control",
        "h1": "Smart Climate Control Integration in Gauteng",
        "sub": "Smart control for compatible heating and cooling equipment you already own.",
        "hero_paras": ["Some existing air conditioners, thermostats and climate controllers can be connected to supported apps or automation platforms. CMAXX can assess whether the equipment you already own exposes suitable functions and help configure supported control, scheduling and connectivity.",
                       "This is a technology integration service. Air-conditioning installation, refrigerant work and mechanical servicing are not included."],
        "micro": "Share the make and model of your climate equipment if you have it. Assessment arrangements and any charges are confirmed before booking.",
        "img": "photo-1600210492486-724fe5c67fb0", "alt": "Bright, modern living room interior", "fallback": "Comfort controls that suit your equipment",
        "cta": "Check My Climate-System Compatibility", "enquiry_id": "smart-enquiry", "wa": "Hello CMAXX, I would like to discuss a smart-home project in Gauteng.", "parent": SMART_PARENT,
        "sections": [
            {"type": "cards", "id": "climate-possible", "nav": "What may be possible", "h2": "What may be possible",
             "lead": "Depending on the system, the agreed scope could include:",
             "cards": [("Manufacturer-app setup", "Connecting supported equipment to its own app and your home network."),
                       ("Supported remote control", "Changing modes and temperature from your phone where the equipment allows it."),
                       ("Temperature schedules", "Agreed schedules for the times and rooms that matter."),
                       ("Room-sensor routines", "Routines using compatible sensors, with manual controls retained."),
                       ("Infrared controllers", "Selected IR controllers operating supported equipment through a remote-control profile, with suitable placement."),
                       ("Notifications", "Supported alerts from the equipment or its controller.")],
             "note": "Sending an infrared command is not always confirmation that the appliance received it or reached the requested state."},
            {"type": "split", "id": "climate-checks", "nav": "Before you buy", "h2": "Questions we answer before you buy a controller",
             "paras": ["A smart thermostat is not a universal replacement for an existing controller. The control interface, electrical requirements, supported operating modes and the HVAC manufacturer's requirements must be checked before any hardware change.",
                       "Professional assessment is useful before purchasing a controller or promising a new routine."],
             "asides": [{"kind": "list", "label": "We confirm", "items": ["What can be controlled", "What feedback is available", "Which functions need the internet", "How the original controls remain usable", "Whether a specialist contractor is needed"]}]},
            {"type": "split", "id": "climate-specialists", "h2": "Who performs the specialist work?",
             "paras": ["Our role is the agreed technology integration and network configuration. Air-conditioning installation, refrigerant work, mechanical servicing, thermostat wiring and other specialist electrical or heating and cooling work are not included in this integration service.",
                       "Where those tasks are needed, an appropriately qualified contractor must undertake them under a clearly defined scope."],
             "asides": [{"kind": "callout", "tone": "accent", "paras": ["We do not promise universal compatibility, a particular room temperature or a percentage reduction in energy costs. Climate equipment is never treated as ordinary smart-plug switching."]}]},
            {"type": "scope", "id": "climate-boundaries", "h2": "What is included - and what is a separate service",
             "included": ["Compatibility assessment of existing equipment", "Manufacturer-app and platform setup", "Supported schedules and routines", "Network connectivity for the controller", "Testing and a practical handover"],
             "excluded": ["Air-conditioner installation or servicing", "Refrigerant or mechanical work", "Thermostat wiring and electrical work", "Guaranteed temperatures or energy savings", "Equipment that exposes no supported control"]},
            smart_process("climate-process"),
            {"type": "faqs", "id": "climate-faqs", "nav": "FAQs", "h2": "Climate control questions",
             "faqs": [("Do you install or service air conditioners?", "No. This service concerns compatible controls, apps, network connections and supported routines. Any required HVAC or electrical work must be completed by the appropriate specialist under a separately defined scope."),
                      ("Can a smart plug control my air conditioner?", "Not as a general assumption. Load characteristics, startup current, safe operation and manufacturer approval must be checked. Climate equipment may need a supported controller interface instead."),
                      ("Can I replace my thermostat with a smart one?", "Only where the control interface, electrical requirements and operating modes are compatible. Wiring changes are carried out by a qualified contractor."),
                      ("Will it work without the internet?", "Some local controls may continue; remote app access and cloud-based routines usually will not. We explain the dependencies of the agreed setup."),
                      ("Will this reduce my energy bill?", "We do not promise savings. Schedules and supported controls can help you manage use, but outcomes depend on the equipment and how it is used."),
                      ("My existing controller app stopped working. Can you help?", 'Yes, through <a href="/smart-home/setup-troubleshooting/">Smart Home Setup &amp; Troubleshooting</a>, where the equipment is supported.'),
                      SMART_FAQ_COST]},
            {"type": "related", "id": "climate-related", "h2": "Related services",
             "links": [("/smart-home/smart-utilities/", "Smart Utilities", "Plugs, sensors and selected controllers.", "Explore utilities"),
                       ("/smart-home/reliable-connectivity/", "Reliable Connectivity", "Signal where the controller is installed.", "Explore connectivity"),
                       ("/smart-home/#ecosystems", "Ecosystems &amp; Compatibility", "Platforms, hubs and standards explained.", "Check compatibility"),
                       ("/smart-home/setup-troubleshooting/", "Setup &amp; Troubleshooting", "Existing controllers that are not working.", "Get support")]},
        ],
        "enquiry": smart_enquiry("Check your climate equipment's compatibility", "Tell us the make and model of your air conditioners, thermostats or controllers, and what you would like to control.", "climate", "sm"),
    },
    {
        "route": "/smart-home/reliable-connectivity/", "prefix": "sn", "service": "connectivity",
        "label": "Reliable Connectivity", "crumb": "Reliable Connectivity",
        "title": "Smart Home WiFi & Connectivity Gauteng | CMAXX",
        "desc": "Plan the WiFi, access points, cabling and PoE behind a reliable smart home in Gauteng before adding more devices.",
        "eyebrow": "The network behind your smart home",
        "h1": "Reliable Smart-Home Connectivity in Gauteng",
        "sub": "A smart home is only as reliable as the network supporting it.",
        "hero_paras": ["Adding smart devices does not repair weak WiFi. A camera at the gate, a television upstairs and a controller inside a cupboard can have very different connection needs.",
                       "We assess where devices will operate, how they communicate and how much traffic the home will carry at busy times - then plan the WiFi, cabling and equipment to suit."],
        "micro": 'For a WiFi fault in an existing home, see <a href="/wifi-assessment-troubleshooting/">WiFi Assessment &amp; Troubleshooting</a>.',
        "img": "photo-1544197150-b99a580bb7a8", "alt": "Network switch with several Ethernet cables connected", "fallback": "The foundation every device relies on",
        "cta": "Discuss My Smart-Home Network", "enquiry_id": "smart-enquiry", "wa": "Hello CMAXX, I would like to discuss a smart-home project in Gauteng.", "parent": SMART_PARENT,
        "sections": [
            {"type": "split", "id": "connectivity-basics", "nav": "Home network basics", "h2": "How a home network is put together",
             "paras": ["The router manages traffic between your home and the internet; access points provide wireless connections around the property. Network switches provide wired ports, and structured cabling provides planned routes that are easier to document and maintain.",
                       "Coverage means the signal reaches the right places. Capacity means the network can handle the active devices and traffic in those places. A phone showing WiFi bars is not proof that a camera upload, several streams and a video call will work well together."],
             "asides": [{"kind": "list", "label": "Home network, simplified", "items": ["<strong>Router</strong> - traffic between the home and the internet", "<strong>Switch</strong> - wired ports for fixed equipment", "<strong>Access point</strong> - wireless connections around the property", "<strong>Compatible PoE device</strong> - data and power through one cable", "<strong>Wired TV or streamer</strong> - fixed equipment on Ethernet where practical"]}]},
            {"type": "cards", "id": "connectivity-design", "nav": "Design choices", "h2": "Design choices that affect reliability",
             "cards": [("Routers, access points and mesh", "A well-placed mesh system can help where new cabling is difficult, but its wireless links also need a good signal. Where practical, Ethernet backhaul connects units by cable."),
                       ("The right band for each device", "Many smart switches, plugs and sensors use 2.4 GHz; some cameras and TVs also support 5 GHz. We check the actual model rather than assume."),
                       ("Ethernet for fixed equipment", "Supported TVs, streamers, receivers, hubs and recorders often benefit from a cable connection."),
                       ("PoE and power budgets", "The device, switch or injector, cabling and available power budget must match. PoE does not power every appliance."),
                       ("Coverage where devices live", "Doors, gates, garages, entertainment areas and outbuildings - not only next to the router."),
                       ("Separation that still works", "A guest or isolated network can stop a phone, speaker and smart device finding each other. We plan permissions and test control.")]},
            {"type": "split", "id": "connectivity-homes", "nav": "Existing or new homes", "h2": "Existing homes and new builds",
             "paras": ["In an existing home, we start with a device and network survey, retain useful equipment and add cabling where it offers clear value. Access to ceilings, cupboards and outbuildings is assessed before promising a concealed installation.",
                       'For new builds and renovations, plan data outlets, access-point positions, television points, CCTV routes and an equipment-cabinet location while plans can still change. See <a href="/structured-cabling/">Structured Cabling</a>.'],
             "asides": [{"kind": "callout", "paras": ["Good planning makes later upgrades easier, but no device or standard can be guaranteed to remain supported forever. We favour documented routes, sensible capacity and a clear equipment record."], "cta": ("/smart-home/#internet-power-security", "Internet, power and outages")}]},
            {"type": "scope", "id": "connectivity-boundaries", "h2": "What is included - and what is a separate service",
             "included": ["Coverage and capacity assessment", "Router, access-point and switch recommendations", "Agreed cabling, PoE and equipment installation", "Network configuration for the agreed devices", "Testing and a documented handover"],
             "excluded": ["The internet service itself, which remains with your ISP", "Guaranteed speeds in every room", "Electrical work for cabinet power supplies", "Repairs to devices that are faulty", 'Ongoing network management unless separately agreed - see <a href="/managed-wifi/">Managed WiFi</a>']},
            smart_process("connectivity-process"),
            {"type": "faqs", "id": "connectivity-faqs", "nav": "FAQs", "h2": "Smart-home connectivity questions",
             "faqs": [("Do all smart-home devices require WiFi?", "No. Some use Ethernet, Bluetooth, Zigbee, Thread or another supported connection. The complete system may still need a compatible hub, controller and home network for app control, automation or remote access."),
                      ("Can CMAXX improve the WiFi before adding smart devices?", "Yes. Assessing the network is central to our approach. This helps separate network problems from device compatibility issues and avoids adding more products to an unsuitable connection."),
                      ("Should a smart TV use Ethernet or WiFi?", "Ethernet is often useful for a fixed TV or streamer. Well-designed WiFi may also be suitable. Neither method is an automatic guarantee of uninterrupted streaming."),
                      ("Is mesh WiFi enough?", "Sometimes. Mesh can help where cabling is difficult, but each unit needs a good connection to the next. Wired backhaul is preferable where practical."),
                      ("Why did my devices stop working on a guest network?", "Isolated networks can prevent phones and smart devices from discovering each other. Network settings must preserve the communication the selected system needs."),
                      SMART_FAQ_COST]},
            {"type": "related", "id": "connectivity-related", "h2": "Related services",
             "links": [("/home-wifi-solutions/", "Home WiFi Solutions", "Whole-home coverage and design.", "Explore Home WiFi"),
                       ("/wifi-assessment-troubleshooting/", "WiFi Assessment &amp; Troubleshooting", "Diagnosis for an existing network.", "Book an assessment"),
                       ("/structured-cabling/", "Structured Cabling", "Planned routes, outlets and cabinets.", "Explore cabling"),
                       ("/wifi-network-solutions/", "WiFi &amp; Network Solutions", "The wider network service.", "Explore WiFi services")]},
        ],
        "enquiry": smart_enquiry("Discuss your smart-home network", "Tell us about the home, where devices need to work and what problems you notice today.", "connectivity", "sn"),
    },
    {
        "route": "/smart-home/smart-utilities/", "prefix": "su", "service": "other_integration",
        "label": "Smart Utilities", "crumb": "Smart Utilities",
        "title": "Smart Plugs, Sensors & Utility Integration Gauteng | CMAXX",
        "desc": "Assess compatible smart plugs, sensors and selected irrigation or gate controllers for useful scheduling, monitoring and notifications in Gauteng homes.",
        "eyebrow": "Plugs, sensors and selected controllers",
        "h1": "Smart Utilities &amp; Sensor Integration in Gauteng",
        "sub": "Small, well-chosen integrations that make daily tasks easier without automating the entire property.",
        "hero_paras": ["We assess compatible smart plugs, sensors and controllers for useful scheduling, monitoring and notifications, then explain the equipment and installation limits.",
                       "We first define the safe, supported function rather than promising to make every appliance smart."],
        "micro": "Tell us which appliance, sensor or controller you have in mind. Assessment arrangements and any charges are confirmed before booking.",
        "img": "photo-1416879595882-3373a0480b5b", "alt": "Garden plants growing in a planted bed", "fallback": "Useful monitoring, safe boundaries",
        "cta": "Check a Device or Integration", "enquiry_id": "smart-enquiry", "wa": "Hello CMAXX, I would like to discuss a smart-home project in Gauteng.", "parent": SMART_PARENT,
        "sections": [
            {"type": "cards", "id": "utilities-uses", "nav": "Use cases", "h2": "Useful integrations to consider",
             "cards": [("Plugs and timers", "On/off control or scheduling for an approved non-critical load, such as a compatible lamp."),
                       ("Energy monitoring", "Supported devices can help you understand the equipment they actually measure - not the entire property."),
                       ("Leak and water sensors", "A compatible sensor may provide an alert; it does not automatically measure consumption or shut off the water."),
                       ("Irrigation controllers", "An existing controller may expose a supported interface for scheduling or notifications."),
                       ("Gate notifications", "Selected gate systems can provide supported status or authorised control, assessed against safety arrangements."),
                       ("Outdoor sensors", "Location, battery maintenance, protection and the route from sensor to hub to phone all affect the result.")]},
            {"type": "split", "id": "utilities-safety", "nav": "Safety boundary", "h2": "The safety boundary",
             "paras": ["Switching power does not give a conventional appliance new controls: an appliance may not restart safely or resume its previous setting when power returns. The plug's local model, load rating, appliance behaviour and manufacturer instructions must all be checked.",
                       "Professional planning is particularly useful where water, moving equipment or mains-powered loads are involved."],
             "asides": [{"kind": "callout", "tone": "accent", "h3": "Not generic smart-plug applications", "paras": ["Motors, pumps, air conditioners, heating appliances, high-startup-current equipment and safety-critical loads. Any required dedicated electrical control belongs with the appropriate electrical professional."]}]},
            {"type": "split", "id": "utilities-controllers", "nav": "Irrigation and gates", "h2": "Irrigation, gates and other controllers",
             "paras": ["An existing irrigation or gate system may expose a supported interface for scheduling, notification or authorised control. CMAXX can assess that integration opportunity.",
                       'Irrigation pipework, plumbing, motor installation, safety hardware and physical repairs remain outside the networking and configuration scope unless a separate specialist arrangement is agreed. <a href="/outdoor-wifi-solutions/">Outdoor WiFi Solutions</a> can help with connectivity around gates, gardens and outbuildings.'],
             "asides": [{"kind": "figure", "img": "photo-1600596542815-ffad4c1539a9", "alt": "Modern house with a landscaped garden", "fallback": "Gardens, gates and outbuildings"}]},
            {"type": "scope", "id": "utilities-boundaries", "h2": "What is included - and what is a separate service",
             "included": ["Compatibility and safety checks for the proposed device", "Setup of supported plugs, sensors and controllers", "Schedules, notifications and supported routines", "Connectivity for the agreed devices", "Testing and a practical handover"],
             "excluded": ["Plumbing, irrigation pipework or water shut-off valves", "Gate motor installation or repairs", "Electrical work for dedicated controls", "Billing-grade energy audits or guaranteed savings", 'Climate equipment - see <a href="/smart-home/climate-control/">Climate Control</a>']},
            smart_process("utilities-process"),
            {"type": "faqs", "id": "utilities-faqs", "nav": "FAQs", "h2": "Smart utilities questions",
             "faqs": [("Can a smart plug control my gate, pump or air conditioner?", "Not as a general assumption. Load characteristics, startup current, safe operation and manufacturer approval must be checked. These systems may need a supported controller interface and specialist installation."),
                      ("Will energy monitoring reduce my bill?", "It can help you understand the equipment being measured. A monitoring plug does not measure the whole property, and the information is not a guarantee of savings or a billing-grade audit."),
                      ("Will a leak sensor turn off my water?", "Not by itself. A compatible sensor may send an alert. Automatic shut-off needs a suitable valve installed by a plumber, which is outside this scope."),
                      ("Can you connect my irrigation controller to an app?", "If it exposes a supported interface, we can assess and configure scheduling or notifications. Pipework and plumbing remain separate."),
                      ("How often do sensor batteries need changing?", "It varies by device and how often it reports. We explain maintenance for the agreed devices at handover."),
                      SMART_FAQ_ELECTRICAL, SMART_FAQ_COST]},
            {"type": "related", "id": "utilities-related", "h2": "Related services",
             "links": [("/smart-home/climate-control/", "Climate Control", "Compatible heating and cooling control.", "Explore climate control"),
                       ("/outdoor-wifi-solutions/", "Outdoor WiFi", "Signal at gates, gardens and outbuildings.", "Explore outdoor WiFi"),
                       ("/smart-home/smart-security-access/", "Smart Security &amp; Access", "Cameras, doorbells and intercoms.", "Explore security"),
                       ("/smart-home/setup-troubleshooting/", "Setup &amp; Troubleshooting", "Existing devices that are not working.", "Get support")]},
        ],
        "enquiry": smart_enquiry("Check a device or integration", "Tell us which appliance, sensor or controller you have in mind and what you would like it to do.", "other_integration", "su"),
    },
]
