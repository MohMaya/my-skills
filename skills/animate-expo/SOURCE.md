# Source and local changes

Upstream identity is in `.skill-lock.json`; it is not a claim that local files are unmodified.

Local edits on 2026-10-18 (re-apply after `npx skills update`):
- Expo SDK 58: the NativeTabs import is `expo-router/native-tabs`; Gesture Handler v3 ships with SDK 58, so the Never Ship row names `usePanGesture()` and RECIPES.md says one gesture API per `GestureDetector` tree. Source: https://expo.dev/changelog/sdk-58, https://docs.swmansion.com/react-native-gesture-handler/docs/guides/upgrading-to-3.
