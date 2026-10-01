#!/usr/bin/env python3
"""Build "CMAXX Website (standalone).html" from src/.

The standalone file is a self-unpacking bundle: a gzip/base64 asset manifest
plus a JSON-encoded page template. This script keeps the manifest exactly as
it is and regenerates only the template from:

  src/base-template.html      the original 9-page site template (unchanged)
  src/partials/components.css shared cx- component styles
  src/pages/*.html            the new page bodies (hero ... final section)

and applies the site-wide connections (navigation bar, footer directory,
router, form behaviour) and the targeted bridge copy on existing pages that
the Managed WiFi and Smart Home developer briefs specify.

Usage:  python3 tools/build_site.py
"""
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "CMAXX Website (standalone).html"

WHATSAPP = "27832127065"   # published mobile 083 212 7065 (brief F4 / Part 09)
TEL = "tel:+27101403660"

# ---------------------------------------------------------------- pages ----
# route, screen label, browser title, page file, header jump links, header CTA
NEW_PAGES = [
    {
        "route": "/managed-wifi/",
        "label": "Managed WiFi",
        "title": "Managed WiFi & Network Support Gauteng | CMAXX",
        "desc": "Ongoing management and support for your agreed WiFi and internal network in Gauteng. Discuss your existing setup and request a network assessment.",
        "file": "managed-wifi.html",
        "nav": [("#managed-scope", "What we manage"), ("#environments", "Your environment"),
                ("#service-process", "How it works"), ("#managed-wifi-faqs", "FAQs")],
        "cta": ("#network-assessment", "Request a Network Assessment", None),
        "sticky": ("#network-assessment", "Request a Network Assessment", None,
                   "Hello CMAXX. I would like to discuss a network assessment."),
    },
    {
        "route": "/industries/student-accommodation/",
        "label": "Student Accommodation WiFi",
        "title": "Student Accommodation WiFi Gauteng | CMAXX",
        "desc": "WiFi planning, installation and ongoing network support for student accommodation in Gauteng. Discuss resident demand, shared areas and your existing setup.",
        "file": "student-accommodation.html",
        "nav": [("#student-requirements", "Requirements"), ("#student-assessment", "What we assess"),
                ("#student-management", "Ongoing support"), ("#student-faqs", "FAQs")],
        "cta": ("#network-assessment", "Request a Network Assessment", None),
        "sticky": ("#network-assessment", "Request a Network Assessment", None,
                   "Hello CMAXX. I would like to discuss a network assessment."),
    },
    {
        "route": "/smart-home/",
        "label": "Smart Home Services",
        "title": "Smart Home Installation Gauteng | CMAXX",
        "desc": "Smart home installation and integration across Gauteng. Connect compatible lighting, WiFi, cameras and entertainment. Request a CMAXX assessment.",
        "file": "smart-home.html",
        "nav": [("#smart-home-services", "Services"), ("#automation", "Routines"),
                ("#ecosystems", "Compatibility"), ("#smart-home-faqs", "FAQs")],
        "cta": ("#smart-home-enquiry", "Request a Smart Home Assessment", "new_smart_home"),
        "sticky": ("#smart-home-enquiry", "Request a Smart Home Assessment", "new_smart_home",
                   "Hello CMAXX, I would like to discuss a smart-home project in Gauteng."),
    },
    {
        "route": "/smart-home/smart-lighting-switches/",
        "label": "Smart Lighting & Switches",
        "title": "Smart Lighting & Switch Installation Gauteng | CMAXX",
        "desc": "Plan smart switches, lighting scenes and app or voice control in Gauteng. CMAXX checks compatibility, configures controls and explains your installation options.",
        "file": "smart-lighting-switches.html",
        "nav": [("#lighting-options", "Choices"), ("#lighting-assessment", "What we check"),
                ("#lighting-routines", "Scenes"), ("#lighting-faqs", "FAQs")],
        "cta": ("#lighting-enquiry", "Request a Lighting Assessment", "lighting"),
        "sticky": ("#lighting-enquiry", "Request a Lighting Assessment", "lighting",
                   "Hello CMAXX, I would like to discuss compatible smart lighting and switches in Gauteng."),
    },
    {
        "route": "/smart-home/setup-troubleshooting/",
        "label": "Smart Home Setup & Troubleshooting",
        "title": "Smart Home Setup & Troubleshooting Gauteng | CMAXX",
        "desc": "Smart devices offline or routines not working? CMAXX provides supported smart-home setup and troubleshooting in Gauteng, including WiFi and app checks.",
        "file": "setup-troubleshooting.html",
        "nav": [("#support-symptoms", "Problems"), ("#support-diagnosis", "Diagnosis"),
                ("#support-preparation", "Before a visit"), ("#support-faqs", "FAQs")],
        "cta": ("#support-enquiry", "Request Smart Home Support", "support"),
        "sticky": ("#support-enquiry", "Request Smart Home Support", "support",
                   "Hello CMAXX, I need help with supported smart-home setup or troubleshooting in Gauteng."),
    },
]

sys.path.insert(0, str(SRC))
import subpages  # noqa: E402


def _subpage_config(sp, cta_service=None):
    """Header/sticky/meta config for a generated sub-page."""
    nav = [("#" + s["id"], s["nav"]) for s in sp["sections"] if s.get("nav")][:4]
    eid = "#" + sp["enquiry_id"]
    return {
        "route": sp["route"], "label": sp["label"], "title": sp["title"], "desc": sp["desc"],
        "body": subpages.render_body(sp), "nav": nav,
        "cta": (eid, sp["cta"], cta_service),
        "sticky": (eid, sp["cta"], cta_service, sp["wa"]),
    }


NEW_PAGES += [_subpage_config(sp) for sp in subpages.MANAGED_SUBPAGES]
NEW_PAGES += [_subpage_config(sp, sp["service"]) for sp in subpages.SMART_SUBPAGES]

# Site navigation: (group, [(route, label)])
SITE_NAV = [
    ("WiFi & Network", [
        ("/wifi-network-solutions/", "WiFi & Network Solutions"),
        ("/home-wifi-solutions/", "Home WiFi"),
        ("/business-wifi-solutions/", "Business & Office WiFi"),
        ("/wifi-assessment-troubleshooting/", "Assessment & Troubleshooting"),
        ("/outdoor-wifi-solutions/", "Outdoor WiFi"),
        ("/event-wifi-solutions/", "Event WiFi"),
    ]),
    ("Managed WiFi", [
        ("/managed-wifi/", "Managed WiFi"),
        ("/managed-wifi/businesses-offices/", "Businesses & Offices"),
        ("/managed-wifi/restaurants-cafes/", "Restaurants & Cafes"),
        ("/managed-wifi/retail-premises/", "Retail & Customer-Facing Premises"),
        ("/managed-wifi/schools/", "Schools & Training Facilities"),
        ("/managed-wifi/residential-estates/", "Residential Estates"),
        ("/managed-wifi/events/", "Event Venues & Events"),
        ("/managed-wifi/public-facilities/", "Community & Public Facilities"),
    ]),
    ("Smart Home", [
        ("/smart-home/", "Smart Home Services"),
        ("/smart-home/smart-lighting-switches/", "Smart Lighting & Switches"),
        ("/smart-home/connected-entertainment/", "Connected Entertainment"),
        ("/smart-home/smart-security-access/", "Smart Security & Access"),
        ("/smart-home/climate-control/", "Climate Control"),
        ("/smart-home/reliable-connectivity/", "Reliable Connectivity"),
        ("/smart-home/smart-utilities/", "Smart Utilities"),
        ("/smart-home/setup-troubleshooting/", "Setup & Troubleshooting"),
    ]),
    ("Infrastructure & IT", [
        ("/structured-cabling/", "Structured Cabling"),
        ("/cctv-security-solutions/", "CCTV & Security"),
        ("/cloud-microsoft-365/", "Cloud & Microsoft 365"),
    ]),
    ("Industries", [
        ("/industries/student-accommodation/", "Student Accommodation WiFi"),
    ]),
]

# Desktop bar shows the main entry point of each cluster plus the new pages.
SITEBAR_PRIMARY = [
    ("/wifi-network-solutions/", "WiFi & Network"),
    ("/managed-wifi/", "Managed WiFi"),
    ("/smart-home/", "Smart Home"),
    ("/structured-cabling/", "Structured Cabling"),
    ("/cctv-security-solutions/", "CCTV & Security"),
    ("/cloud-microsoft-365/", "Cloud & Microsoft 365"),
    ("/industries/student-accommodation/", "Student Accommodation"),
]

# Which cluster entry is "current" for each page in the desktop bar.
CLUSTER_OF = {
    "/home-wifi-solutions/": "/wifi-network-solutions/",
    "/business-wifi-solutions/": "/wifi-network-solutions/",
    "/wifi-assessment-troubleshooting/": "/wifi-network-solutions/",
    "/outdoor-wifi-solutions/": "/wifi-network-solutions/",
    "/event-wifi-solutions/": "/wifi-network-solutions/",
    "/smart-home/smart-lighting-switches/": "/smart-home/",
    "/smart-home/setup-troubleshooting/": "/smart-home/",
}
CLUSTER_OF.update({sp["route"]: "/managed-wifi/" for sp in subpages.MANAGED_SUBPAGES})
CLUSTER_OF.update({sp["route"]: "/smart-home/" for sp in subpages.SMART_SUBPAGES})

ROUTE_ALIASES = {
    "/": "/wifi-network-solutions/",
    "/services/": "/wifi-network-solutions/",
    # The WordPress cabling slug in the briefs; this build's cabling page lives at /structured-cabling/.
    "/infrastructure-cabling/": "/structured-cabling/",
}


def esc(s):
    return html.escape(s, quote=True)


def unsplash(photo_id):
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=1200&q=70"


def wa(text):
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"


# ------------------------------------------------------------ fragments ----
def sitebar(route):
    current = CLUSTER_OF.get(route, route)
    links = []
    for href, label in SITEBAR_PRIMARY:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{esc(label)}</a>')
    groups = []
    for group, items in SITE_NAV:
        groups.append(f'<li class="cx-sitebar-group">{esc(group)}</li>')
        for href, label in items:
            cur = ' aria-current="page"' if href == route else ""
            groups.append(f'<li><a href="{href}"{cur}>{esc(label)}</a></li>')
    return (
        '<nav class="cx-sitebar" aria-label="Site">'
        '<div class="cx-sitebar-in"><span class="cx-sitebar-label">Services</span>'
        + "".join(links)
        + '<a href="/contact/" style="margin-left: auto;">Contact</a></div>'
        '<details class="cx-sitebar-mobile"><summary>All services &amp; pages</summary><ul>'
        + "".join(groups)
        + '<li class="cx-sitebar-group">Company</li><li><a href="/contact/">Contact</a></li>'
        '<li><a href="/areas-we-serve/">Areas We Serve</a></li></ul></details>'
        "</nav>"
    )


def footer_directory():
    cols = []
    for group, items in SITE_NAV:
        lis = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for h, l in items)
        cols.append(f"<div><h2>{esc(group)}</h2><ul>{lis}</ul></div>")
    cols.append(
        "<div><h2>Company</h2><ul>"
        '<li><a href="/contact/">Contact</a></li>'
        '<li><a href="/areas-we-serve/">Areas We Serve</a></li>'
        '<li><a href="/our-work/">Case Studies</a></li>'
        '<li><a href="/policy-popia/">Privacy Policy &amp; POPIA Notice</a></li>'
        "</ul></div>"
    )
    return f'<nav class="cx-footdir" aria-label="Site directory">{"".join(cols)}</nav>'


def header(page):
    nav = "".join(
        f'<a href="{h}" style="text-decoration: none; color: var(--color-text);">{esc(l)}</a>'
        for h, l in page["nav"])
    href, label, service = page["cta"]
    svc = f' data-service="{service}"' if service else ""
    return f'''  <header style="position: sticky; top: 0; z-index: 50; background: color-mix(in srgb, var(--color-bg) 92%, transparent); backdrop-filter: blur(10px); border-bottom: 1px solid var(--color-divider);">
    {sitebar(page["route"])}
    <div style="max-width: 1240px; margin: 0 auto; padding: 14px 24px; display: flex; align-items: center; gap: 28px; flex-wrap: wrap;">
      <a href="/" style="font-family: var(--font-heading); font-size: 21px; text-decoration: none; color: var(--color-text); margin-right: auto; display: flex; align-items: center; gap: 10px;">
        <span style="width: 34px; height: 34px; border-radius: 999px; background: var(--color-accent); color: var(--color-bg); display: grid; place-items: center; font-size: 15px;">C</span>
        CMAXX <span style="color: var(--color-accent-700);">WiFi Solutions</span>
      </a>
      <nav class="cx-headnav" aria-label="Page sections" style="display: flex; align-items: center; gap: 22px; flex-wrap: wrap; font-size: 14.5px;">{nav}</nav>
      <div style="display: flex; align-items: center; gap: 10px;">
        <a href="{TEL}" style="font-size: 14.5px; text-decoration: none; color: var(--color-text); white-space: nowrap;">010 140 3660</a>
        <a class="btn btn-primary" href="{href}"{svc} style="font-size: 14.5px; padding: 10px 20px; white-space: nowrap;">{esc(label)}</a>
      </div>
    </div>
  </header>
'''


def footer():
    return f'''  <footer style="margin-top: 80px; padding: 44px 24px 120px; border-top: 1px solid var(--color-divider);">
    {footer_directory()}
    <div style="max-width: 1240px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 20px 40px; align-items: center; font-size: 14px; color: var(--color-neutral-700);">
      <span style="font-family: var(--font-heading); font-size: 17px; color: var(--color-text); margin-right: auto;">CMAXX WiFi Solutions</span>
      <span>Midrand, Gauteng</span>
      <a href="{TEL}">010 140 3660</a>
      <a href="/contact/">Contact CMAXX</a>
    </div>
  </footer>
'''


def sticky(page):
    href, label, service, wa_text = page["sticky"]
    svc = f' data-service="{service}"' if service else ""
    return f'''  <div class="cx-sticky" data-sticky="">
    <a class="btn btn-primary" href="{href}"{svc}>{esc(label)}</a>
    <a class="btn btn-secondary" href="{wa(wa_text)}" data-contact="whatsapp">WhatsApp</a>
    <a class="btn btn-secondary" href="{TEL}" data-contact="phone">Call 010 140 3660</a>
  </div>
'''


# ---------------------------------------------------------------- forms ----
NETWORK_PROPERTY_TYPES = [
    ("business", "Business or office"), ("restaurant", "Restaurant or cafe"),
    ("retail", "Retail premises"), ("student", "Student accommodation"),
    ("estate", "Estate communal areas"), ("school", "School or training facility"),
    ("public", "Community or public venue"), ("home", "Home"), ("event", "Event"),
    ("other", "Other or not sure"),
]
SMART_SERVICES = [
    ("new_smart_home", "New smart-home project"), ("lighting", "Smart lighting and switches"),
    ("connectivity", "WiFi and network for smart devices"), ("support", "Existing-device setup or troubleshooting"), ("entertainment", "Connected entertainment"),
    ("security", "Cameras/intercom integration"), ("climate", "Compatible climate integration"),
    ("other_integration", "Smart plugs, sensors or other integration"), ("not_sure", "Other / not sure"),
]
SMART_PROPERTY_TYPES = ["House", "Apartment / townhouse", "New build / renovation",
                        "Guest house / lodge / short-stay property", "Other"]


def field(fid, label, control, required=False, helptext=None, full=False, req_note=None):
    note = req_note or ("Required" if required else "Optional")
    desc = []
    help_html = ""
    if helptext:
        help_html = f'<p class="cx-help" id="{fid}-help">{esc(helptext)}</p>'
        desc.append(f"{fid}-help")
    desc.append(f"{fid}-err")
    control = control.replace("{DESC}", " ".join(desc))
    cls = "cx-field cx-field--full" if full else "cx-field"
    return (f'<div class="{cls}"><label for="{fid}">{esc(label)} <span class="cx-req">({note})</span></label>'
            f'{control}{help_html}<p class="cx-err" id="{fid}-err"></p></div>')


def text_input(fid, name, kind="text", autocomplete=None, required=False):
    ac = f' autoComplete="{autocomplete}"' if autocomplete else ""
    req = ' aria-required="true"' if required else ""
    return (f'<input class="input" id="{fid}" name="{name}" type="{kind}"{ac}{req} maxLength="200" '
            f'aria-describedby="{{DESC}}">')


def select(fid, name, options, default="", required=False, placeholder="Please choose"):
    req = ' aria-required="true"' if required else ""
    opts = f'<option value="">{esc(placeholder)}</option>' + "".join(
        f'<option value="{v}">{esc(l)}</option>' for v, l in options)
    return (f'<select class="input" id="{fid}" name="{name}"{req} defaultValue="{default}" '
            f'aria-describedby="{{DESC}}">{opts}</select>')


def textarea(fid, name, required=False):
    req = ' aria-required="true"' if required else ""
    return (f'<textarea class="input" id="{fid}" name="{name}"{req} maxLength="3000" rows="5" '
            f'aria-describedby="{{DESC}}"></textarea>')


def form_shell(fid, kind, service_ctx, title, intro, fields_html, privacy, submit, below):
    return f'''<form class="cx-form" id="{fid}" data-cx-form="{kind}" data-context="{service_ctx}" action="/contact/" method="post" aria-labelledby="{fid}-title">
            <h3 id="{fid}-title">{esc(title)}</h3>
            <p class="cx-form-intro">{esc(intro)}</p>
            <div class="cx-summary" role="alert" tabIndex="-1" data-summary=""></div>
            <div class="cx-fields">{fields_html}</div>
            <p class="cx-privacy">{privacy}</p>
            <button class="btn btn-primary cx-submit" type="submit">{esc(submit)}</button>
            <p class="cx-below">{esc(below)}</p>
            <div class="cx-status" role="status" aria-live="polite" data-status=""></div>
          </form>'''


def form_network(variant, prefix=None):
    """variant: 'managed' (no preselection) or a property-type value to preselect."""
    p = prefix or ("sa" if variant == "student" else "mw")
    fid = f"{p}-form"
    default_type = "" if variant == "managed" else variant
    intro = ("Tell us where the property is, how it is used and what needs attention. Approximate occupancy is enough for the initial enquiry."
             if variant == "student" else
             "Share the basics below. You do not need a technical equipment list to start the conversation.")
    def rid(v):
        return f' id="{p}-method"' if v == "email" else ""
    radios = "".join(
        f'<label class="radio"><input type="radio"{rid(v)} name="contact_method" value="{v}" '
        f'aria-describedby="{p}-method-err"><span class="dot"></span>{esc(l)}</label>'
        for v, l in (("email", "Email"), ("phone", "Phone call"), ("whatsapp", "WhatsApp")))
    f = [
        field(f"{p}-name", "Full name", text_input(f"{p}-name", "full_name", autocomplete="name", required=True), required=True),
        field(f"{p}-org", "Organisation or property name", text_input(f"{p}-org", "organisation", autocomplete="organization")),
        field(f"{p}-type", "Type of property or organisation",
              select(f"{p}-type", "property_type", NETWORK_PROPERTY_TYPES, default_type, required=True), required=True),
        field(f"{p}-area", "Suburb or town", text_input(f"{p}-area", "suburb", autocomplete="address-level2", required=True), required=True),
        field(f"{p}-msg", "What would you like help with?", textarea(f"{p}-msg", "message", required=True), required=True,
              helptext="Tell us what is happening, where it happens and what you would like to improve.", full=True),
        (f'<fieldset class="cx-fieldset cx-field--full" data-group="contact_method"><legend>How should we contact you? '
         f'<span class="cx-req">(Required)</span></legend><div class="cx-radios">{radios}</div>'
         f'<p class="cx-err" id="{p}-method-err"></p></fieldset>'),
        field(f"{p}-email", "Email address", text_input(f"{p}-email", "email", "email", "email"),
              req_note="Required for an email response"),
        field(f"{p}-phone", "Contact number", text_input(f"{p}-phone", "phone", "tel", "tel"),
              req_note="Required for a call or WhatsApp"),
    ]
    if variant == "student":
        f.append(field(f"{p}-rooms", "Approximate rooms and residents", text_input(f"{p}-rooms", "rooms_residents"),
                       helptext="Approximate numbers only. Please do not include residents' personal details."))
    more = [
        field(f"{p}-isp", "Current internet provider", text_input(f"{p}-isp", "isp"),
              helptext="“Not sure” is a perfectly good answer."),
        field(f"{p}-users", "Approximate number of users and devices", text_input(f"{p}-users", "users_devices"),
              helptext="An estimate is fine; an exact count is not necessary."),
        field(f"{p}-floors", "Number of buildings or floors", text_input(f"{p}-floors", "buildings_floors")),
        field(f"{p}-time", "Preferred time to contact you", text_input(f"{p}-time", "preferred_time"),
              helptext="A preference only; appointment times are confirmed separately."),
    ]
    f.append('<details class="cx-more"><summary>Add more property details (optional)</summary>'
             f'<div class="cx-fields">{"".join(more)}</div></details>')
    privacy = ("CMAXX WiFi Solutions uses the information you provide to respond to your enquiry and discuss the requested service. "
               "Please do not include passwords, identity documents, payment details, tenant records or private information about other people. "
               'Read our <a href="/policy-popia/">Privacy Policy &amp; POPIA Notice</a> for more about how information is handled.')
    return form_shell(fid, "network", variant, "Request a Network Assessment", intro, "".join(f), privacy,
                      "Request a Network Assessment",
                      "Submitting this form requests a discussion. It does not confirm an appointment, a free assessment or a service agreement.")


SMART_FORM_TEXT = {
    "new_smart_home": ("sh", "Send Smart Home Enquiry", "Smart home enquiry",
                       "Keep it simple: tell us what you want to achieve. We will discuss the details with you."),
    "lighting": ("sl", "Send Lighting Enquiry", "Lighting enquiry",
                 "Tell us which rooms and lights you want to improve."),
    "support": ("ss", "Send Support Enquiry", "Support enquiry",
                "Tell us what is not working and which devices are involved."),
}


def form_smart(service, prefix=None):
    p, submit, title, intro = SMART_FORM_TEXT.get(service, (
        "sx", "Send Smart Home Enquiry", "Smart home enquiry",
        "Tell us what you want to achieve. You do not need a finished equipment list."))
    p = prefix or p
    fid = f"{p}-form"
    f = [
        field(f"{p}-name", "Full name", text_input(f"{p}-name", "full_name", autocomplete="name", required=True), required=True),
        field(f"{p}-phone", "Contact number", text_input(f"{p}-phone", "phone", "tel", "tel", required=True), required=True),
        field(f"{p}-email", "Email address", text_input(f"{p}-email", "email", "email", "email")),
        field(f"{p}-area", "Suburb / area", text_input(f"{p}-area", "suburb", autocomplete="address-level2", required=True), required=True),
        field(f"{p}-service", "What do you need help with?",
              select(f"{p}-service", "service", SMART_SERVICES, service, required=True), required=True),
        field(f"{p}-ptype", "Property type",
              select(f"{p}-ptype", "property_type", [(t, t) for t in SMART_PROPERTY_TYPES], "")),
        field(f"{p}-msg", "Tell us about your project or problem", textarea(f"{p}-msg", "message", required=True), required=True,
              helptext="Describe what you want to achieve or what is not working. Do not include passwords, access codes or private footage.",
              full=True),
        field(f"{p}-models", "Existing brands or model numbers", text_input(f"{p}-models", "models"),
              helptext="Model names are helpful; login details and setup QR codes are not required.", full=True),
    ]
    privacy = ('We use your enquiry details to respond to your request and discuss the relevant service. Please read our '
               '<a href="/policy-popia/">Privacy &amp; POPIA Notice</a>. Do not send passwords, access codes or private camera footage through this form.')
    return form_shell(fid, "smart", service, title, intro, "".join(f), privacy, submit,
                      "Submitting this form does not confirm an appointment or final quotation.")


def expand(body):
    body = re.sub(r"\[\[U:([\w-]+)\]\]", lambda m: unsplash(m.group(1)), body)
    body = re.sub(r"\[\[WA:([^\]]+)\]\]", lambda m: esc(wa(html.unescape(m.group(1)))), body)
    body = re.sub(r"\[\[FORM_NETWORK:(\w+)(?::(\w+))?\]\]", lambda m: form_network(m.group(1), m.group(2)), body)
    body = re.sub(r"\[\[FORM_SMART:(\w+)(?::(\w+))?\]\]", lambda m: form_smart(m.group(1), m.group(2)), body)
    left = re.findall(r"\[\[[^\]]*\]\]", body)
    if left:
        sys.exit(f"Unexpanded markers: {left}")
    return body


def build_page(page):
    body = expand(page["body"] if "body" in page else (SRC / "pages" / page["file"]).read_text())
    return (
        f'<section data-page="{page["route"]}" data-screen-label="{esc(page["label"])}" '
        f'data-title="{esc(page["title"])}" data-description="{esc(page["desc"])}" style="display: none;">\n\n'
        '<div style="background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); min-height: 100vh;">\n\n'
        + header(page) + "\n" + body + "\n" + footer() + "\n" + sticky(page) +
        "</div>\n\n</section>\n"
    )


# ------------------------------------------------- existing-page edits ----
def replace_once(s, old, new, what):
    n = s.count(old)
    if n != 1:
        sys.exit(f"[{what}] expected exactly one match, found {n}")
    return s.replace(old, new)


def insert_at_section_end(t, section_id, block, what):
    start = t.find(f'<section id="{section_id}"')
    if start < 0:
        sys.exit(f"[{what}] section {section_id} not found")
    end = t.find("\n    </div>\n  </section>", start)
    if end < 0:
        sys.exit(f"[{what}] end of section {section_id} not found")
    return t[:end] + "\n      " + block + t[end:]


def bridge(body, tone="green", heading=None):
    bg = {"green": "var(--color-accent-2-100)", "accent": "var(--color-accent-100)",
          "line": "transparent"}[tone]
    border = "border: 1px solid var(--color-divider); " if tone == "line" else ""
    h = (f'<h2 style="font-size: clamp(24px, 2.4vw, 30px); line-height: 1.12; margin: 0 0 10px;">{heading}</h2>'
         if heading else "")
    return (f'<div class="cx-bridge" style="background: {bg}; {border}border-radius: 30px; padding: 26px 30px; '
            f'margin-top: 26px; font-size: 15.5px;">{h}<p style="margin: 0; max-width: 78ch;">{body}</p></div>')


# Targeted amendments: Managed WiFi brief section E4 and Smart Home brief Part 06
# ("links back from existing CMAXX pages"). Each is a small contextual block
# inside an existing section, so no existing page gains a section.
BRIDGES = [
    # WiFi & Network Solutions parent
    ("p0-process", bridge('An installation delivers an agreed network project. Where you also need a continuing support relationship, explore <a href="/managed-wifi/">ongoing Managed WiFi support</a>. The management scope, equipment responsibilities and support arrangements are agreed separately from the installation unless your proposal states otherwise.', "green", "Support after the installation"), "E4.1"),
    ("p0-related", bridge('Planning connected lighting, entertainment or security at home? Our <a href="/smart-home/">Smart Home Services</a> combine compatible-device integration with the network supporting it.', "line"), "SH-WN"),
    # Home WiFi
    ("p1-solution", bridge('A reliable home network also supports compatible lighting, controls and connected devices. Explore our <a href="/smart-home/">Smart Home Services</a> to plan the integration around it.', "line"), "SH-HW"),
    ("p1-process", bridge('For a property that needs a continuing network-support arrangement, ask about <a href="/managed-wifi/">Managed WiFi support</a>. Suitability and the covered equipment are assessed separately; not every household needs an ongoing service.'), "E4.3-home"),
    # Business & Office WiFi
    ("p2-process", bridge('Installation and ongoing support answer different needs. Our <a href="/managed-wifi/">ongoing Managed WiFi support</a> covers the continuing responsibilities agreed for your internal network. For property-specific resident requirements, explore <a href="/industries/student-accommodation/">student accommodation WiFi solutions</a>.', "green", "Need someone to manage the network after handover?"), "E4.2"),
    ("p2-environments", bridge('For suitable accommodation projects, <a href="/smart-home/">Smart Home Services</a> can be assessed alongside guest networking, with separate permissions for property controls.', "line"), "SH-BW"),
    # WiFi Assessment & Troubleshooting
    ("p3-symptoms", bridge('When the network is working but supported devices or routines still fail, our <a href="/smart-home/setup-troubleshooting/">Smart Home Setup &amp; Troubleshooting</a> service can assess the configuration and integration.', "line"), "SH-WT"),
    ("p3-process", bridge('Where a recurring support relationship would help after the initial fault is addressed, explore <a href="/managed-wifi/">ongoing network management</a>. The assessment itself does not automatically establish a managed-service agreement.'), "E4.3-assessment"),
    # Outdoor WiFi
    ("p4-options", bridge('Outdoor connectivity may support selected cameras, sensors and controls. Discuss <a href="/smart-home/">compatible smart-home integration</a> alongside the network design.', "line"), "SH-OW"),
    ("p4-process", bridge('For installed infrastructure that needs continuing care, discuss <a href="/managed-wifi/">management of your agreed network</a>. Outdoor coverage, equipment and attendance responsibilities must be included explicitly in the scope.'), "E4.3-outdoor"),
    # Event WiFi
    ("p5-process", bridge('A temporary event network is planned for a specific date, venue and requirement. A venue that also needs year-round support can explore <a href="/managed-wifi/">ongoing venue network management</a>. Event deployment, attendance and temporary equipment are not automatically included in a normal recurring management agreement.', "green", "Permanent venue support is a separate decision"), "E4.5"),
    # Structured Cabling
    ("p6-use-cases", bridge('For new homes and renovations, combine network points, access-point locations and camera routes with practical <a href="/smart-home/">smart-home planning</a>.', "line"), "SH-SC"),
    ("p6-process", bridge('Once the physical infrastructure is in place, <a href="/managed-wifi/">agreed ongoing network management</a> can provide continuing support for the specified network environment. A managed-service fee does not automatically include every future cable repair or additional data point.'), "E4.6-cabling"),
    # CCTV & Security
    ("p7-solutions", bridge('Selected camera, intercom and notification functions can form part of a wider connected property. Explore our <a href="/smart-home/">Smart Home Services</a> to discuss compatible integration.', "line"), "SH-CS"),
    ("p7-network", bridge('Camera-system support and <a href="/managed-wifi/">managed internal-network support</a> have different responsibilities. Where both are required, the proposal should identify the camera, recording, access and network work covered by each service.'), "E4.6-cctv"),
    # Cloud & Microsoft 365
    ("p8-intro", bridge('Online applications depend on an appropriate internet connection and internal network. <a href="/managed-wifi/">Managed internal-network support</a> can address the agreed connectivity infrastructure, but it does not replace Microsoft 365 administration, endpoint support or application-provider support.'), "E4.6-cloud"),
    ("p8-intro", bridge('A home-office project may also need <a href="/smart-home/">connected-home networking and integration</a>. Keep that scope separate from Microsoft 365 and productivity support.', "line"), "SH-IT"),
]

# WiFi parent card summaries replaced per brief E4.1 (business/event/assessment).
SUMMARY_EDITS = [
    ('<h3 style="font-size: 23px; margin: 6px 0 0;">Business &amp; Office WiFi Solutions</h3>\n          <p style="margin: 0; font-size: 15.5px; color: var(--color-neutral-800);">Professionally designed commercial networks supporting users, applications, guest access, security and future growth.</p>',
     '<h3 id="business-office-wifi" style="font-size: 23px; margin: 6px 0 0;">Business &amp; Office WiFi Solutions</h3>\n          <p style="margin: 0; font-size: 15.5px; color: var(--color-neutral-800);">We design and install workplace WiFi and internal networks around the building, users, applications and existing infrastructure. Discuss a new setup, an upgrade or a targeted improvement, with ongoing support available under a separately agreed scope.</p>',
     "E4.1-business"),
    ('<p style="margin: 0; font-size: 15.5px; color: var(--color-neutral-800);">Temporary network infrastructure planned around the event venue, backhaul, attendees, devices and applications.</p>',
     '<p style="margin: 0; font-size: 15.5px; color: var(--color-neutral-800);">Temporary WiFi for conferences, exhibitions and other events, planned around the venue, expected usage, available internet feed, power and agreed event support.</p>',
     "E4.1-event"),
    ('<p style="margin: 0; font-size: 15.5px; color: var(--color-neutral-800);">Diagnosis of slow WiFi, dead zones, disconnections, poor roaming, cabling problems and unexplained performance issues.</p>',
     '<p style="margin: 0; font-size: 15.5px; color: var(--color-neutral-800);">An assessment helps identify likely network constraints and the appropriate next steps. The checks, access requirements, deliverables and any charges depend on the agreed assessment scope.</p>',
     "E4.1-assessment"),
]


def amend_existing_pages(t):
    for old, new, what in SUMMARY_EDITS:
        t = replace_once(t, old, new, what)
    for section_id, block, what in BRIDGES:
        t = insert_at_section_end(t, section_id, block, what)
    return t


# ------------------------------------------------------------- router ----
ROUTER_OLD_START = "  componentDidMount() {"
ROUTER_OLD_END = "  cctvRecommend() {"


def router_js():
    routes = {r: r for r in [
        "/wifi-network-solutions/", "/home-wifi-solutions/", "/business-wifi-solutions/",
        "/wifi-assessment-troubleshooting/", "/outdoor-wifi-solutions/", "/event-wifi-solutions/",
        "/structured-cabling/", "/cctv-security-solutions/", "/cloud-microsoft-365/"]}
    for p in NEW_PAGES:
        routes[p["route"]] = p["route"]
    routes.update(ROUTE_ALIASES)
    return (SRC / "partials" / "router.js").read_text().replace("__ROUTES__", json.dumps(routes, indent=2).replace("\n", "\n    "))


# --------------------------------------------------------------- build ----
def main():
    t = (SRC / "base-template.html").read_text()
    css = (SRC / "partials" / "components.css").read_text()

    # 1. shared component styles
    t = replace_once(t, "</helmet>", f"<style>\n{css}\n</style>\n</helmet>", "css")

    # 2. site nav bar in every existing page header + footer directory
    def per_page(m):
        block = m.group(0)
        route = re.search(r'data-page="([^"]+)"', block).group(1)
        block = re.sub(r'(<header style="position: sticky;[^>]*>)', lambda h: h.group(1) + "\n    " + sitebar(route), block, count=1)
        block = re.sub(r'(<footer style="[^"]*">)', lambda f: f.group(1) + "\n    " + footer_directory(), block, count=1)
        label = re.search(r'data-screen-label="([^"]+)"', block).group(1)
        block = block.replace(f'data-screen-label="{label}"', f'data-screen-label="{label}" data-title="{label} | CMAXX WiFi Solutions"', 1)
        return block
    t, n = re.subn(r'<section data-page="[^"]+".*?\n</section>\n', per_page, t, flags=re.S)
    if n != 9:
        sys.exit(f"expected 9 existing pages, found {n}")

    # 3. targeted bridge copy on existing pages
    t = amend_existing_pages(t)

    # 4. new pages
    pages = "\n".join(build_page(p) for p in NEW_PAGES)
    t = replace_once(t, "\n</div>\n</x-dc>", "\n" + pages + "\n</div>\n</x-dc>", "pages")

    # 5. router + behaviour
    a = t.index(ROUTER_OLD_START)
    b = t.index(ROUTER_OLD_END)
    t = t[:a] + router_js() + "\n" + t[b:]

    # 6. site-level title/description
    t = t.replace("<title>CMAXX WiFi Solutions | WiFi, Cabling, CCTV &amp; Cloud Services in Gauteng</title>",
                  "<title>CMAXX WiFi Solutions | WiFi, Managed WiFi, Smart Home, Cabling, CCTV &amp; Cloud in Gauteng</title>", 1)

    if "{{" in "".join(build_page(p) for p in NEW_PAGES):
        sys.exit("template interpolation braces found in new pages")

    # 7. write template back into the bundle
    out = OUT.read_text()
    m = re.search(r'(<script type="__bundler/template">\s*)(.*?)(\s*</script>)', out, re.S)
    encoded = json.dumps(t).replace("</", "<\\/")
    out = out[:m.start(2)] + encoded + out[m.end(2):]
    OUT.write_text(out)
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "template.html").write_text(t)
    print(f"wrote {OUT.name}: template {len(t):,} chars, {len(NEW_PAGES)} new pages")


if __name__ == "__main__":
    main()
