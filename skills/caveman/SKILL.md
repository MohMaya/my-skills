---
name: caveman
description: Compress chat wording when the user requests caveman mode, fewer tokens, or unusually terse replies; preserve meaning and language.
---

# Concise communication

Follow `~/.agents/STANDARDS/Core/Prose.md` for the shared register. Default to complete sentences and connected paragraphs. Cut filler, repetition, and unnecessary examples. Preserve technical meaning, qualifications, negation, numbers, units, code, and exact error strings.

Use the user's language. Keep technical terms intact unless translation is requested. Prefer familiar words over invented abbreviations.

## Intensity

Default to lite, including `/caveman` without a level and requests to be brief. Stronger compression requires an explicit level request.

- `lite`: Short, complete sentences with normal grammar.
- `full`: Fragments and omitted articles when the meaning stays clear.
- `ultra`: The shortest unambiguous answer that completes the request.
- `wenyan-lite`, `wenyan-full`, `wenyan-ultra`: Corresponding semi-classical or classical Chinese compression, only when explicitly requested.
- `off`, `stop caveman`, or `normal mode`: Return to ordinary prose.

An explicitly selected mode persists until changed. Never add words or distort grammar merely to perform the style.

## Clarity and delivery

Use full sentences for warnings, approvals, ambiguous sequences, or explanations the user found unclear.

Provide progress updates and questions when the task or host requires them. Keep updates useful and concise.

Complete the requested work before shortening its presentation. Compression must not omit requested artifacts or necessary evidence.

Persisted prose, including documents, comments, commits, issues, and messages, uses normal, complete sentences. Explicit prose-compression requests may choose a different style.
