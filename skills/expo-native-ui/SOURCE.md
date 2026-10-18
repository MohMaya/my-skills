# Source and local changes

Upstream identity is in `.skill-lock.json`; it is not a claim that local files are unmodified.

Local edits on 2026-10-18 (re-apply after `npx skills update`):
- Motion pointers name `animate-expo`; data fetching names TanStack Query (the kernel default) instead of the uninstalled `expo-data-fetching`; the `expo-skill-feedback` line is removed; submitting feedback to Expo asks Shiv first.
- Expo SDK 58: `File.write()` is async, so references/media.md uses `writeSync`; references/icons.md notes `md` tab icons need `expo-symbols`. Source: https://expo.dev/changelog/sdk-58.
