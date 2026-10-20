---
name: naming
description: Name variables, functions, types, files, API fields, branches, and domain concepts. Use before introducing any new name, when a name is hard to choose, and when reviewing a diff for vague, noisy, or misleading names.
---

# Naming

A name is a claim about what a thing is. It is read far more often than it is written, and it is the smallest unit of design. A wrong name gives every reader the wrong model before they read the body.

Never keep the first name that compiles. Run the five steps.

**Dvandva.** Run `dvandva` before a new public or domain name.

## The five steps

### 1. Say it in one sentence

Write the sentence the name compresses: `This <kind> <does what> for <whom>.`

- `This function reserves stock for an order.` becomes `reserveStock`.
- `This value is the number of days since the invoice was issued.` becomes `daysSinceIssued`.
- `This type is a customer who has paid.` becomes `PayingCustomer`.

If the sentence needs "and", the thing does two jobs. Split it, then name each part. A name that is hard to choose is a design signal, not a vocabulary gap.

**Done when** the sentence has one verb and one object.

### 2. Use the word the domain already uses

Search `GLOSSARY.md`, the API schema, the UI copy, and the nearest module. If the business says "workspace", the code says `workspace`, never `tenant`, `account`, or `org`.

- Reuse the existing term even when you would have chosen a different one.
- If no term is precise, coin one, define it in a sentence, and add it to `GLOSSARY.md` in the same change. `domain-modeling` owns the format.
- If two terms exist for one concept, pick one and migrate every use. Never add a third.

**Done when** the name uses the caller's word, and a new domain term is recorded.

### 3. Match the shape to the kind

| Kind | Shape | Example |
| --- | --- | --- |
| Type, value, property | noun | `Invoice`, `totalCents`, `workspace` |
| Function that changes state | verb and object | `issueInvoice`, `reserveStock` |
| Function that returns a value | noun phrase when cheap and pure, verb and object otherwise | `invoiceTotal`, `findOverdue` |
| Boolean | assertion | `isPaid`, `hasAccess`, `shouldRetry`, `canRefund` |
| Event | past tense | `InvoiceIssued`, `PaymentFailed` |
| Command, job, branch | imperative | `IssueInvoice`, `sc/INV-42-retry-backoff` |
| Collection | plural noun | `invoices`, `retryAttempts` |
| Module, package, file | the concept it owns | `billing/`, `invoice-reminders.ts` |

A function that returns a boolean is a question. A function that mutates is an instruction. A name that reads as one and behaves as the other is a lie.

**Done when** the part of speech matches the kind, and a value-returning function keeps the one shape its cost earns.

### 4. Cut what the scope already says

Every word must add information the call site does not already carry.

| Remove | Bad | Good |
| --- | --- | --- |
| Type echo | `usersArray`, `nameString`, `numUsers` | `users`, `name`, `userCount` |
| Scope echo | `User.userName`, `InvoiceService.sendInvoice` | `User.name`, `send` |
| Noise suffix | `UserData`, `OrderInfo`, `ConfigObject` | `User`, `Order`, `Config` |
| Encoding | `strName`, `m_total`, `IInvoice` | `name`, `total`, `Invoice` |
| Placeholder | `data`, `info`, `obj`, `tmp`, `foo` | the role: `unpaidInvoices`, `retryDelayMs` |
| Generic verb | `handleData`, `processOrder`, `UserManager` | the job: `persistInvoice`, `cancelOrder` |

Keep the type word only when two values of different shapes share a scope, such as `limitRaw` and `limit`.

Length follows scope:

| Scope | Words | Example |
| --- | --- | --- |
| A line or two | 1, or the language's idiom | `i`, `err`, `r`, `ok` |
| One function | 1 to 2 | `retryDelay`, `unpaidInvoices` |
| Public API or module | 2 to 3, precise | `scheduleRetry`, `InvoiceRepository` |
| Domain type or concept | 1 exact noun | `Invoice`, `Subscription` |

The wider the scope and the farther the use from the declaration, the more the name must carry.

**Done when** every remaining word is information the reader does not already have.

### 5. Test the call site and the promise

Read the use aloud as a sentence. Then check the candidate against the seven failures:

1. **Vague.** `data`, `info`, `result`, `item`, `value`, `obj`. What is it? Name the role. The gate rejects `data`, `info`, `obj`, `object`, `val`, `tmp`, `temp`, `thing`, `stuff`, `misc`, `foo`, `bar`, `baz`, `qux`, and `dummy` on sight. `result`, `item`, and `value` are yours to judge, because a one-line scope can make them precise.
2. **Type echo.** `userString`, `usersArray`, `numUsers`. The compiler already knows.
3. **Noise.** `UserData`, `OrderInfo`, `ConfigObject`, `UserManager`, `StringUtil`. These words promise a distinction they do not make.
4. **Scope echo.** `User.userName`, `InvoiceService.sendInvoice`. The receiver already said it.
5. **Two jobs.** `handleData`, `processOrder`, `DocumentProcessor`. Name the job or split the thing.
6. **Lie.** `getUser` that writes, `isOpen` that returns a count, `checkX` that mutates, `load` that is pure. Match the verb to the cost and the effect.
7. **Synonym drift.** `fetch`, `get`, `retrieve`, and `load` for one operation. Pick one and use it everywhere.

`get` is cheap and pure. `fetch` and `load` do IO. `compute` is expensive and pure. `find` may return nothing. `ensure` creates when absent. `create` fails when present. `upsert` does both. `remove` takes something out of a collection. `delete` destroys it. `send`, `publish`, and `emit` name three different fan-outs.

**Done when** the call site reads correctly, and the name promises nothing the code does not do.

## Consistency

A codebase is a lexicon. One concept keeps one name everywhere, and one name keeps one meaning everywhere.

- When two names exist for one concept, pick one and migrate every use in the same change.
- When one name covers two concepts, split it. `block` for a file block and a disk block becomes `fileBlock` and `diskBlock`.
- Pair opposites by the same rule: `open` and `close`, `start` and `stop`, `begin` and `end`, `add` and `remove`, `create` and `delete`, `lock` and `unlock`.
- Record the chosen term in `GLOSSARY.md` so the next agent inherits the decision instead of re-litigating it.

## Naming a concept

The same procedure applies to a product concept, an API field, a ticket title, a branch, and a skill name.

- Name the concept after the user's job, not your implementation. `Workspace` beats `TenantContainer`.
- Define it in one sentence without using the word. If you cannot, it is two concepts.
- Use the name unchanged in code, UI copy, API fields, docs, tickets, and the glossary. A concept with two names has no name.
- Before coining a term, check the glossary and the schema. A synonym is a second source of truth.

## Before you commit

1. Run `python3 ~/.agents/hooks/naming-gate.py` in the repository. It checks added lines and rejects vacuous names, noise suffixes on types, and a vague verb paired with a generic object.
2. Read the diff for names only. The gate catches the objective subset. Step 5 catches the rest.
3. When a framework or a protocol fixes the name, mark the line `// naming: ignore <reason>`. Every other failure is a rename.
4. If a rename touches more than the change, commit the rename separately from the behavior change.

Language casing and idioms are in [references/conventions.md](references/conventions.md).
