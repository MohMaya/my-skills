# Source and local changes

Upstream identity is in `.skill-lock.json`; it is not a claim that local files are unmodified.

Local edits on 2026-10-18 (re-apply after `npx skills update`):
- Motion pointers name `animate-expo` (upstream's `expo-animation` carries the same content); the `expo-skill-feedback` line is removed; submitting feedback to Expo asks Shiv first.
- Expo SDK 58: `expo-router/native-tabs` is the stable import (SKILL.md, references/tabs.md, route-structure.md); `md` tab icons need `expo-symbols`; `Stack.Toolbar` works on Android from SDK 56 and needs `@expo/ui` on SDK 58 (references/toolbar-and-headers.md); zoom-transitions link points at the latest Link docs. Source: https://expo.dev/changelog/sdk-58, https://docs.expo.dev/router/migrate/sdk-57-to-58/.
