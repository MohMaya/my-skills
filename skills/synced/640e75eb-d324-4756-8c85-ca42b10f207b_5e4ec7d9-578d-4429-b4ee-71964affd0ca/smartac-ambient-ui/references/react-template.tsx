// SmartAC Ambient UI — React artifact starter
//
// Copy this as the skeleton when building a React/TSX artifact. Every
// container here is a real primitive from @smartacteam/ambient-web.
// Do not replace any of these imports with raw <div>/<button>/<span>.

import { Badge } from "@smartacteam/ambient-web/badge";
import { Button } from "@smartacteam/ambient-web/button";
import { Card } from "@smartacteam/ambient-web/card";
import { CentralIcon } from "@smartacteam/ambient-web/icon";
import { Separator } from "@smartacteam/ambient-web/separator";
import { Sidebar } from "@smartacteam/ambient-web/sidebar";
import { Table } from "@smartacteam/ambient-web/table";

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-surface-inset text-text-primary">
      <Sidebar.Root collapsible="icon">
        <Sidebar.Header className="h-14 flex-row border-b border-stroke-default">
          <div className="flex items-center gap-2 px-4">
            <CentralIcon name="IconRescueRing" radius="2" stroke="1.5" fill="outlined" className="size-4" />
            <span className="text-sm font-medium">SmartAC</span>
          </div>
        </Sidebar.Header>
        <Sidebar.Content>
          <Sidebar.Group>
            <Sidebar.GroupContent>
              <Sidebar.Menu>
                {[
                  { title: "Activity", icon: "IconElectrocardiogram", active: true },
                  { title: "Homes", icon: "IconHomeLine" },
                  { title: "Customers", icon: "IconPeople" },
                  { title: "Orders", icon: "IconPackageDelivery" },
                ].map((item) => (
                  <Sidebar.MenuItem key={item.title}>
                    <Sidebar.MenuButton isActive={item.active}>
                      <CentralIcon
                        name={item.icon as "IconElectrocardiogram"}
                        radius="2"
                        stroke="1.5"
                        fill="outlined"
                        className="size-4"
                      />
                      <span>{item.title}</span>
                    </Sidebar.MenuButton>
                  </Sidebar.MenuItem>
                ))}
              </Sidebar.Menu>
            </Sidebar.GroupContent>
          </Sidebar.Group>
        </Sidebar.Content>
      </Sidebar.Root>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 flex h-14 items-center gap-2 border-b border-stroke-default bg-surface-default pr-5 pl-2">
          <div className="flex-1" />
          <Button variant="ghost" size="icon">
            <CentralIcon name="IconBell2" radius="2" stroke="1.5" fill="outlined" />
          </Button>
        </header>

        <main className="flex flex-1 flex-col gap-4 p-6">
          <div>
            <h1 className="text-2xl font-medium tracking-tight text-text-primary">GTM Dashboard</h1>
            <p className="mt-1 text-sm text-text-secondary">New logos · Q1 2026</p>
          </div>

          <Card.Root>
            <Card.Header>
              <Card.Title>Pipeline snapshot</Card.Title>
              <Card.Description>Trailing 90 days</Card.Description>
              <Card.Action>
                <Badge color="error">Behind pace</Badge>
              </Card.Action>
            </Card.Header>
            <Card.Content>
              <div className="grid grid-cols-4 gap-5">
                {[
                  { label: "Closed won", value: "$291.8K" },
                  { label: "Deals closed", value: "19" },
                  { label: "Open deals", value: "958" },
                  { label: "Stalled", value: "230", tone: "warning" as const },
                ].map((s) => (
                  <div key={s.label} className="flex flex-col gap-1">
                    <span className="text-xs text-text-secondary">{s.label}</span>
                    <span
                      className={`text-2xl font-medium tabular-nums ${
                        s.tone === "warning"
                          ? "text-status-warning-default"
                          : "text-text-primary"
                      }`}
                    >
                      {s.value}
                    </span>
                  </div>
                ))}
              </div>
            </Card.Content>
          </Card.Root>

          <Card.Root>
            <Card.Header>
              <Card.Title>Top deals</Card.Title>
            </Card.Header>
            <Table.Root>
              <Table.Header>
                <Table.Row>
                  <Table.Head>Deal</Table.Head>
                  <Table.Head>Owner</Table.Head>
                  <Table.Head>Stage</Table.Head>
                  <Table.Head className="text-right">Amount</Table.Head>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                <Table.Row>
                  <Table.Cell>Cowboy's</Table.Cell>
                  <Table.Cell>J. Rivera</Table.Cell>
                  <Table.Cell>
                    <Badge size="sm" color="success">Closed won</Badge>
                  </Table.Cell>
                  <Table.Cell className="text-right tabular-nums">$92,400</Table.Cell>
                </Table.Row>
              </Table.Body>
            </Table.Root>
          </Card.Root>
        </main>
      </div>
    </div>
  );
}
