# Source and local changes

Upstream identity is in `.skill-lock.json`; it is not a claim that local files are unmodified.

Local edits on 2026-10-18 (re-apply after `npx skills update`):
- The `expo-skill-feedback` line is removed; submitting feedback to Expo asks Shiv first.
- Expo SDK 58: large lists use SwiftUI `List.ForEach` or Compose `LazyColumn.Items`, which recycle rows (SKILL.md, references/swift-ui.md, references/jetpack-compose.md). Source: https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/list/, https://docs.expo.dev/versions/v58.0.0/sdk/ui/jetpack-compose/lazycolumn/.
