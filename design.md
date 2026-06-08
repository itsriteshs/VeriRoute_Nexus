---
version: "packetflow-aether-dashboard-2026-06-08"
name: "PacketFlow ImmuneNet — Aether Control Dashboard"
description: "A production-grade logistics trust dashboard that combines the PaperFlow layout structure with the Aether Convergence color and typography system, adapted to the provided rounded SaaS dashboard inspiration image. The final UI should feel like a calm, premium command center for Proof-of-Movement, ImmuneNet alerts, SmartHub relay hardware, and city-scale digital-twin logistics."
source_basis:
  layout_reference: "PaperFlow Design Layout"
  visual_theme_reference: "Aether — Convergence of Intelligence"
  inspiration_image: "rounded white/green SaaS dashboard with left rail, top search bar, metric cards, analytics cards, collaboration panel, progress gauge, project list, and dark green timer card"
colors:
  primary: "#B1E09D"
  secondary: "#061C15"
  accent: "#82A89C"
  background: "#B1E09D"
  shell: "#EFF4EF"
  surface: "#FFFFFF"
  surface-muted: "#F6FAF7"
  surface-dark: "#061C15"
  text-primary: "#111827"
  text-secondary: "#4B5563"
  text-muted: "#8A9A94"
  border: "#D1DEDC"
  success: "#2F8F5B"
  warning: "#C8A43D"
  danger: "#DC4A45"
  info: "#82A89C"
typography:
  display-lg:
    fontFamily: "Inter"
    fontSize: "56px-64px"
    fontWeight: 500
    lineHeight: "1.04"
    letterSpacing: "-0.02em"
  heading-xl:
    fontFamily: "Inter"
    fontSize: "32px-40px"
    fontWeight: 600
    lineHeight: "1.1"
  heading-md:
    fontFamily: "Inter"
    fontSize: "20px-24px"
    fontWeight: 600
    lineHeight: "1.2"
  body-md:
    fontFamily: "Inter"
    fontSize: "15px-16px"
    fontWeight: 400
    lineHeight: "1.6"
  body-ui:
    fontFamily: "Inter"
    fontSize: "14px-16px"
    fontWeight: 400
    lineHeight: "1.45"
  label-md:
    fontFamily: "JetBrains Mono"
    fontSize: "11px-12px"
    fontWeight: 600
    lineHeight: "1.2"
spacing:
  base: "8px"
  gap: "16px"
  card-padding: "24px"
  section-padding: "80px"
rounded:
  app-shell: "32px"
  card: "28px-32px"
  control: "48px"
  pill: "9999px"
shadow:
  shell: "0 24px 80px rgba(6, 28, 21, 0.10)"
  card: "0 12px 36px rgba(6, 28, 21, 0.06)"
  hover: "0 18px 48px rgba(6, 28, 21, 0.10)"
---

# PacketFlow ImmuneNet — Aether Control Dashboard Design System

## 1. Design Decision

We are using the **PaperFlow dashboard/layout structure**, but replacing its orange paper-like identity with the **Aether Convergence visual language**.

The final product should follow the uploaded inspiration image: a premium rounded SaaS dashboard with a soft outer canvas, white cards, a left navigation rail, a search top bar, metric cards, analytics modules, and a dark green highlight card. But the content must be PacketFlow-specific: Proof-of-Movement, ImmuneNet, SmartHub relay nodes, PacketFlow routing, trust scoring, cold-chain proof, and demo controls.

### Final design sentence

**PacketFlow ImmuneNet is a calm, premium logistics trust command center: white rounded SaaS dashboard structure, Aether green intelligence palette, and cyber-physical logistics proof panels.**

Do not make it look like a generic delivery app. Do not make it look like a dark cybersecurity dashboard. It should look like a clean, judge-friendly, production SaaS interface that quietly reveals deep technical power.

---

## 2. Source Merge Rules

### From PaperFlow Design Layout

Keep:

- Pricing/plan-style card density converted into dashboard cards.
- Bento layout rhythm.
- Clear conversion-style CTAs.
- White/soft surface hierarchy.
- Structured first viewport composition.
- Calm product-page spacing.

Remove or convert:

- Orange palette.
- Pricing copy.
- Inter-only personality.
- Generic plan cards.

### From Aether Convergence

Use:

- Primary green: `#B1E09D`.
- Deep green/black surface: `#061C15`.
- Muted green accent: `#82A89C`.
- Inter for display, UI headings, and body copy.
- JetBrains Mono for technical labels, status codes, event IDs, hub IDs, route IDs, and API-like metadata.
- Smooth, restrained motion.
- Ambient intelligent-system feeling.

### From the dashboard inspiration image

Use:

- Large rounded outer container.
- Left sidebar navigation.
- Top search and user/status bar.
- Metric cards across the top.
- Main bento grid below.
- One dark green feature card for the strongest live/demo moment.
- Soft gray background around the app shell.
- White dashboard cards with rounded corners.
- Green primary action buttons.
- Minimal icon-line language.

---

## 3. Visual Personality

The interface should feel like:

- Premium logistics SaaS.
- Calm operations room.
- Intelligent network dashboard.
- Trust verification system.
- Real product, not a hackathon toy.

Keywords:

`calm`, `verified`, `alive`, `modular`, `networked`, `premium`, `trust-first`, `logistics intelligence`, `green signal`, `physical proof`.

Avoid:

- Neon sci-fi overload.
- Too many gradients.
- Raw terminal UI everywhere.
- Random icons.
- Red-heavy danger dashboard.
- Basic courier tracking UI.
- Generic admin dashboard.

---

## 4. Color System

### Core palette

| Token | Value | Usage |
|---|---:|---|
| `primary` | `#B1E09D` | Hero accents, active states, verified badges, soft chart fills |
| `secondary` | `#061C15` | Dark feature cards, navigation active states, critical contrast blocks |
| `accent` | `#82A89C` | Muted green-gray metadata, secondary controls, border glow |
| `background` | `#B1E09D` | Optional full-page brand wash or large section background |
| `shell` | `#EFF4EF` | App-level gray-green canvas around dashboard |
| `surface` | `#FFFFFF` | Main cards, panels, sidebar, topbar |
| `surface-muted` | `#F6FAF7` | Secondary card interiors and disabled areas |
| `surface-dark` | `#061C15` | Dark route card, live relay card, high-emphasis demo widget |
| `text-primary` | `#111827` | Main readable text |
| `text-secondary` | `#4B5563` | Subtext and body metadata |
| `text-muted` | `#8A9A94` | Inactive nav, subtle labels |
| `border` | `#D1DEDC` | Card borders, input borders, separators |
| `success` | `#2F8F5B` | Accepted scans, trusted hubs, green LEDs |
| `warning` | `#C8A43D` | Watch/risky state, cold-chain warning |
| `danger` | `#DC4A45` | Blocked scans, quarantine, tamper |

### Usage ratio

Use approximately:

- 65% white/soft shell surfaces.
- 20% deep green structural emphasis.
- 10% Aether primary green accents.
- 5% warning/danger colors.

Red should only appear when something is genuinely blocked, quarantined, or tampered. This makes the fake scan demo visually stronger.

---

## 5. Typography System

### Main UI and Body Font

Use **Inter** for:

- Dashboard title.
- Navigation labels.
- Card titles.
- Metric numbers.
- Buttons.
- Status text.
- Table rows.
- Body copy.
- Dashboard subtitles.
- Empty-state explanatory copy.

### Technical font

Use **JetBrains Mono** for:

- `MED-104`.
- `HUB-A` / `HUB-B`.
- `ESP-NOW`.
- `ACCEPTED`, `BLOCKED`, `REROUTED`.
- API payload labels.
- Event IDs.
- Trust deltas.
- Latency metrics.

### Type scale

| Element | Font | Size | Weight |
|---|---|---:|---:|
| Page title | Inter | 36-44px | 600 |
| Section heading | Inter | 22-28px | 600 |
| Card title | Inter | 16-20px | 600 |
| Metric number | Inter | 42-56px | 500 |
| Body copy | Inter | 14-16px | 400 |
| Status label | JetBrains Mono | 11-12px | 600 |
| Button | Inter | 14-16px | 600 |

---

## 6. Main Dashboard Layout

The dashboard should follow the uploaded inspiration image structure.

### Overall shell

```text
Full page background: #EFF4EF or very light gray-green
  └── Large rounded app shell, white/near-white, 32px radius
        ├── Left sidebar
        └── Main dashboard area
              ├── Topbar
              ├── Header row
              ├── KPI cards
              └── Bento dashboard grid
```

### Recommended desktop size

- Canvas: `1440px x 1024px` visual target.
- App shell margin: `48px-64px`.
- Sidebar width: `240px`.
- Main content: remaining width.
- Grid gap: `16px`.
- Card radius: `28px-32px`.
- Card padding: `20px-24px`.

---

## 7. Sidebar Design

### Sidebar brand

Replace the inspiration logo with:

```text
PacketFlow
ImmuneNet
```

or compact:

```text
PacketFlow
```

Logo idea: circular route mark with two connected nodes and a small shield/check inside.

### Sidebar sections

Use these exact navigation items:

```text
MENU
- Dashboard
- Digital Twin
- Parcels
- SmartHubs
- ImmuneNet
- AgentOps

SYSTEM
- Ledger
- Metrics
- Settings
```

### Active state

Active item uses:

- Left vertical pill indicator in `#2F8F5B` or `#061C15`.
- Icon and text in `#061C15`.
- Soft background: `rgba(177, 224, 157, 0.22)`.
- Radius: `18px`.

Inactive item:

- Text: `#8A9A94`.
- Icon: muted stroke.

### Bottom sidebar card

Instead of “Download our Mobile App,” use:

```text
Live Relay Mode
HUB-A → HUB-B
ESP-NOW Active
```

Dark green card, same as the inspiration’s bottom promotional card.

Button:

```text
View Hardware
```

---

## 8. Topbar Design

### Search input

Placeholder:

```text
Search parcel, hub, event...
```

Use rounded input similar to inspiration image.

Add keyboard hint:

```text
⌘ F
```

### Topbar icons

Right side:

- Message/log icon.
- Bell/alert icon.
- User/team pill.

User pill content:

```text
Team Aristotle
FAR AWAY 2026
```

Use a small circular avatar or geometric node icon.

### Header actions

Primary button:

```text
+ Create Parcel
```

Secondary outline button:

```text
Import Scenario
```

Use pill buttons with Aether control radius `48px`.

---

## 9. Header Section

### Page title

```text
Dashboard
```

Subtitle in Inter:

```text
Verify movement, route parcels, and watch the network heal in real time.
```

Do not write too much here. The dashboard should feel operational, not explanatory.

---

## 10. Top KPI Cards

Follow the inspiration image’s four top cards.

### Card 1 — highlighted dark/green card

Title:

```text
Trusted Scans
```

Main number:

```text
24
```

Footer badge:

```text
+6 accepted today
```

Use deep green gradient or dark green card with `#B1E09D` glow.

### Card 2

Title:

```text
Blocked Claims
```

Main number:

```text
10
```

Footer:

```text
Fake scans quarantined
```

Use white card; danger appears only as a tiny badge.

### Card 3

Title:

```text
Active Routes
```

Main number:

```text
12
```

Footer:

```text
PacketFlow live
```

### Card 4

Title:

```text
Risky Hubs
```

Main number:

```text
2
```

Footer:

```text
Under watch
```

### Card interaction

Each KPI card has a small top-right circular arrow icon. Hover lifts card by `-3px` and increases shadow.

---

## 11. Main Bento Grid

Use a 12-column grid.

Recommended layout:

```text
Row 1:
[Digital Twin / Network Map: 6 cols] [PacketFlow Decision: 3 cols] [SmartHub Relay: 3 cols]

Row 2:
[Movement Proof: 4 cols] [ImmuneNet Alerts: 4 cols] [Parcel Queue: 4 cols]

Row 3:
[Hub Trust Board: 4 cols] [Route Progress Gauge: 3 cols] [Demo Controls: 5 cols]
```

If screen is smaller, stack cards in this priority:

1. Digital Twin
2. SmartHub Relay
3. PacketFlow Decision
4. Movement Proof
5. ImmuneNet Alerts
6. Demo Controls
7. Trust Board
8. Metrics

---

## 12. Card-by-Card Specification

## 12.1 Digital Twin Card

### Title

```text
Network Twin
```

### Subtitle

```text
Live parcel movement across trusted hubs
```

### Visual

A simplified graph/map hybrid:

- Hubs as rounded circular nodes.
- Route edges as thin muted green lines.
- Active path as thick `#061C15` or `#2F8F5B` line.
- Parcel dot moving between hubs.
- HUB-A and HUB-B have small hardware badges.
- ESP-NOW handshake shown as an electric pulse between HUB-A and HUB-B.

### Hub node states

| State | Visual |
|---|---|
| Trusted | Green fill or green ring |
| Watch | Amber ring |
| Risky | Amber fill with dark text |
| Quarantined | Red ring and lock icon |
| Physical hardware | Small chip badge |

### Required visible labels

```text
HUB-A
HUB-B
HUB-E
COLD-HUB-C
CUSTOMER-ZONE
```

### Interaction

Clicking a hub opens a small details drawer or tooltip:

```text
HUB-B
Trust: 0.92
Status: Active
Queue: 35%
Cold Chain: No
Last Event: p2p_handshake
```

---

## 12.2 PacketFlow Decision Card

### Title

```text
PacketFlow Decision
```

### Main decision

```text
Next Hop
HUB-B
```

### Reason line

```text
Selected because it preserves the 45-minute SLA while maintaining high hub trust.
```

### Score breakdown

Use compact horizontal bars or rows:

```text
SLA Risk        0.20
Congestion      0.50
Trust Risk      0.08
Condition Risk  0.20
Cost Score      0.30
```

### Formula badge

Small mono label:

```text
weighted_risk_score = 0.293
```

### Visual style

White card with deep green selected-hop pill. Use JetBrains Mono for hub IDs and score.

---

## 12.3 SmartHub Relay Card

This is the main hardware-wow card. It should be visually strong.

### Title

```text
SmartHub Relay
```

### Main content

```text
HUB-A → HUB-B
ESP-NOW Handshake Active
```

### Visual

Use a dark green card like the Time Tracker card in the inspiration image.

Elements:

- Two circular hub nodes.
- Animated pulse between them.
- Parcel chip in center: `MED-104`.
- Status badge: `P2P VERIFIED`.
- OLED mini-icon indicator.

### Status rows

```text
BLE Tag     Verified
RFID        Matched
ESP-NOW     Pre-authorised by HUB-A
LED         Green
```

### CTA

```text
Run Relay Walk
```

Use primary green button on dark card.

---

## 12.4 Movement Proof Card

### Title

```text
Movement Proof
```

### Rows

```text
Parcel ID       MED-104
Hub             HUB-A
GPS Distance    18m / 75m
RFID            Verified
BLE             Verified | RSSI 1.2m
Temperature     24.3°C / 25°C
Tamper          Clear
Decision        ACCEPTED
```

### Visual style

White card with pill badges. Use green check badges for passed checks. Use mono for values.

### Decision state variants

Accepted:

```text
ACCEPTED
Green badge
```

Blocked:

```text
BLOCKED
Red badge
```

Rerouted:

```text
REROUTED
Amber badge
```

---

## 12.5 ImmuneNet Alerts Card

### Title

```text
ImmuneNet Alerts
```

### Alert list examples

```text
BLOCKED
Fake scan at HUB-C — GPS outside geofence

REROUTED
Cold-chain breach — MED-104 sent to COLD-HUB-C

WATCH
HUB-C trust dropped to 0.50
```

### Visual rules

- Keep card white.
- Each alert is a rounded row.
- Left side has a small status dot.
- Red/amber is restrained.
- Use mono status label.

### Click state

Click alert expands:

```text
Failed checks: geofence
Action: QUARANTINE_MOVEMENT_CLAIM
Trust delta: -0.15
Ledger event: EVT-014
```

---

## 12.6 Parcel Queue Card

Inspired by the “Project” list in the image.

### Title

```text
Parcels
```

### CTA

```text
+ New
```

### Rows

```text
MED-104  Medicine      Due: 45m SLA
FOOD-221 Fresh Food    Due: 30m SLA
LUX-088  Luxury Goods  Due: 90m SLA
AID-502  Relief Kit    Due: 60m SLA
```

Each row has:

- Small category icon.
- Parcel ID in mono.
- Type label.
- SLA or due status.

---

## 12.7 Hub Trust Board Card

Inspired by the collaboration list in the image.

### Title

```text
Hub Trust Board
```

### Rows

```text
HUB-A        0.99   Trusted
HUB-B        0.92   Trusted
HUB-C        0.50   Risky
COLD-HUB-C   0.95   Trusted
HUB-E        0.88   Trusted
```

### Status badges

| Status | Badge |
|---|---|
| Trusted | green |
| Watch | muted amber |
| Risky | amber/red |
| Quarantined | red |

Add small sparkline-style trust decay if time permits.

---

## 12.8 Route Progress Gauge Card

Inspired by the circular progress card in the image.

### Title

```text
Route Progress
```

### Main gauge

```text
41%
Relay Complete
```

### Legend

```text
Completed
In Progress
Pending
```

Use Aether green for completed, dark green for in progress, diagonal hatch for pending, matching the inspiration card’s visual rhythm.

---

## 12.9 Demo Controls Card

This is the judge interaction panel.

### Title

```text
Demo Controls
```

### Buttons

```text
Fail HUB-B
Inject Fake Scan
Raise Temperature
Trigger Traffic Jam
Reset Demo
```

### Button hierarchy

- Primary/demo-safe action: deep green filled.
- Scenario buttons: white with green border.
- Dangerous action: small red icon/badge, not full red button.

### Feedback area

After action:

```text
AgentOps detected hub overload.
PacketFlow rerouted MED-104 through HUB-D.
```

---

## 13. Page Variants

## 13.1 Dashboard Page

Purpose: main judge demo.

Must include:

- KPI cards.
- Digital twin.
- PacketFlow decision.
- SmartHub Relay.
- Movement Proof.
- ImmuneNet Alerts.
- Demo Controls.

This is the page opened during the live demo.

## 13.2 Digital Twin Page

Purpose: scale proof.

Layout:

- Full-width network map.
- Left filter rail: vans, drones, bots, cold hubs.
- Right drawer: selected hub/parcel details.
- Bottom timeline of events.

Visual:

- More map-heavy.
- Animated parcels.
- What-if controls pinned bottom-right.

## 13.3 Parcels Page

Purpose: parcel ledger and individual proof history.

Layout:

- Parcel table.
- Status filters.
- Selected parcel card.
- Movement timeline.
- Export proof button.

## 13.4 SmartHubs Page

Purpose: physical hardware and trust network proof.

Layout:

- HUB-A and HUB-B live cards.
- ESP-NOW handshake log.
- OLED state preview.
- LED state preview.
- RFID/BLE/GPS proof rows.

## 13.5 ImmuneNet Page

Purpose: anomaly engine proof.

Layout:

- Six immune checks as cards.
- Alert feed.
- Blocked movement claims.
- Trust impact chart.

Six cards:

```text
Geofence
Speed
Route Graph
Clone Scan
Cold Chain
Tamper
```

## 13.6 AgentOps Page

Purpose: autonomous replanning proof.

Layout:

- Disruption feed.
- Current route vs new route.
- Agent action trace.
- Notification preview.

---

## 14. Component Specification

## 14.1 Card

```css
.card {
  background: #FFFFFF;
  border: 1px solid #D1DEDC;
  border-radius: 32px;
  padding: 24px;
  box-shadow: 0 12px 36px rgba(6, 28, 21, 0.06);
}
```

Hover:

```css
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 48px rgba(6, 28, 21, 0.10);
}
```

## 14.2 Dark feature card

```css
.card-dark {
  background: radial-gradient(circle at 80% 20%, rgba(177, 224, 157, 0.22), transparent 28%), #061C15;
  color: #FFFFFF;
  border-radius: 32px;
  border: 1px solid rgba(177, 224, 157, 0.24);
}
```

Use for:

- SmartHub Relay.
- Live Relay Mode sidebar card.
- Optional final demo state card.

## 14.3 Button

Primary:

```css
.button-primary {
  background: #061C15;
  color: #FFFFFF;
  border-radius: 9999px;
  padding: 14px 24px;
}
```

Secondary:

```css
.button-secondary {
  background: #FFFFFF;
  color: #061C15;
  border: 1px solid #061C15;
  border-radius: 9999px;
  padding: 14px 24px;
}
```

Soft green:

```css
.button-soft {
  background: #B1E09D;
  color: #061C15;
  border-radius: 9999px;
}
```

## 14.4 Badge

```css
.badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  border-radius: 9999px;
  padding: 5px 9px;
}
```

Badge variants:

```text
ACCEPTED  green background, dark green text
BLOCKED   pale red background, danger text
REROUTED  pale amber background, amber text
P2P       primary green background, deep green text
LIVE      deep green background, white text
```

## 14.5 Input

Search/input fields:

```css
.input {
  background: #FFFFFF;
  border: 1px solid transparent;
  border-radius: 9999px;
  padding: 14px 18px;
  color: #111827;
}
.input:focus {
  border-color: #82A89C;
  box-shadow: 0 0 0 4px rgba(130, 168, 156, 0.16);
}
```

## 14.6 Icon style

Use:

- Thin line icons.
- 1.75px stroke.
- Rounded caps.
- No filled cartoon icons.
- Icons should be green/gray, not multicolor.

Icon suggestions:

```text
Dashboard      grid
Digital Twin   network
Parcels        package
SmartHubs      router/chip
ImmuneNet      shield
AgentOps       activity/bolt
Ledger         list
Metrics        chart
Settings       gear
```

---

## 15. Motion Design

Motion should be smooth and restrained.

### Required motion cues

1. Card hover lift.
2. Staggered dashboard entrance.
3. ESP-NOW pulse animation between HUB-A and HUB-B.
4. Parcel dot moving along route edge.
5. Alert row slide-in when ImmuneNet blocks a scan.
6. Gauge progress sweep.
7. Soft ambient wave/radial pattern inside dark green cards.

### Motion timings

```text
Card hover: 180ms ease-out
Page entrance: 420ms cubic-bezier(0.22, 1, 0.36, 1)
Route movement: 900ms-1400ms
ESP-NOW pulse: 700ms repeating only during event
Alert slide-in: 260ms ease-out
```

Do not use chaotic bouncing. This is a control dashboard.

---

## 16. Dashboard Copy System

Use crisp operational language.

### Good copy

```text
Movement accepted.
GPS geofence passed.
HUB-B selected as next hop.
Fake scan blocked before ledger entry.
Cold-chain risk detected. Rerouting to COLD-HUB-C.
Trust dropped from 0.65 to 0.50.
```

### Avoid

```text
Your package is on the way!
Oops something went wrong.
Amazing AI magic happened.
We optimized everything.
```

### Main product line

```text
Tracking records claims. PacketFlow verifies movement.
```

### Dashboard subtitle

```text
Verify movement, route parcels, and watch the network heal in real time.
```

### Hardware relay line

```text
HUB-B already knows MED-104 is coming. Trust moved before the parcel arrived.
```

---

## 17. State Design

## 17.1 Accepted scan state

Visual:

- Green LED indicator.
- `ACCEPTED` badge.
- Movement proof rows all checked.
- Dashboard edge animates from HUB-A to HUB-B.

Text:

```text
Movement accepted because identity, GPS geofence, route validity, speed plausibility, temperature, and tamper checks passed.
```

## 17.2 Blocked fake scan state

Visual:

- Red LED indicator.
- Alert row slides into ImmuneNet Alerts.
- HUB-C trust score drops.
- Movement claim appears as quarantined, not accepted.

Text:

```text
Scan blocked because scanner GPS was outside HUB-C geofence.
```

## 17.3 Cold-chain breach state

Visual:

- Temperature chip turns amber/red.
- Route line moves toward COLD-HUB-C.
- PacketFlow Decision updates to reroute.

Text:

```text
Cold-chain risk detected. MED-104 exceeded 25°C, so PacketFlow rerouted it to COLD-HUB-C.
```

## 17.4 ESP-NOW handshake state

Visual:

- HUB-A emits pulse.
- Edge between HUB-A and HUB-B flashes once.
- HUB-B card shows incoming.
- SmartHub Relay card status becomes `P2P VERIFIED`.

Text:

```text
Inter-hub handshake received: HUB-A → HUB-B.
```

---

## 18. Responsive Behavior

### Desktop

- Full sidebar visible.
- 12-column bento grid.
- KPI cards in one row.

### Tablet

- Sidebar collapses to icon rail.
- KPI cards become 2x2.
- Digital twin becomes full-width.

### Mobile

- Bottom navigation.
- KPI cards horizontal scroll.
- Digital twin first.
- Cards stack vertically.
- Demo controls become sticky bottom sheet.

Mobile is not the main hackathon demo target, but it should not break.

---

## 19. Implementation Notes for Codex / Frontend Builder

### Recommended stack

```text
React + Vite
TypeScript
Tailwind CSS
Lucide React icons
Framer Motion
React Flow or Cytoscape.js
Recharts
```

### Tailwind token mapping

```js
colors: {
  aether: {
    primary: '#B1E09D',
    secondary: '#061C15',
    accent: '#82A89C',
    shell: '#EFF4EF',
    surface: '#FFFFFF',
    muted: '#F6FAF7',
    border: '#D1DEDC',
    text: '#111827',
    subtext: '#4B5563',
    success: '#2F8F5B',
    warning: '#C8A43D',
    danger: '#DC4A45'
  }
}
```

### Border radius mapping

```js
borderRadius: {
  shell: '32px',
  card: '32px',
  control: '48px',
  pill: '9999px'
}
```

### Font mapping

```css
--font-display: 'Inter', sans-serif;
--font-body: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

Use Inter as the default UI and body font. Use JetBrains Mono only for labels, IDs, metrics, and technical metadata.

---

## 20. Exact First Screen Content

### Sidebar

```text
PacketFlow

MENU
Dashboard
Digital Twin
Parcels
SmartHubs
ImmuneNet
AgentOps

SYSTEM
Ledger
Metrics
Settings

Live Relay Mode
HUB-A → HUB-B
ESP-NOW Active
View Hardware
```

### Topbar

```text
Search parcel, hub, event...
Team Aristotle
FAR AWAY 2026
```

### Header

```text
Dashboard
Verify movement, route parcels, and watch the network heal in real time.

+ Create Parcel
Import Scenario
```

### KPI cards

```text
Trusted Scans      24    +6 accepted today
Blocked Claims     10    Fake scans quarantined
Active Routes      12    PacketFlow live
Risky Hubs         2     Under watch
```

### Bento cards

```text
Network Twin
PacketFlow Decision
SmartHub Relay
Movement Proof
ImmuneNet Alerts
Parcels
Hub Trust Board
Route Progress
Demo Controls
```

---

## 21. Judge-Facing UI Priorities

Build these first:

1. Dashboard shell matching the inspiration image.
2. Aether color system applied consistently.
3. KPI cards with PacketFlow metrics.
4. Network Twin with HUB-A/HUB-B and animated route.
5. SmartHub Relay dark card.
6. Movement Proof panel.
7. ImmuneNet Alerts panel.
8. Demo control buttons.

Polish later:

1. Trust board sparklines.
2. Gauge animation.
3. More pages.
4. User profile/dropdowns.
5. Export screens.

---

## 22. Non-Negotiable Guardrails

- Do not use PaperFlow orange.
- Do not use Inter as the main personality font unless fallback is needed.
- Do not make the UI dark mode overall.
- Do not make it look like a courier tracking app.
- Do not make every card green; preserve white breathing space.
- Do not overuse red.
- Do not hide the hardware proof. HUB-A, HUB-B, ESP-NOW, BLE, RFID, GPS, LED must be visible.
- Do not flatten everything into generic cards. Keep bento rhythm and visual hierarchy.
- Do not use fake AI-chatbot framing. This is a protocol dashboard.
- The first viewport must clearly show: parcel movement, route decision, trust proof, and anomaly response.

---

## 23. Final Build Target

The final UI should make a judge understand this within 10 seconds:

1. This is not a tracking app.
2. A parcel is moving through a network.
3. Every movement claim is verified.
4. Hubs have trust scores.
5. Fake scans can be blocked.
6. The physical HUB-A to HUB-B relay is real.
7. The dashboard looks like a real product.

Final one-line design target:

**Aether colors + PaperFlow structure + rounded green SaaS dashboard inspiration + PacketFlow logistics trust content.**
