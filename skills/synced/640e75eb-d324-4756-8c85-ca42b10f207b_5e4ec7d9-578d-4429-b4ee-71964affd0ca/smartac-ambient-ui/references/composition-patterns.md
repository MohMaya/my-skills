# SmartAC Ambient UI — Composition Patterns

These are the **only** approved shapes for the common dashboard building
blocks. Derived from the actual production code in
`alpha-web/apps/contractor-dashboard`. If you catch yourself inventing a new
structure, stop and use one of these.

---

## 1. KPI / Stat card

A single large metric with optional delta. The most common dashboard
building block. **Never** build this out of raw `<div>`s with custom classes
(no `.stat-val`, no `.wtd-val`, no `.metric-number`). Use `.ui-stat`.

### HTML
```html
<div class="ui-card">
  <div class="ui-card-header">
    <div class="ui-card-title">Closed Won</div>
    <div class="ui-card-description">Q1 2026, through Mar 31</div>
  </div>
  <div class="ui-card-content">
    <div class="ui-stat">
      <div class="ui-stat-label">Total</div>
      <div class="ui-stat-value ui-stat-value-lg ui-tabular">$291.8K</div>
      <div class="ui-stat-delta ui-stat-delta-negative">
        <span class="ui-icon ui-icon-3"><!-- svg arrow-down --></span>
        $213.6K behind pace
      </div>
    </div>
  </div>
</div>
```

### React
```tsx
<Card.Root>
  <Card.Header>
    <Card.Title>Closed Won</Card.Title>
    <Card.Description>Q1 2026, through Mar 31</Card.Description>
  </Card.Header>
  <Card.Content>
    <div className="flex flex-col gap-1">
      <span className="text-xs text-text-secondary">Total</span>
      <span className="text-2xl font-medium tabular-nums text-text-primary">$291.8K</span>
      <span className="inline-flex items-center gap-1 text-sm text-status-error-default">
        <CentralIcon name="IconArrowDownRight" radius="2" stroke="1.5" fill="outlined" />
        $213.6K behind pace
      </span>
    </div>
  </Card.Content>
</Card.Root>
```

---

## 2. Stat grid (multiple KPIs in one card)

Replaces the v7 `<div class="stat-strip">` / `<div class="wtd-grid">` anti-pattern.

### HTML
```html
<div class="ui-card">
  <div class="ui-card-header">
    <div class="ui-card-title">Pipeline snapshot</div>
  </div>
  <div class="ui-card-content">
    <div style="display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px;">
      <div class="ui-stat">
        <div class="ui-stat-label">Open deals</div>
        <div class="ui-stat-value ui-tabular">958</div>
      </div>
      <div class="ui-stat">
        <div class="ui-stat-label">Closed 90d</div>
        <div class="ui-stat-value ui-tabular">19</div>
      </div>
      <div class="ui-stat">
        <div class="ui-stat-label">Stalled</div>
        <div class="ui-stat-value ui-tabular ui-text-warning">230</div>
      </div>
      <div class="ui-stat">
        <div class="ui-stat-label">Weighted forecast</div>
        <div class="ui-stat-value ui-tabular">$1.89M</div>
      </div>
    </div>
  </div>
</div>
```

Grid layout uses plain CSS grid. Never use a named custom class for layout.

---

## 3. Status badges (in place of colored text)

Never color a raw `<span>` red/green/yellow to indicate status. Use `.ui-badge`.

### HTML
```html
<span class="ui-badge ui-badge-error">Significantly behind</span>
<span class="ui-badge ui-badge-warning">Stalled</span>
<span class="ui-badge ui-badge-success">On pace</span>
<span class="ui-badge ui-badge-default">Draft</span>
<span class="ui-badge ui-badge-count ui-badge-sm">12</span>
```

### React
```tsx
<Badge color="error">Significantly behind</Badge>
<Badge color="warning">Stalled</Badge>
<Badge color="success">On pace</Badge>
<Badge type="count">12</Badge>
```

---

## 4. Progress bar (replaces v7's custom `.prog-track`)

Use `.ui-progress-track` + `.ui-progress-fill`. Width is the only inline
value allowed. Add `.ui-progress-marker` for an expected-pace tick.

### HTML
```html
<div class="ui-card">
  <div class="ui-card-header">
    <div class="ui-card-title">Annual pacing</div>
    <div class="ui-card-action">
      <span class="ui-badge ui-badge-error">Behind</span>
    </div>
  </div>
  <div class="ui-card-content">
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px;">
      <span class="ui-text-sm ui-text-secondary">$291.8K of $2.05M</span>
      <span class="ui-text-sm ui-tabular ui-text-secondary">14%</span>
    </div>
    <div class="ui-progress-track ui-progress-track-lg">
      <div class="ui-progress-fill" style="width:14%;"></div>
      <div class="ui-progress-marker" style="left:24.7%;" title="Expected by Q1 end"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:6px;">
      <span class="ui-text-xs ui-text-secondary ui-tabular">Actual 14%</span>
      <span class="ui-text-xs ui-text-secondary ui-tabular">Expected 24.7%</span>
    </div>
  </div>
</div>
```

No absolute-positioned dot markers. No overlapping labels.

---

## 4b. Stacked bar + legend (funnel, source mix, rep pipeline)

For HTML artifacts, any multi-colored bar is `.ui-bar-stack` with
`.ui-bar-segment.ui-swatch-series-N` children. The legend is
`.ui-chart-legend` with `.ui-swatch-dot.ui-swatch-series-N` swatches.
Never assign a bespoke `--gtm-*` variable per category — label it in the
legend instead.

### HTML
```html
<div class="ui-card">
  <div class="ui-card-header">
    <div class="ui-card-title">Lead source mix</div>
    <div class="ui-card-description">Share of open pipeline by source</div>
  </div>
  <div class="ui-card-content" style="display:flex; flex-direction:column; gap:12px;">
    <div class="ui-bar-stack ui-bar-stack-lg">
      <div class="ui-bar-segment ui-swatch-series-1" style="width:32%;" title="Paid social — 32%"></div>
      <div class="ui-bar-segment ui-swatch-series-5" style="width:22%;" title="Direct — 22%"></div>
      <div class="ui-bar-segment ui-swatch-series-7" style="width:18%;" title="Organic — 18%"></div>
      <div class="ui-bar-segment ui-swatch-series-2" style="width:14%;" title="Offline — 14%"></div>
      <div class="ui-bar-segment ui-swatch-series-4" style="width:14%;" title="Referrals — 14%"></div>
    </div>
    <div class="ui-chart-legend">
      <span class="ui-chart-legend-item"><span class="ui-swatch-dot ui-swatch-series-1"></span>Paid social</span>
      <span class="ui-chart-legend-item"><span class="ui-swatch-dot ui-swatch-series-5"></span>Direct</span>
      <span class="ui-chart-legend-item"><span class="ui-swatch-dot ui-swatch-series-7"></span>Organic</span>
      <span class="ui-chart-legend-item"><span class="ui-swatch-dot ui-swatch-series-2"></span>Offline</span>
      <span class="ui-chart-legend-item"><span class="ui-swatch-dot ui-swatch-series-4"></span>Referrals</span>
    </div>
  </div>
</div>
```

### React
Use `<Chart>` from `@smartacteam/ambient-web/chart`. It handles the palette
internally from the tokens; do not pass hex colors.

---

## 5. Data table

### HTML
```html
<div class="ui-card">
  <div class="ui-card-header">
    <div class="ui-card-title">Top deals</div>
  </div>
  <table class="ui-table">
    <thead>
      <tr>
        <th>Deal</th>
        <th>Owner</th>
        <th>Stage</th>
        <th style="text-align:right;">Amount</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Cowboy's</td>
        <td>J. Rivera</td>
        <td><span class="ui-badge ui-badge-sm ui-badge-success">Closed won</span></td>
        <td class="ui-tabular" style="text-align:right;">$92,400</td>
      </tr>
      <tr>
        <td>Genz-Ryan</td>
        <td>S. Patel</td>
        <td><span class="ui-badge ui-badge-sm ui-badge-warning">Follow-up</span></td>
        <td class="ui-tabular" style="text-align:right;">$20,600</td>
      </tr>
    </tbody>
  </table>
</div>
```

Note: table sits **inside** `.ui-card` but **outside** `.ui-card-content` so it
spans the full card width. Use right-aligned `ui-tabular` for numeric columns.

---

## 6. App shell (sidebar + header + main)

### HTML
```html
<div style="display:flex; min-height:100vh;">
  <aside class="ui-sidebar">
    <div class="ui-sidebar-header">
      <span class="ui-icon ui-icon-4"><!-- logo svg --></span>
      <span>SmartAC</span>
    </div>
    <nav style="padding:8px 0; display:flex; flex-direction:column; gap:2px;">
      <a href="#" class="ui-sidebar-item is-active">
        <span class="ui-icon ui-icon-4"><!-- svg --></span>Activity
      </a>
      <a href="#" class="ui-sidebar-item">
        <span class="ui-icon ui-icon-4"><!-- svg --></span>Homes
      </a>
    </nav>
  </aside>
  <div style="flex:1; display:flex; flex-direction:column; min-width:0;">
    <header class="ui-app-header">
      <div style="flex:1;"><!-- search --></div>
      <button class="ui-button ui-button-ghost ui-button-icon">
        <span class="ui-icon ui-icon-4"><!-- bell --></span>
      </button>
    </header>
    <main style="flex:1; padding:24px; display:flex; flex-direction:column; gap:16px;">
      <!-- dashboard cards go here -->
    </main>
  </div>
</div>
```

---

## 7. Empty state / callout

Never use raw colored `<div>` warnings (`.warn-box`). Use a card with a
semantic badge and muted description.

### HTML
```html
<div class="ui-card">
  <div class="ui-card-content" style="display:flex; gap:12px; align-items:flex-start; padding-top:20px; padding-bottom:20px;">
    <span class="ui-badge ui-badge-warning ui-badge-sm">Action needed</span>
    <div>
      <div class="ui-text-sm ui-font-medium ui-text-primary">Many open deals have no Amount set in HubSpot</div>
      <div class="ui-text-sm ui-text-secondary" style="margin-top:4px;">Closed-won figures are understated. Require Amount before deals advance past Follow-Up Mtg Booked.</div>
    </div>
  </div>
</div>
```

---

## 8. Page layout rhythm

A dashboard page is a vertical stack of `.ui-card`s inside a main area with
24px padding and 16px gap between cards. Section headings (`.ui-text-xl`)
separate groups.

```html
<main style="padding:24px; display:flex; flex-direction:column; gap:16px;">
  <div>
    <h1 class="ui-text-2xl ui-text-primary">GTM Dashboard</h1>
    <div class="ui-text-sm ui-text-secondary" style="margin-top:4px;">New logos · Q1 2026</div>
  </div>

  <h2 class="ui-text-lg ui-text-primary" style="margin-top:8px;">Annual pacing</h2>
  <div class="ui-card">...</div>

  <h2 class="ui-text-lg ui-text-primary" style="margin-top:8px;">Pipeline</h2>
  <div class="ui-card">...</div>
</main>
```

Never use all-caps section dividers (`.sec-hdr` style). Never use horizontal
rules between sections — the gap does the work.
