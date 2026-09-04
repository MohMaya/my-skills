# Stack/Expo.md

Load for Expo and React Native work.

## Toolchain

- Use the existing Expo and EAS setup.

## Structure and boundaries

Recommended split:
- `models/`
- `services/`
- `components/`
- `screens/`
- `hooks/`

Screens compose. Services own logic. Components present.

## Navigation and platform behavior

- keep routing clear and file-based if the repo uses Expo Router
- isolate platform-specific behavior
- do not bury navigation side effects in random components

## Data and offline behavior

- service layer owns network and storage logic
- views should not perform direct API calls
- be explicit about sync and offline tradeoffs

## Performance and accessibility

- watch list rendering
- avoid unnecessary re-renders
- handle safe areas, keyboard behavior, and touch targets correctly
- accessible labels and focus behavior are part of done

## Testing

- view tests for interaction, service tests for logic

## Anti-patterns

- hook monsters
- Redux or state machinery without real need
- platform checks spread across presentation code
- business logic in screens

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md`. Additionally:
- platform-specific behavior is contained
- list and render performance are still acceptable
- changed flows were verified on the relevant platform
