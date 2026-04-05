# My Personal Project — Complete product specification

**Version:** 1.18 (implementation-aligned)  
**Status:** Source of truth for implementation  
**Repository:** [github.com/jhrb96/personal](https://github.com/jhrb96/personal)

---

## How to read this document

- **Quick orientation (≈5 minutes):** Read **§1 At a glance** and **§3** (what lives on **`/`** and in which order). Skim **§15** for the stack.  
- **Implementation or debugging:** Use **§4** (feature checklist), **§11** (consent + legal routes), **§20** (requirement IDs), then **§21** (launch checklist).  
- **Metrics, traffic, and labelling:** **§6–§9** (UTMs, two reach signals, funnel, tracked visitor rules) and **§14** (KPI philosophy).  

This file stays the **single canonical** spec: behaviour is authoritative here and in code together; **§23** records substantive edits.

---

## Table of contents

**Site, audience, and product intent**

1. [Executive summary](#1-executive-summary) — *what ships; metadata; at-a-glance*  
2. [Problem, audience, and success](#2-problem-audience-and-success) — *why the site exists; who it serves*

**Information architecture and UX**

3. [Information architecture](#3-information-architecture) — *single-page **`/`**; section order; hero copy; footer routes*  
4. [Feature set (plan of record)](#4-feature-set-plan-of-record) — *numbered capability list*  
5. [Visual design and brand](#5-visual-design-and-brand) — *look, theme, layout constraints*

**Data, traffic, consent, and legal**

6. [Traffic qualification (UTM)](#6-traffic-qualification-utm) — *allowlisted `utm_medium`*  
7. [Analytics model: two reach signals](#7-analytics-model-two-reach-signals) — *qualified vs tracked visitors*  
8. [Funnel definitions](#8-funnel-definitions) — *stages and instrumentation*  
9. [Visitor definition (tracked visitors)](#9-visitor-definition-tracked-visitors) — *UTC day, storage, bots*  
10. [Consent boundaries](#10-consent-boundaries) — *what is gated vs essential*  
11. [Privacy, legal, and CMP](#11-privacy-legal-and-cmp) — *banner, `/privacy`, `/cookies`, alternatives*

**Integrations and public metrics**

12. [Integrations: booking, feedback, automation](#12-integrations-booking-feedback-automation) — *Calendar, Typeform, Zapier*  
13. [Public dashboard (`#metrics`)](#13-public-dashboard-metrics) — *tiles, labels, targets*  
14. [Metrics philosophy and KPIs](#14-metrics-philosophy-and-kpis) — *how to talk about numbers*

**Stack, content, constraints**

15. [Project stack](#15-project-stack) — *Layer/Components table + live Architecture columns*  
16. [Content inventory](#16-content-inventory) — *shipped vs still iterating*  
17. [Accessibility and i18n](#17-accessibility-and-i18n)  
18. [Out of scope](#18-out-of-scope)  
19. [Known limitations and operational notes](#19-known-limitations-and-operational-notes)

**Requirements and operations**

20. [Implementation requirements (IDs)](#20-implementation-requirements-ids) — *CMP-*, ESS-*, etc.*  
21. [Launch checklist](#21-launch-checklist)  
22. [Glossary](#22-glossary)  
23. [Document history](#23-document-history)

**Appendix:** [Single-Page Dynamic Clarifications (locked)](#single-page-dynamic-clarifications-locked) — *nav, progress, events, motion*

---

## 1. Executive summary

### At a glance

- **Single-page site** on **`/`** (English only): hero, about, thesis, metrics, architecture, pre-mortem, CTA, feedback — sticky nav and legacy path redirects to **`#`** anchors.  
- **First-party metrics** on **`#metrics`**: qualified UTM visitors + consent-gated tracked visitors; public dashboard **not** fed by Vercel Web Analytics.  
- **Booking** via **Google Calendar**; **feedback** via **Typeform** → **Zapier** → **Notion** (+ Slack/email).  
- **Consent:** first-party banner; **Privacy** and **Cookie** notices at **`/privacy`** and **`/cookies`**.  
- **Stack:** **Next.js** on **Vercel**, optional **KV/Redis** for aggregates, architecture table in **`lib/architecture-content.ts`**.  
- **Honest labelling:** never blend UTM-qualified and tracked-visitor series without explicit copy (see **§7**, **§14**).

**One-line:** A “show, don’t tell” interactive site that converts high-intent visitors into booked intros, with transparent instrumentation, honest metrics, and a visible continuous-discovery loop.

**Root metadata (App Router):** **`title`:** `My Personal Project — Site`. **`description`:** `Show-don't-tell site: product thesis, architecture, first-party metrics, and continuous discovery.`

**What ships:** A **Next.js** app on **Vercel**, **English-only**, as a **single** on-page site on **`/`** (full **About** first below **Hero** — product intro, reverse-chron **Experience** / **Education**, press and programme cards, collapsible eras/schools — then **thesis**, **metrics**, and other narrative sections), a **public metrics story** built from **first-party** data (not Vercel Web Analytics on the public dashboard), **Google Calendar** booking, **Typeform** feedback → **Zapier** → **Notion** (+ notifications), a **first-party consent banner** that gates **analytics** while keeping **strictly necessary** experiences (including feedback) available (**§11**), and **Privacy** / **Cookie** notices at **`/privacy`** and **`/cookies`** (UK ICO–style structure).

---

## 2. Problem, audience, and success

### 2.1 Problem

Strong PMs are hard to signal through static resumes. Target employers are tired of generic PDFs. The site exists to **prove** product taste, technical judgment, analytical rigor, and operational habits **on arrival**.

### 2.2 Primary audiences

| Audience | Need |
|----------|------|
| **VP Product / engineering leaders** | Depth: thesis, architecture, post-mortem, metrics honesty. |
| **Recruiters** | Speed: credibility, scheduling, minimal friction (**under 10 seconds** to value + primary CTA above the fold). |

### 2.3 Success goals

1. **Career:** Access to high-ownership, high-caliber teams and compensation (outcome outside this doc).  
2. **Product proof:** Ship an MVP that demonstrates UX, data narrative, architecture transparency, and research discipline.  
3. **Conversion:** Ambitious targets on **qualified** outreach; denominators and numerators **explicitly labeled** (see §14).  
4. **Continuous discovery:** Qualitative feedback drives iteration; personal **SLA:** address valid objections in site or messaging within **48 hours** where practical.

---

## 3. Information architecture

*In this section:* how the **single** shipped experience on **`/`** is ordered (sections, hero, footer links), how **legacy** URLs behave, and the **site structure** table that maps areas to **`#`** IDs.

### 3.1 Single depth on `/`

There is **one** shipped experience on **`/`** (no Recruiter vs Product URL toggle). Content mix:

- **`#about`:** Full bio — product intro, then reverse-chron **Experience** and **Education**; **press cards** and collapsible employer/education rows as today. Default **collapsed** disclosures on load; each summary shows an **Expand** label and chevron when closed. Legacy **`/#highlights`** scrolls to the top of **`#about`** via a compat anchor (no separate Career highlights block).  
- **Scroll order after #hero:** **`#about`** (bio, experience, press), **`#thesis`** (product thesis), **`#metrics`** (public dashboard), **`#architecture`**, **`#post-mortem`**, **`#cta`**, **`#feedback`**. Full narrative and **full public dashboard** layout.

**Canonical home:** **`/`** (no `mode` query). Legacy URLs with **`?mode=product`** are **stripped client-side** while preserving **hash** and other query params (e.g. UTMs).

**Outbound links:** Prefer root + UTMs, e.g. `/?utm_medium=dm&utm_source=linkedin`.

**Primary delivery:** **Single-page** on **`/`** with stable **`#` section IDs** and sticky in-page nav. **Legacy paths** (`/about`, `/thesis`, `/architecture`, `/post-mortem`, `/social`, `/dashboard`) **redirect** to **`/#…`** anchors. **Privacy** and **Cookie** policies stay on **separate** routes, footer-linked.

**`#hero`:** Besides the primary **Schedule** CTA, a **secondary control** (GitHub mark + label) opens the **complete** product spec (**`Personal_Project_Spec.md`**), using the **same canonical URL** as footer **Spec on GitHub**.

**Shipped hero copy (v1)** — visible strings on **`/`** (see **`components/single-page-content.tsx`**):

- **Eyebrow (uppercase):** **My Personal Project**  
- **Headline (`<h1>`, two lines):** **Showcasing product judgment** / **on one page**  
- **Supporting paragraph:** *I want to show how I think and what I can build. This minimum viable product site includes a bio, condensed product documentation, metrics, a feedback form, and a booking link.*  
- **Controls:** **Booking** CTA and **spec** control are both in the hero band (booking also appears in **`#cta`**).

### 3.2 Site structure (plan of record)

| Area | Description |
|------|-------------|
| **Executive summary** | **`#hero`** — shipped copy: eyebrow **My Personal Project**; headline **Showcasing product judgment** / **on one page**; MVP intro paragraph (bio, documentation, metrics, feedback, booking); **Google Calendar** booking CTA + **GitHub-mark** control to the **full** written spec (same URL as footer **Spec on GitHub**). **`#about`** (document order **immediately after** **Hero**, **before** **Thesis**) — reverse-chron **Experience** / **Education** with collapsible blocks (**default collapsed**, **Expand** + chevron): identity in the header → optional bullets and linked **press** / **programme** cards in the panel (see §4). Legacy **`/#highlights`** scrolls to the top of **`#about`**. |
| **Product Thesis** | Section **`#thesis`** (after **About**, before **Metrics**) — **Problem statement**; **Proposed Solution** (four bullets); short in-page links to **Metrics**, **Architecture**, and **Pre-Mortem**; **four** default-collapsed disclosures (vision, dual-audience table, execution engine, impact & discovery). KPI definitions and denominators stay in **`#metrics`**, not duplicated here. |
| **Transparent dashboard** | Section **`#metrics`** on `/` — public metrics with **honest refresh/latency** copy (full dashboard — §13). |
| **Architecture & trade-offs** | Section **`#architecture`** — **Project stack** table (§15 **Layer** / **Components**) plus on-page **Trade-offs** and **Why I chose it** columns; links to this spec where useful. |
| **Post-mortem** | Section **`#post-mortem`** — failure + operational follow-up (intellectual honesty). |
| **Frictionless conversion** | Section **`#cta`** — prominent path to **Google Calendar booking** (`calendar.app.google/...`). |
| **Continuous discovery** | Section **`#feedback`** — **Typeform** **last** on the page (after **`#cta`**); feedback via scroll, not above the fold. |

**Footer (every page):** **Privacy** → **`/privacy`**, **Cookie policy** → **`/cookies`**, **Spec on GitHub** → canonical markdown URL at top of this doc.

---

## 4. Feature set (plan of record)

*In this section:* the **numbered plan of record** — what each major block on **`/`** (and policies) **must** do. Use this list when checking parity with components and routes.

1. **Executive summary (home)** — **`#hero`**: shipped headline and MVP intro (see **§3.1** **Shipped hero copy**); **Schedule** + spec controls in the hero; repeat booking path in **`#cta`**. **`#about`** (first section after **Hero**): product intro; reverse-chron **Experience** / **Education** with full **press proof** where configured — headline, outlet, **short quote** (one sentence on mobile; slightly longer blockquote allowed on wide viewports), **Read full article** → **canonical publisher URL** (not in-repo HTML as the primary link). Press rows live in a **typed `lib/` manifest**; **mobile:** press cards **stack** vertically. Quotes MUST be taken from the linked article or labeled (e.g. **“From coverage in …”**). Employer and education rows are **collapsible** (`<details>` / disclosure pattern); default **collapsed**, with visible **Expand** + chevron on the summary. Legacy **`/#highlights`** scrolls to the top of **`#about`**.  
2. **Product Thesis** — Section **`#thesis`** on `/` (**before** **`#metrics`**): problem statement, **Proposed Solution** bullet list, cross-links to metrics/architecture/pre-mortem, and four collapsible depth blocks (see §3.2 table row).  
3. **Public dashboard** — Section **`#metrics`**: first-party metrics; full layout in §13.  
4. **Architecture & trade-offs** — Section **`#architecture`** on `/` (include **Project stack** §15 plus extended columns on the live page — see §15 implementation note).  
5. **Post-mortem** — Section **`#post-mortem`** on `/`.  
6. **Scheduling** — Section **`#cta`**: outbound link to **Google Calendar booking page**.  
7. **Feedback** — Section **`#feedback`**: **Typeform** last on page → **Zapier** → **Notion** + Slack/email.  
8. **Consent** — First-party cookie banner + **`/api/consent/analytics`**; policies and categories per **§11** and **§20** (the **§15** stack row remains labelled **OSS CMP** + policies as architectural shorthand).  
9. **Color theme** — Manual **light** / **dark** / **system** (§5); persisted preference; drives page chrome and theme-aware brand marks.

**Explicitly out:** Public competitive **teardowns** (§18).

---

## 5. Visual design and brand

- **Direction:** **Prestige editorial** — visual flair **and** clarity; **not** gimmick-first UI. **Employer and education logos** for **factual identification** of the owner’s roles and study (**nominative use**, e.g. assets under `assets/brand/`) are **in scope**.  
- **Layout:** Main column **max-w-6xl** aligned with sticky header; bordered sections span the **full** column width (no mixed narrower card max-widths).  
- **Motion:** Respect **prefers-reduced-motion**; any animated interactions must remain **accessible**.  
- **Color theme:** A **manual** control SHALL set appearance to **light**, **dark**, or **system** (follow OS). The choice SHALL **persist** (e.g. local storage). The **effective** theme SHALL drive Tailwind **`dark:`** styling on the document root **and** **theme-aware assets** (e.g. separate light / dark **brand** marks under `assets/brand/` and `assets/brand/darkmodebrand/`) so logos do not rely on **`prefers-color-scheme` alone** when the user overrides theme.

---

## 6. Traffic qualification (UTM)

**Qualified** sessions are defined by an allowlisted **`utm_medium`** (bucket). **`utm_source`** = specific channel. **`utm_campaign`** = optional campaign label.

| `utm_medium` | Use |
|--------------|-----|
| `social` | Social network posts |
| `dm` | Direct messages |
| `referral` | Warm intros / forwarded links |
| `forum` | Forums, community Slacks, etc. |
| `email` | Email outreach (if distinct from `dm`) |
| `event` | Conferences, talks, QR codes |
| `job_board` | Hiring-related placements |

**Examples:**  
`?utm_medium=dm&utm_source=linkedin&utm_campaign=catalyst-v1`  
`?utm_medium=social&utm_source=x`

**Non-qualified:** Missing or unknown `utm_medium` → **Unattributed** / **All traffic**. **Never** merge into qualified KPIs without a label.

---

## 7. Analytics model: two reach signals

*In this section:* the **two** reach series the product exposes — **UTM-qualified visitors** (no analytics consent) vs **tracked visitors** (after consent) — and how they differ in question, consent, and rough implementation.

The product uses **two** labeled series; they answer different questions.

| Series | Question it answers | Consent | Implementation sketch |
|--------|---------------------|---------|-------------------------|
| **Qualified visitors (UTM)** | “How many **unique browsers** arrived via a qualified outbound link (allowlisted `utm_medium`)?” | **Not** required | **Edge middleware** + **httpOnly** first-party cookie + **Redis sets** (cumulative; not UTC-day buckets). |
| **Tracked visitors / Landing** | “How many people **accepted tracking** and generated a counted visit?” | **Required** (analytics category) | **`localStorage`** + visitor increment API; **first pageview** after accept per UTC day (§9). Public **`#metrics`** shows a **cumulative** total (still at most one increment per browser per UTC day). |

> **Key rule:** Never conflate the two series in UI or narrative without explicit labels. A headline for tracked visitors can be: **“Hit my qualified link and accepted tracking.”**

---

## 8. Funnel definitions

*In this section:* funnel **stages** (landing, scroll-through, schedule started, booked) and which **instrumentation** backs each — and what **must not** feed the public dashboard.

**Public dashboard data** comes **only** from **first-party** pipelines (counters, anonymous events, integrations) — **not** from **Vercel Web Analytics** (§15).

**Vercel Web Analytics:** **Off by default.** If enabled (e.g. private debugging), it **must** be **consent-gated** and **must not** feed the **public** dashboard (**VWA-1**).

> **Key rule:** Public **`#metrics`** tiles use **first-party** pipelines only — not Vercel Web Analytics (**VWA-1**).

| Stage | Definition | Instrumentation |
|-------|------------|-----------------|
| **Landing** | **First pageview** after **analytics consent** that triggers the **UTC calendar-day** visitor increment for that day. **≠** UTM-qualified visitors (separate cumulative series). | First-party API + §9 |
| **Scroll-through** | **All-time** share: cumulative **complete** ÷ cumulative **start** (each browser contributes at most one **start** and one **complete** per UTC day via client dedupe). Range ends at a **sentinel** immediately **before** the Typeform block. | Anonymous **POST** (`start` / `complete`) — **ESS-1**; **`#metrics`** shows **%** from cumulative counters |
| **Schedule started** | User initiates booking from site (e.g. click CTA to Google booking page); public tile is a **cumulative** total. | Anonymous **POST** — **essential operational** |
| **Booked (confirmed)** | Appointment held / confirmed | **Google Calendar** (and optional Zapier → Notion/ops) — **not** shown as a public dashboard counter (avoids false positives without strict Calendar filters) |

**Honesty:** UI states **actual** refresh cadence (batching, rollup interval), not faux “live.”

---

## 9. Visitor definition (tracked visitors)

**Window:** **UTC calendar day** (midnight-to-midnight **UTC**).

**Storage:** `localStorage` (or equivalent) holds the **last UTC date** (`YYYY-MM-DD`) for which this browser was counted.

**Rule:** At most **one** visitor increment per **UTC day** per browser profile. The **counted hit** is the **first pageview** on that calendar day **after** analytics consent that triggers the increment.

**CMP:** No read/write of visitor session keys and **no** visitor-count API call **until** the user accepts the **analytics / measurement** category — must match Privacy/Cookie copy.

**Bots:** Best-effort exclusion; disclose that figures exclude automated traffic to the extent detected.

**Not used:** Rolling 24-hour window from first hit (deprecated for this product).

---

## 10. Consent boundaries

*In this section:* a **matrix** of data/UX surfaces (visitor session, scroll metrics, Typeform, UTMs, optional VWA) and whether each is **analytics-gated**, **essential**, or **strictly necessary** — the quick reference for **§11** implementation detail.

| Data / UX | Treatment |
|-----------|-----------|
| **Visitor session** (`localStorage` + visitor-count API) | **Analytics / measurement** — **only after accept** |
| **Scroll-through** | **Essential operational** — allowed without analytics accept; **anonymous POSTs** per **ESS-1** (range excludes Typeform) |
| **Schedule started** | **Essential operational** — **anonymous POST**; same consent boundary as scroll-through |
| **Typeform** | **Strictly necessary** in CMP — **not** analytics-only; **Reject all** must still load embed (**TYPEFORM-1**) |
| **Qualified visitors (UTM)** | Server-side cookie + URL — **no** analytics consent for this count; **label** distinctly vs tracked visitors |
| **Vercel Web Analytics** | Off by default; if on → analytics consent |
| **Public dashboard** | Composes **first-party** series only per rows above |

> **Key rule:** **Typeform** stays available when visitors reject non-essential analytics (**TYPEFORM-1**); **Privacy** / **Cookies** copy must stay aligned.

---

## 11. Privacy, legal, and CMP

*In this section:* what **ships** today (banner, API, routes), where **authoritative legal text** lives, and **library alternatives** if you fork the CMP.

### 11.1 Implemented consent (v1)

- **Surface:** Fixed **first-party** banner on **`/`** — **Accept analytics** / **Reject non-essential**; decision persisted in **browser local storage**; analytics identifier set or cleared via **`POST` / `DELETE`** **`/api/consent/analytics`** (**httpOnly** cookie when accepted).  
- **Semantics:** Match **§10** and **§20** (**CMP-1**, **CMP-2**, **TYPEFORM-1**, **ESS-1**, **VWA-1**): optional analytics and visitor-persistent storage for those counts **only** after accept; **Typeform** remains available when analytics is rejected (**strictly necessary** positioning — **Privacy** / **Cookies** must stay aligned).  
- **Code:** **`components/consent-banner.tsx`** (+ related client listeners). This is **not** the [Vanilla Cookie Consent](https://github.com/orestbida/cookieconsent) bundle as the deployed UI; it follows the same **category** intent as **CMP-4**-style minimal CMP.

### 11.2 Published legal notices

- **Routes:** **`/privacy`** (privacy notice), **`/cookies`** (cookie policy) — footer-linked, UK ICO–oriented structure, controller and contact **as published** in-app.  
- **Rule:** Full legal text is **authoritative** on those pages; this spec does not duplicate it—only behaviour and routes are referenced here.

### 11.3 Alternatives (forks / greenfield)

- **Libraries:** [Vanilla Cookie Consent](https://github.com/orestbida/cookieconsent), **`react-cookie-consent`**, or **shadcn-style** UI remain valid **alternatives** if you replace the minimal banner— you still own vendor inventory and proof of gating.  
- **Scripts:** Non-essential scripts load **only** after appropriate consent (**CMP-1**).  
- **Vercel** is infrastructure/processor — see [Vercel legal](https://vercel.com/legal); it is **not** a replacement for consent UX and policies.  

---

## 12. Integrations: booking, feedback, automation

### 12.1 Booking

- **UX:** Link (or button) to **Google Calendar booking page** — `https://calendar.app.google/...` pattern (env `NEXT_PUBLIC_BOOKING_URL` overrides committed default).  
- **Confirmation:** **Google Calendar** is the system of record. Optional **Zapier** on **New Event** may notify Notion/Slack — **not** wired to a public **Booked** counter in the app (see §19).

### 12.2 Feedback

```
Typeform → Zapier → Notion (database row) + Slack or email
```

- **No app-owned DB** for qualitative storage — **Notion** holds responses.  
- **Metrics** (aggregates, funnel counters) may use **Vercel KV** (or equivalent).  
- **Placement:** Section order **last** (after final scheduling CTA). Primary CTA stays above the fold; feedback is reached by scrolling.

### 12.3 Automation

- **Zapier** is the orchestration layer between Typeform, Notion, notifications, and Calendar triggers.

---

## 13. Public dashboard (`#metrics`)

*In this section:* what the **public** metrics block on **`/`** shows — qualified vs tracked visitors, essential tiles, and targets — **one** on-page dashboard (no separate Recruiter/Product URL mode).

- Show **qualified UTM visitors** (cumulative uniques, server-side, always label) **and** **tracked visitor** metrics (consent-gated where applicable; **cumulative** total on the tile, §9 dedupe rule unchanged).  
- If analytics **not** accepted: visitor count shows **—** and/or **“Accept analytics to see visitor counts”**.  
- **Essential** metrics: **scroll-through** (% from **all-time** cumulative starts/completes), **schedule started** (**cumulative**) — **no** public **Booked** tile.  
- **Targets:** Ambitious goals with **date range** and explicit denominators (§14).

---

## 14. Metrics philosophy and KPIs

- **Qualified vs All:** Always label **UTM-qualified** vs **Unattributed** / **All traffic**.  
- **Two “qualified reach” meanings:** (1) **UTM-qualified visitors** — cumulative unique browsers with allowlisted `utm_medium` (cookie dedupe; no analytics consent). (2) **Tracked visitors** — only with consent; increments **at most once per browser per UTC day**, dashboard shows **cumulative** total. **Never** blend without labels.  
- **Stretch goals:** Shown as targets with **time bounds** and stated **hypothesis** (e.g. share of traffic from intentional outbound).  

**Primary KPI (product narrative):** Funnel or intent story on **high-intent** segments — define numerator/denominator in dashboard copy (e.g. UTM-qualified visitors → **schedule started**; tracked visitors → **scroll-through** — pick and label one **primary** story on the Architecture page).

**Secondary:** Section views (anonymous aggregates); scroll-through as **read-depth** signal with definition in UI.

**Qualitative:** Count of Typeform submissions; themes feed copy iteration.

---

## 15. Project stack

*In this section:* the **reference stack table** (mirrored on **`/#architecture`** and referenced from privacy subprocessors) plus how **Trade-offs** / **Why I chose it** are maintained in code.

**Implementation note:** the live **Architecture** section mirrors **Layer** and **Components** from this table via `lib/architecture-content.ts`, and adds two on-page columns—**Trade-offs** and **Why I chose it**—that are **not** part of the Privacy subprocessors mirror below. Those two columns are written in **plain language** for a general reader (business and operational outcomes); keep **Layer** and **Components** aligned with this table when editing the rows.

Mirror this table on the **Architecture** page and in **Privacy** subprocessors.

| Layer | Components |
|-------|------------|
| App | **Next.js** (App Router) |
| Hosting / edge | **Vercel** |
| First-party metrics | Vercel Functions / Edge + **KV** (or equivalent) |
| Optional analytics | **Vercel Web Analytics** — **off by default**; consent-gated if enabled; **not** for public dashboard |
| Booking | **Google Calendar** booking (`calendar.app.google`) |
| Feedback | **Typeform** |
| Automation | **Zapier** |
| Internal | **Notion**; **Slack** or email |
| Consent | **OSS CMP** + policies |

---

## 16. Content inventory

**Shipped in v1:** **`#hero`** copy and root **metadata** (§1, §3.1); **Privacy** / **Cookie** pages at **`/privacy`** and **`/cookies`**; **CMP** banner strings in **`components/consent-banner.tsx`**.

**Iterate / review** where copy is still open-ended:

- **Executive summary:** optional tightening with someone who hires PMs (hero MVP paragraph may evolve).  
- **Career / bio:** reverse-chron **eras**, stacked layout; **press cards** in **#about** per §4; **`lib/`** manifest fields (title, outlet, canonical url, quote, optional attribution, logo key, employer/era tag).  
- Product Thesis, Architecture narrative, Post-mortem.  
- **Press excerpts** in **`#about`** (including short quotes where permissioned and sourced from coverage): align with live articles or use explicit attribution labels; avoid fabricated quotes.  
- Dashboard copy (definitions, refresh rate, labels).

---

## 17. Accessibility and i18n

- **Accessibility:** Keyboard navigation, focus order, contrast, **prefers-reduced-motion**, semantic HTML; **theme control** keyboard-operable with clear name/state (see §5). **Launch standard (v1):** **no obvious blockers** on common mobile widths, keyboard paths, and one screen-reader smoke pass — not a formal WCAG conformance. Operational checklist: `openspec/changes/project-catalyst/design.md` § **Accessibility & mobile acceptance**.  
- **i18n:** **English only** for v1.

---

## 18. Out of scope

- **Public product teardowns** of other companies.  
- **Paid** Vercel Analytics tier as a **dependency** of the public dashboard story.  
- **i18n** / localized locales (v1).

---

## 19. Known limitations and operational notes

- **No public Booked counter:** Calendar-derived counts are **not** shown on the dashboard (Zapier without strict filters produced false positives). Confirm bookings in **Google Calendar** (and optional Zapier → Notion).  
- **Scroll range:** Engagement **scroll-through** ends at the sentinel **before** Typeform; scrolling inside the embed does not advance the metric.  
- **Hero / executive copy:** External copy review recommended before wide outbound (shipped MVP intro in **`#hero`** may still evolve).

---

## 20. Implementation requirements (IDs)

| ID | Requirement |
|----|---------------|
| **CMP-1** | Non-essential scripts only after relevant consent. |
| **CMP-2** | Visitor `localStorage` + visitor-count API only after **analytics / measurement** accept. |
| **CMP-3** | **Shipped (v1):** minimal **first-party** consent banner + **`/api/consent/analytics`** (see **§11.1**). **Fork path:** **Vanilla Cookie Consent** + App Router client boundary; inject optional scripts only after accept. |
| **CMP-4** | Alternative: **shadcn-style** CMP UI — same **CMP-1** / **CMP-2** semantics. |
| **ESS-1** | Scroll-through + schedule started: **essential**; **anonymous POSTs** — no stable client id; server **must not** fingerprint to individuals. |
| **TYPEFORM-1** | Typeform in **strictly necessary**; **Reject all** still loads embed. |
| **VWA-1** | Vercel Web Analytics **off by default**; if on → consent; **never** public dashboard input. |

**Acceptance:** Visitor + analytics-gated behavior matches published policies; essential paths (**ESS-1**, **TYPEFORM-1**) documented and implemented consistently.

---

## 21. Launch checklist

- [ ] Privacy + Cookie policies match **actual** scripts, storage, and subprocessors.  
- [ ] CMP categories: analytics vs strictly necessary (Typeform) configured; **Reject all** tested.  
- [ ] Footer: Privacy, Cookie (if any), **Spec on GitHub** → this file.  
- [ ] Dashboard labels: UTM-qualified visitors vs tracked visitors; refresh cadence stated.  
- [ ] UTMs tested on outbound links; canonical home is **`/`** (no `mode` query).  
- [ ] Zapier flows live (Typeform → Notion; optional Calendar notifications — **not** required for app metrics).  
- [ ] Non-negotiables copy reviewed.  

---

## 22. Glossary

| Term | Meaning |
|------|---------|
| **Qualified visitor (UTM)** | Unique browser (first-party cookie) that arrived with allowlisted `utm_medium`; counted once per scope in cumulative Redis sets. |
| **Tracked visitor** | Browser counted at most once per **UTC day** after analytics consent (first qualifying pageview); **`#metrics`** displays the **cumulative** sum of those increments. |
| **Landing** | Funnel stage = that first qualifying pageview for the visitor model. |
| **Essential operational** | Events (scroll-through POSTs, schedule started) allowed without analytics consent; anonymous only (**ESS-1**). |
| **Scroll-through** | **All-time** %: cumulative completes ÷ cumulative starts (per-browser dedupe still **once per UTC day** for each event type); main narrative range excludes Typeform block. |
| **Project stack** | Full transparent technology list (§15). |

---

## 23. Document history

| Version | Summary |
|---------|---------|
| **1.0** | **Complete spec:** Merged PRD features, modes, UTM, dual reach metrics, funnel, UTC visitor model, consent/CMP IDs, integrations, dashboards, stack, KPIs, launch checklist, glossary, out of scope. Repository: [jhrb96/jhrb-portfolio](https://github.com/jhrb96/jhrb-portfolio). |
| **1.1** | Scroll-through metric (sentinel before Typeform); Typeform **last**; **no** public Booked counter; **max-w-6xl** aligned column; repo **jhrb-portfolio**. |
| **1.2** | Inclusive UX acceptance: **no obvious blockers**; matrix in OpenSpec `design.md`; tasks **6.5** / **7.3**. |
| **1.3** | Bio / press: **reverse-chron stacked eras**; **Recruiter Option B** (micro-cred only); **Product** press cards + canonical publisher links + quote rules; typed **`lib/`** manifest; mobile press cards **stack**; nominative employer/education logos distinguished from forbidden racing reference IP (§5). |
| **1.4** | **Single-page primary IA** on **`/`** with section **`#` IDs**; **legacy path redirects** to anchors; table §3.2 and feature list §4 name sections instead of separate marketing “pages” for narrative (policies remain separate routes). |
| **1.5** | **Manual color theme:** **light** / **dark** / **system** + persistence; document root drives **`dark:`** and **brand** light/dark assets (effective theme, not OS media query alone when overridden); OpenSpec **catalyst-site** requirement + task **2.12**. |
| **1.6** | **Single depth:** Removed Recruiter/Product URL modes; one experience on **`/`** (full About + bullet Highlights + full metrics/narrative); legacy **`?mode=product`** stripped client-side; redirects use **`/#…`** only. |
| **1.10** | **No top-level `#proof`:** Strategic proof section removed from **`/`**; **`lib/sections.ts`** and in-page nav omit **`proof`**; legacy **`/social`** redirects to **`/#about`** (press and bio). |
| **1.11** | **`#about`** moved **after** **`#pre-mortem`** and **before** **`#cta`** in document order, **`SECTION_IDS`**, and sticky nav; hero remains first; thesis still immediately follows hero (before metrics). |
| **1.12** | **`#about`** is **first** below **`#hero`**; **Career highlights** bullet block removed from **`#about`**; legacy **`/#highlights`** retained as scroll target at top of About; **`SECTION_IDS`** and sticky nav order updated (`about` before `thesis`). |
| **1.13** | **UTM-qualified metric:** cumulative **unique visitors** via **`catalyst_qualified_vid`** + Redis **sets** (no UTC-day reset for that tile); legacy daily **`metrics:qualified:YYYY-MM-DD:*`** keys unused by summary. |
| **1.14** | **Public dashboard totals:** Tracked visitors, scroll-through numerators/denominators, and schedule started use **cumulative** KV counters on **`#metrics`** (dual-written `*:total` keys); UTC-day rules apply to **when** an increment fires, not to resetting the displayed headline. |
| **1.15** | **Copy terminology:** In-app and spec-facing prose uses **“site”** for the shipped **`/`** experience; **“portfolio”** is reserved for the **repository** name (**`jhrb-portfolio`**) in URLs and similar identifiers. |
| **1.16** | **Display name:** Public product label **My Personal Project** (hero, metadata, footer, readme, this doc H1); technical **`catalyst_*`** keys and **`Personal_Project_Spec.md`** filename unchanged. |
| **1.17** | **Build parity:** Spec documents **shipped hero** copy, **root metadata**, **`/privacy`** / **`/cookies`**, **implemented** first-party consent banner vs **library alternatives** (**§11**); **CMP-3** updated; **§16** inventory reflects what is live; header **Version** aligned with history. |
| **1.18** | **Readability:** **How to read** guide and **thematic** table of contents; **At a glance** under **§1**; **In this section** leads for **§3, §4, §7, §8, §10, §11, §13, §15**; **Key rule** blockquotes where helpful; **§3** retitled (dropped legacy “and modes”); **§13** ToC anchor fixed to match **Public dashboard (`#metrics`)**; appendix linked from ToC. |

Prior iterative edits (discovery through requirements lock) are superseded by this document for implementation purposes.

---

## Single-Page Dynamic Clarifications (Locked)

- **Single depth:** One layout on **`/`**; section-level composition (full **About** below **Hero**, then **thesis**, full **metrics**, and narrative sections) — no URL mode toggle.
- **Legacy URLs:** **`?mode=product`** (and other `mode` values) are removed from the address bar on **`/`** while preserving **hash** and non-mode query params.
- **UTM handling:** Canonical tag for home is **`/`**; marketing links may append UTMs.

### Navigation + Progress
- Sticky nav uses stable section anchors on **`/`**.
- Progress UI includes active-section indicator and overall narrative progress bar.
- Progress denominator is section-content range: **`hero` start → `feedback` end** (full page, including Typeform block).

### Event Semantics (Anonymous / ESS-1)
- `section_view` fires on **50% intersection**, **first-entry per load** only.
- `section_view` remains aggregate counters only (no fingerprinting).

### Motion + Accessibility
- Fade-in animations trigger once per section per load.
- For `prefers-reduced-motion`, sections render immediately (no transition), while section-active and progress tracking remain enabled.
