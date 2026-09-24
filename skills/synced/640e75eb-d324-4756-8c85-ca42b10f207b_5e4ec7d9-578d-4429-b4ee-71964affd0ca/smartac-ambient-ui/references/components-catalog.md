# SmartAC Ambient UI — Component Catalog

The full production React primitives. For **React/TSX artifacts**, import from
`@smartacteam/ambient-web/<component>`. For **HTML artifacts**, use the
`.ui-*` class equivalents from `primitives.css`.

Never build a custom equivalent of anything in this list.

## Import paths

Every component is a subpath import:

```tsx
import { Button } from "@smartacteam/ambient-web/button";
import { Badge } from "@smartacteam/ambient-web/badge";
import { Card } from "@smartacteam/ambient-web/card";
import { Input } from "@smartacteam/ambient-web/input";
import { Label } from "@smartacteam/ambient-web/label";
import { Table } from "@smartacteam/ambient-web/table";
import { DataTable } from "@smartacteam/ambient-web/data-table";
import { Dialog } from "@smartacteam/ambient-web/dialog";
import { Popover } from "@smartacteam/ambient-web/popover";
import { Tooltip } from "@smartacteam/ambient-web/tooltip";
import { Tabs } from "@smartacteam/ambient-web/tabs";
import { Select } from "@smartacteam/ambient-web/select";
import { Switch } from "@smartacteam/ambient-web/switch";
import { Checkbox } from "@smartacteam/ambient-web/checkbox";
import { RadioGroup } from "@smartacteam/ambient-web/radio-group";
import { Avatar } from "@smartacteam/ambient-web/avatar";
import { Sidebar } from "@smartacteam/ambient-web/sidebar";
import { Separator } from "@smartacteam/ambient-web/separator";
import { Menu } from "@smartacteam/ambient-web/menu";
import { Toast } from "@smartacteam/ambient-web/toast";
import { CentralIcon } from "@smartacteam/ambient-web/icon";
import { Chart } from "@smartacteam/ambient-web/chart";
import { Gauge } from "@smartacteam/ambient-web/gauge";
import { Progress } from "@smartacteam/ambient-web/progress";
import { Spinner } from "@smartacteam/ambient-web/spinner";
import { Skeleton } from "@smartacteam/ambient-web/skeleton";
```

## Full primitive inventory

| Primitive | Import | HTML emulation class |
|-----------|--------|----------------------|
| Alert | `@smartacteam/ambient-web/alert` | `.ui-card` + `.ui-badge-*` |
| AlertDialog | `@smartacteam/ambient-web/alert-dialog` | (React only) |
| Avatar | `@smartacteam/ambient-web/avatar` | — |
| AvatarGroup | `@smartacteam/ambient-web/avatar-group` | — |
| **Badge** | `@smartacteam/ambient-web/badge` | `.ui-badge .ui-badge-{default,success,warning,error,info,count}` |
| Breadcrumb | `@smartacteam/ambient-web/breadcrumb` | — |
| **Button** | `@smartacteam/ambient-web/button` | `.ui-button .ui-button-{default,primary,ghost,text,destructive}` + `.ui-button-{sm,lg,icon}` |
| ButtonGroup | `@smartacteam/ambient-web/button-group` | — |
| Calendar | `@smartacteam/ambient-web/calendar` | (React only) |
| **Card** | `@smartacteam/ambient-web/card` | `.ui-card`, `.ui-card-header`, `.ui-card-title`, `.ui-card-description`, `.ui-card-action`, `.ui-card-content`, `.ui-card-footer` |
| **Chart** | `@smartacteam/ambient-web/chart` | Compose with `.ui-bar-stack` + `.ui-bar-segment.ui-swatch-series-N` and `.ui-chart-legend`. Never inline `var(--primitives-color-dataviz-*)`. |
| Checkbox | `@smartacteam/ambient-web/checkbox` | — |
| Collapsible | `@smartacteam/ambient-web/collapsible` | — |
| Command | `@smartacteam/ambient-web/command` | (React only) |
| ContextMenu | `@smartacteam/ambient-web/context-menu` | (React only) |
| **DataTable** | `@smartacteam/ambient-web/data-table` | `.ui-table` |
| Dialog | `@smartacteam/ambient-web/dialog` | (React only) |
| Empty | `@smartacteam/ambient-web/empty` | `.ui-card` with `.ui-text-secondary` content |
| **Gauge** | `@smartacteam/ambient-web/gauge` | (use Progress emulation or SVG) |
| HoverCard | `@smartacteam/ambient-web/hover-card` | (React only) |
| **Icon (CentralIcon)** | `@smartacteam/ambient-web/icon` | inline SVG inside `.ui-icon .ui-icon-{3,4,5,6}` |
| **Input** | `@smartacteam/ambient-web/input` | `.ui-input` |
| InputGroup | `@smartacteam/ambient-web/input-group` | — |
| Kbd | `@smartacteam/ambient-web/kbd` | — |
| **Label** | `@smartacteam/ambient-web/label` | `.ui-label` |
| Logo / LogoMark | `@smartacteam/ambient-web/logo` | — |
| Menu | `@smartacteam/ambient-web/menu` | (React only) |
| Popover | `@smartacteam/ambient-web/popover` | (React only) |
| **Progress** | `@smartacteam/ambient-web/progress` | `.ui-progress-track` + `.ui-progress-fill` (+ `.ui-progress-marker`) |
| RadioGroup | `@smartacteam/ambient-web/radio-group` | — |
| Scroll | `@smartacteam/ambient-web/scroll` | — |
| Select | `@smartacteam/ambient-web/select` | (React only) |
| **Separator** | `@smartacteam/ambient-web/separator` | `.ui-separator`, `.ui-separator-vertical` |
| Sheet | `@smartacteam/ambient-web/sheet` | (React only) |
| **Sidebar** | `@smartacteam/ambient-web/sidebar` | `.ui-sidebar`, `.ui-sidebar-header`, `.ui-sidebar-item` |
| Skeleton | `@smartacteam/ambient-web/skeleton` | — |
| Spinner | `@smartacteam/ambient-web/spinner` | — |
| Surface | `@smartacteam/ambient-web/surface` | `.ui-surface-{inset,default,elevated,offset}` |
| Switch | `@smartacteam/ambient-web/switch` | — |
| **Table** | `@smartacteam/ambient-web/table` | `.ui-table` |
| Tabs | `@smartacteam/ambient-web/tabs` | (React only) |
| Textarea | `@smartacteam/ambient-web/textarea` | `.ui-input` (as textarea) |
| ThemeMenu | `@smartacteam/ambient-web/theme-menu` | — |
| Toast / Toaster | `@smartacteam/ambient-web/toast` | (React only) |
| Toggle / ToggleGroup | `@smartacteam/ambient-web/toggle` | — |
| Tooltip | `@smartacteam/ambient-web/tooltip` | (React only) |

## Compound component shape

Compound primitives (Card, Sidebar, Tabs, Dialog, Menu, Select, Popover) are
exported as a namespace. Always use `<Component.Part>`:

```tsx
<Card.Root>
  <Card.Header>
    <Card.Title>Pipeline</Card.Title>
    <Card.Description>Trailing 90 days</Card.Description>
    <Card.Action>
      <Button variant="ghost" size="icon-sm">
        <CentralIcon name="IconDotsHorizontal" radius="2" stroke="1.5" fill="outlined" />
      </Button>
    </Card.Action>
  </Card.Header>
  <Card.Content>{/* body */}</Card.Content>
  <Card.Footer>{/* actions */}</Card.Footer>
</Card.Root>
```

## Icons — CentralIcon

Icons come from `@central-icons-react/all`, accessed via `<CentralIcon name="..." />`.

```tsx
<CentralIcon name="IconBell2" radius="2" stroke="1.5" fill="outlined" />
<CentralIcon name="IconCheckCircle" radius="2" stroke="1.5" fill="outlined" className="text-status-success-default" />
```

Common names: `IconBell2`, `IconCheckCircle`, `IconAlertCircle`, `IconArrowUp`,
`IconArrowDown`, `IconArrowUpRight`, `IconArrowDownRight`, `IconDotsHorizontal`,
`IconPlus`, `IconMinus`, `IconX`, `IconSearch`, `IconFilter`, `IconChevronDown`,
`IconChevronRight`, `IconHomeLine`, `IconPeople`, `IconPackageDelivery`,
`IconElectrocardiogram`, `IconRescueRing`, `IconCalendar`, `IconClock`,
`IconTrendUp`, `IconTrendDown`, `IconDollar`, `IconBolt`.

Always pass `radius="2" stroke="1.5" fill="outlined"` unless you have a reason
to deviate.

For **HTML artifacts**: use inline SVG inside `<span class="ui-icon ui-icon-4">...</span>`.
The icon inherits the current text color. Never substitute emoji or HTML
entities (`▶`, `✓`, `⚠`, `✕`, `&#9654;`, `&#10005;`).

## Token classes (when composing around primitives)

Inside `className`, use these Tailwind-style classes — they exist in the real
app's Tailwind config and in `primitives.css` for HTML artifacts.

| Class | Maps to |
|-------|---------|
| `bg-surface-default` | `--app-color-surface-default` |
| `bg-surface-inset` | `--app-color-surface-inset` |
| `bg-surface-elevated` | `--app-color-surface-elevated` |
| `bg-status-success-subtle` / `-warning-` / `-error-` / `-info-` | status fills |
| `text-text-primary` | primary text |
| `text-text-secondary` | muted text |
| `text-status-success-default` / `-warning-` / `-error-` / `-info-` | status text |
| `border-stroke-default` | subtle border |
| `border-stroke-strong` | stronger border |
| `border-status-{level}-border` | status border |

Spacing is plain Tailwind: `p-6`, `px-5`, `gap-3`, `flex`, `grid`. Radii use
`rounded-md`, `rounded-lg`, `rounded-full`. Never set `padding`, `margin`,
`background-color`, `color`, or `border-color` as inline style.
