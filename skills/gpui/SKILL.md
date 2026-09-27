---
name: gpui
description: Build or review native Rust desktop UI with GPUI, including entities, rendering, actions, focus, background work, and component selection. Use for standalone GPUI apps and GPUI changes in existing apps.
---

# GPUI application development

Read `~/.agents/STANDARDS/Stack/Desktop.md` for stack policy, design authority, architecture, and delivery checks.
This skill owns GPUI implementation conventions. `rust-best-practices` supplies Rust guidance; `gpui-test` supplies deterministic test techniques.

## Resolve the actual API

Read the application's Cargo manifest, lockfile, toolchain, existing components, and approved design.
Identify the resolved GPUI version and any component framework before selecting examples.
Read matching upstream source or versioned documentation for every unfamiliar context, event, or rendering API.
Confirm a matching existing call site. Use a minimal example only when API uncertainty remains.

The [GPUI README](https://github.com/zed-industries/zed/blob/main/crates/gpui/README.md) links platform setup, ownership, and accessibility documentation.
The [official examples](https://github.com/zed-industries/zed/tree/main/crates/gpui/examples) cover input, menus, windows, and lists.
Resolve these moving links to the project's pinned release or revision before copying code.

## Own state and rendering

Represent persistent UI state with entities and update it through the matching GPUI contexts.
Keep entity reads and updates short; avoid reentrant mutable access to the same entity.
Use weak entity references when callbacks or tasks should not keep a view alive.
Handle failed upgrades when the user closes a view before work completes.

Use `Render` and existing element primitives for composition. Add custom elements only when those primitives cannot express the approved interaction.
Keep stable element identities for stateful controls and list items.
Notify observers and request redraws when relevant state changes; avoid unconditional update loops.
Use virtualized lists for large collections so render work follows visible content.

## Keep work and input responsive

Use GPUI's foreground and background executors according to thread affinity.
Move blocking IO and expensive computation off the UI thread, then apply results through the supported context APIs.
Own task handles and subscriptions for their intended lifetime. Cancel obsolete work or reject stale results before applying them.
Add another async runtime only when a dependency requires it and its integration has an explicit lifetime and shutdown boundary.
Rust reference examples using Tokio do not establish that GPUI needs Tokio.

Use GPUI actions, key bindings, and focus APIs for commands and keyboard navigation.
Use the framework's text-input facilities for selection, composition, and IME behavior.
Verify focus restoration after dialogs and keyboard access to the changed controls.

## Choose components deliberately

Reuse the application's existing components and design tokens.
For missing controls, evaluate [Longbridge GPUI Kit](https://github.com/longbridge/gpui-kit) against the design and pinned GPUI version.
It is an optional component framework, not part of the required stack.
When adopting it, inspect its current `skills/gpui-kit` and `skills/gpui-kit-design-guides` guidance and compatible dependency recipe.
Verify those paths against upstream before installing; indexed skill names can lag repository changes.

Identify the owning crate for every imported extension trait or helper.
Zed's `ui` helpers and Longbridge's component helpers are not automatically available in a standalone GPUI application.

## Verify behavior

Use `gpui-test` when tests depend on GPUI contexts, scheduling, or fake time.
That imported skill describes Zed's source revision; confirm macro arguments, environment variables, and test-support features against the app's GPUI version.
Keep domain-only tests independent of GPUI. Use the application's native verification path for visible interactions.
Finish with the checks in `STANDARDS/Stack/Desktop.md`, stating the target platform and any unverified behavior.
