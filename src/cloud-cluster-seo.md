# Cloud & Microsoft 365 cluster — per-page SEO specification

The five Cloud & Microsoft 365 child pages are built as `data-page` sections
inside the single design-canvas document (`src/site.dc.html`, packed into
`CMAXX Website (standalone).html`). One document cannot carry six titles, six
meta descriptions, six canonicals or six schema blocks, so the per-page metadata
below is specified here for the WordPress implementation rather than faked in
the prototype.

Everything else in the brief's publishing checklist — the mandatory section
order per blueprint, one H1 per page, crawlable `<a href>` links with
descriptive anchor text, breadcrumbs on every child, server-rendered FAQ copy in
accessible accordions, unique copy per page, service-specific CTAs and the
accuracy guardrails — is implemented in the pages themselves.

## Pages

| # | Page | Slug |
| --- | --- | --- |
| Parent | Cloud & Microsoft 365 Services | `/cloud-microsoft-365/` |
| 1 | Microsoft 365 Setup & Migration | `/cloud-microsoft-365/microsoft-365-setup-migration/` |
| 2 | Microsoft 365 Support & Administration | `/cloud-microsoft-365/microsoft-365-support/` |
| 3 | Microsoft Teams & SharePoint Solutions | `/cloud-microsoft-365/teams-sharepoint/` |
| 4 | Business Email & Exchange Online | `/cloud-microsoft-365/business-email-exchange-online/` |
| 5 | Business Backup & NAS Storage | `/cloud-microsoft-365/business-backup-nas/` |

Create the five as WordPress children of the existing Cloud & Microsoft 365
page, keeping the parent URL. Set 301 redirects for any test or previous slugs.

## 1. Microsoft 365 Setup & Migration

- **URL** `/cloud-microsoft-365/microsoft-365-setup-migration/`
- **SEO title** Microsoft 365 Setup & Migration Gauteng | CMAXX
- **Meta description** Plan and migrate business email, users, files and Microsoft 365 services with structured support from CMAXX across Gauteng.
- **H1** Microsoft 365 Setup & Migration for Gauteng Businesses
- **Keyword theme** Microsoft 365 migration Gauteng
- **Primary CTA** Request a Migration Assessment · **Secondary** Book a Cloud Consultation

## 2. Microsoft 365 Support & Administration

- **URL** `/cloud-microsoft-365/microsoft-365-support/`
- **SEO title** Microsoft 365 Support Gauteng | CMAXX
- **Meta description** Ongoing Microsoft 365 administration for users, licences, email, MFA, Teams, SharePoint and business support across Gauteng.
- **H1** Microsoft 365 Support & Administration for Gauteng Businesses
- **Keyword theme** Microsoft 365 support Gauteng
- **Primary CTA** Get Microsoft 365 Support · **Secondary** Discuss a Monthly Support Plan

## 3. Microsoft Teams & SharePoint Solutions

- **URL** `/cloud-microsoft-365/teams-sharepoint/`
- **SEO title** Microsoft Teams & SharePoint Services Gauteng | CMAXX
- **Meta description** Teams and SharePoint setup, permissions, document libraries and collaboration support for Gauteng businesses.
- **H1** Microsoft Teams & SharePoint Solutions for Gauteng Businesses
- **Keyword theme** Teams and SharePoint services Gauteng
- **Primary CTA** Book a Collaboration Assessment · **Secondary** Request a Permissions Review

## 4. Business Email & Exchange Online

- **URL** `/cloud-microsoft-365/business-email-exchange-online/`
- **SEO title** Business Email & Exchange Online Gauteng | CMAXX
- **Meta description** Professional company email, Exchange Online setup, mailbox migration, shared mailboxes and Outlook support for Gauteng businesses.
- **H1** Business Email & Exchange Online Services for Gauteng Businesses
- **Keyword theme** business email setup Gauteng
- **Primary CTA** Set Up Professional Business Email · **Secondary** Request an Email Migration Quote

## 5. Business Backup & NAS Storage Solutions

- **URL** `/cloud-microsoft-365/business-backup-nas/`
- **SEO title** Business Backup & NAS Storage Gauteng | CMAXX
- **Meta description** NAS storage, local backup, off-site copies, monitoring and recovery solutions for Gauteng businesses.
- **H1** Business Backup & NAS Storage Solutions for Gauteng Businesses
- **Keyword theme** NAS storage and backup Gauteng
- **Primary CTA** Book a Backup & Storage Assessment · **Secondary** Discuss a NAS Solution

## Applies to every page

- Self-referencing canonical to the final `cmaxxwifisolutions.co.za` URL; index,
  follow; included in the XML sitemap and verified in Search Console after QA.
- `BreadcrumbList` structured data matching the visible breadcrumb, plus
  `Service` markup and site-level Organisation / LocalBusiness data. Mark up
  only facts true and visible on the page.
- FAQ content is published for users and topical depth. `FAQPage` markup may be
  added if technically valid, but do not expect a rich result.
- A unique title and meta description per page — none reused across the cluster.
- Lead form fields per the brief: full name, company, business email, telephone
  or WhatsApp, approximate number of users, current email or cloud platform, and
  service required.
- Track CTA clicks, form submissions, phone clicks and WhatsApp clicks.

## Accuracy guardrails held in the copy

The brief lists wording that must not appear as a blanket claim. None of it
does. The pages use instead:

| Instead of | The pages say |
| --- | --- |
| "No data loss" | "Carefully planned migrations are designed to minimise disruption and reduce data-loss risk" |
| "POPIA compliant" | "Configured to support your organisation's security, privacy and POPIA responsibilities" |
| "Zero downtime" | An explicit description of what staff will experience during DNS propagation and MFA registration |
| "Enterprise-grade security included" | Named controls, each qualified by the plan that provides it |
| "Microsoft Partner" | "CMAXX is an independent service provider and is not affiliated with or endorsed by Microsoft" |

Every feature claim that varies by licence is qualified — anti-spam, phishing
protection, retention, archiving, versioning windows, safe links and
attachments, and Microsoft 365 recovery behaviour. No counters or unverified
performance figures appear anywhere.

## Brand-asset rule

No Microsoft logo, app icon or partner badge is used anywhere in the cluster.
Microsoft product names appear as text only, which is what the brief requires
unless CMAXX holds the relevant permission and an approved asset. Keep it that
way when adding imagery.

## Outstanding before launch

- **Imagery.** Each page carries one `<image-slot>` placeholder needing a real
  CMAXX photograph or a custom CMAXX diagram — the brief specifically suggests a
  Microsoft 365 relationship diagram, a seven-step migration illustration, a
  Teams/SharePoint/OneDrive ownership diagram and a 3-2-1 backup diagram. Avoid
  generic futuristic server imagery and app-logo collages.
- **Case studies.** No placeholder projects have been written. Cloud-specific
  case studies should replace generic WiFi and CCTV testimonials as proof on
  this cluster.
- **Pages linked but not yet built:** `/managed-wifi/`, `/areas-we-serve/` and
  `/contact/` do not exist in the prototype, so those links fall through to the
  contact section.
