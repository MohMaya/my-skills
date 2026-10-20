# Conventions

Read the section for the language you are writing. Case is mechanical. The five steps in the skill decide the words.

## TypeScript and JavaScript

- Variables and functions are `camelCase`. Types, interfaces, and components are `PascalCase`. Module constants are `SCREAMING_SNAKE_CASE` only when immutable and shared.
- No `I` prefix on interfaces. No `Enum` suffix on enums.
- Booleans read as assertions: `isPaid`, `hasAccess`, `canRefund`, `shouldRetry`. Never `paid`, `access`, or `notReady`.
- A component is named for what it renders: `InvoiceTable`, not `TableComponent` or `InvoiceComponent`.
- Props name the role at the call site: `invoice`, `onIssue`, `isPending`. A prop named `data` or `info` is a missing model.
- Files are `kebab-case.ts`, named for the concept they own: `invoice-reminders.ts`, not `utils.ts` or `helpers.ts`.
- Hooks start with `use` and name the behavior: `useInvoiceReminders`.
- Async functions name the IO verb: `fetchInvoice`, `loadWorkspace`, `saveInvoice`. Never `handleSave`.

## Python

- `snake_case` for variables and functions, `PascalCase` for classes, a leading underscore for private names, dunders only for protocol methods.
- No abbreviations: `configuration`, not `cfg`; `request`, not `req`.
- Predicates read as assertions: `is_paid`, `has_access`, `can_refund`.
- Modules are `snake_case.py`, named for the concept: `invoice_reminders.py`.
- Constants are `SCREAMING_SNAKE_CASE` and name the role, not the value: `MAX_RETRY_ATTEMPTS`, not `THREE`.

## Go

- `MixedCaps`, never underscores. An initialism keeps one case: `appID`, `ServeHTTP`, `xmlAPI`.
- Short names follow scope. `i` in a loop, `c` for a `Client` receiver, `ctx` for a context, `err` for an error. A package-level value gets a full name.
- The package name qualifies every export, so drop it: `chubby.File`, not `chubby.ChubbyFile`.
- No `Get` prefix on getters: `Counts`, not `GetCounts`. Use `Fetch` or `Compute` when the call is expensive.
- Interfaces describe behavior and usually end in `-er`: `Reader`, `Notifier`. One method, one interface.
- Receivers are one or two letters of the type, and the same letters on every method.

## Rust

- `snake_case` for functions and variables, `UpperCamelCase` for types and enum variants, `SCREAMING_SNAKE_CASE` for constants and statics.
- Conversions use the standard prefixes: `as_` is free and borrowed, `to_` allocates or costs, `into_` consumes.
- Getters drop `get_`: `first()`, not `get_first()`. Keep `get` for a container with one obvious thing to get.
- Iterators follow `iter`, `iter_mut`, and `into_iter`, and the returned type matches the method.
- Error types use verb-object-error order: `ParseAddrError`, not `AddrParseError`.

## Swift

- `lowerCamelCase` for values, functions, and enum cases. `UpperCamelCase` for types and protocols.
- The call site must read as an English phrase: `employees.remove(at: index)`, not `employees.remove(index)`.
- Booleans read as assertions: `isEmpty`, `intersects(_:)`.
- A protocol that describes a thing is a noun (`Collection`). A protocol that describes a capability ends in `-able`, `-ible`, or `-ing` (`Equatable`, `ProgressReporting`).
- Name by role, not type: `greeting`, not `string`; `supplier`, not `widgetFactory`.
- Acronyms keep one case: `utf8Bytes`, `userSMTP`, `isRepresentableAsASCII`.

## SQL and API fields

- Tables and columns are `snake_case`. A primary key is `id`. A foreign key is `<singular>_id`: `invoice_id`.
- Booleans take `is_` or `has_`: `is_paid`, `has_shipped`.
- Money carries its unit and scale: `total_cents`, not `total`.
- Timestamps end in `_at`, dates in `_on`, durations in `_ms` or `_seconds`. Never a bare `time` or `date`.
- An API field keeps the glossary term. Do not rename `workspace` to `tenant` at the boundary.

## Files, branches, tickets

- Files and directories are `kebab-case` and name the concept: `invoice-reminders/`, not `misc/`.
- Branches are `sc/<TICKET>-<imperative>`: `sc/INV-42-retry-backoff`.
- A ticket title names the outcome in the imperative: `Retry failed invoice deliveries`, not `Invoice delivery stuff`.
