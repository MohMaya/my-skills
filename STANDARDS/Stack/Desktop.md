# Stack/Desktop.md

Load before selecting a desktop stack or planning, building, or reviewing GPUI behavior.

## Stack policy

Use Rust + GPUI for every new desktop application, including a desktop companion to an existing web or mobile product.
Cargo owns the Rust build and dependencies. GPUI owns windows, UI state, layout, input, and GPU rendering.
Use the platform backends supported by the selected GPUI release; application code normally needs no direct graphics API dependency.

An alternative stack, including Electron, Tauri, or Wails, requires Shiv's explicit direction or approval of a concrete constraint.
When GPUI cannot meet a requirement, describe the missing capability and its effect before proposing an exception.
Maintain existing desktop applications in their current stack until Shiv authorizes a migration.

GPUI produces native binaries with custom GPU-rendered controls. Native OS widgets, accessibility, and platform integration require separate verification.

## Skills and design

Read [Rust.md](Rust.md) before writing Rust. Use `codebase-design` and `shiv-code-gate` for module design and the Structure Note.
The kernel's design authority still applies. Follow the approved design and name missing states before implementation.
Load `gpui` for native component implementation and `gpui-test` for GPUI tests and scheduler failures.
Use native inspection for GPUI reviews; apply `pe-review` design principles only where they fit, without its browser-only procedure.

Keep domain logic independent of GPUI contexts and view entities. Let views translate user actions into domain operations.
Separate persistence, networking, and platform calls at boundaries that can hold behavioral tests.
Start with modules; split crates when ownership or reuse justifies the boundary.

## Version and runtime discipline

Pin a compatible GPUI release or Git revision and commit the application lockfile.
Check examples and API documentation against that version before copying them. GPUI remains pre-1.0 and upstream examples can drift.
Choose component dependencies against the approved design and their compatibility with the pinned GPUI version.
Read each dependency's license; permission to use GPUI does not establish permission to copy every Zed crate.

## Verification and delivery

Run the Rust checks in [Rust.md](Rust.md), plus behavioral tests at the changed domain and GPUI boundaries.
Exercise the real native application with an available native automation tool or a repo-local driver.
Browser checks alone do not verify a native desktop binary. Use `create-verification-skill` when reproducible native driving is missing.

Check the changed flow's loading, empty, error, and success states, keyboard focus, shortcuts, text input, and window resizing.
Check accessibility roles, labels, actions, and screen-reader behavior on the target platform for changed controls.
Verify relevant clipboard, menus, file dialogs, multiple windows, and shutdown behavior when the feature uses them.
Establish cold-start, idle memory/CPU, and interaction-latency baselines for new apps using a representative workload.
Remeasure affected metrics for performance-sensitive changes, regressions, or release verification; reuse valid evidence for narrow edits.

Before shipping, verify packaging, signing, installation, and any update flow on each claimed target platform.
Report untested targets and blocked checks explicitly. The kernel's production instrumentation and launch requirements remain in force.

## Primary references

- [GPUI framework and examples](https://gpui.rs/).
- [GPUI README and platform setup](https://github.com/zed-industries/zed/blob/main/crates/gpui/README.md).
- [GPUI API documentation](https://docs.rs/gpui).

Resolve these references to the project's pinned version before relying on version-sensitive details.
