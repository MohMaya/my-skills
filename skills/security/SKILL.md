---
name: security
description: Authentication, authorization, secrets, and untrusted input. Use when adding or changing login, signup, sessions, tokens, or OAuth; when writing authorization or multi-tenant data access; when handling secrets or credentials; when accepting untrusted input (uploads, URLs, paths, HTML, shell commands, deserialization); and when reviewing a diff for security.
---

# Security

Every request moves through four states, each entered through one guard: unauthenticated, authenticated principal, authorized for this resource and tenant, effect. Every secret and every untrusted byte reaches the system through a maintained library or an explicit boundary parser.

**Dvandva.** Run `dvandva` before you produce a design, a diff, or a finding.

## Modes

| Mode | When | Steps |
| --- | --- | --- |
| **build** | Adding or changing login, sessions, tokens, OAuth, authorization, secrets, or an input path | 0–4 |
| **review** | A diff or module for security | 5 |

One owner per concern: SQL values go through `postgres` (bound parameters); status codes and error shapes through `api-design`; log and alert design through `operability`; a full audit or pen test through `security-audit`; the verdict through `bar-raiser`. The `guard-protected-paths.sh` hook already blocks agent writes to secret files.

## 0. Mandate

Name the project's auth provider. When the repository does not show one, ask Shiv which, recommending Firebase Auth. The provider and its maintained SDK own password storage, sessions, token issue, MFA, and token validation (Firebase: Admin SDK `verifyIdToken`, `revokeRefreshTokens`, `checkRevoked`). Code in this repository does not hand-roll password hashing, a session store, JWT verification, or a crypto primitive; where a primitive is unavoidable, a maintained library supplies it.

**Done when** the plan names the provider and the library that validates its tokens.

## 1. Request machine

| State | Entered when | Guard (one function, service layer) | Rejects with |
| --- | --- | --- | --- |
| Unauthenticated | A request arrives | None | None |
| Principal | The provider's library verifies the credential | `authenticate` returns a `Principal` (uid, tenant memberships, roles) parsed into a type | 401 |
| Authorized | The principal, action, and resource id pass `authorize` | `authorize` loads the resource through a tenant-scoped query, then checks the action | 403, or 404 when existence is itself secret |
| Effect | Authorized | The service mutates using only fields parsed from an explicit input schema | None |

- Guards live in the service layer, never in components or ad-hoc route code; client checks only shape the UI.
- The tenant comes from the principal's verified membership. A client-supplied tenant id is a selector, checked against that membership.
- The tenant predicate sits inside the data-access query (or an RLS policy), so another tenant's row is never fetched and then filtered.
- Every resource id from path, query, or body gets an object-level check; unguessable ids do not replace it.
- An illegal move fails closed and is logged.

**Done when** every transition on the changed path names its guard and a test that fails when that guard is removed.

## 2. Secrets

Inject each secret at runtime from a secret manager. Source, committed env files, container `ENV`/`ARG`, image layers, and client bundles hold none. A secret that reached a remote is revoked and rotated first; history rewriting with `git filter-repo` follows.

**Done when** `gitleaks` is clean on the diff and every secret the change touches has a named store, owner, and rotation path.

## 3. Untrusted input

For each sink the change adds (SQL, shell, filesystem path, outbound URL, upload, HTML, deserializer, inbound webhook, redirect target), parse the input at the boundary into a domain type, then apply that sink's rule from [references/checklist.md](references/checklist.md#untrusted-input).

**Done when** every new sink has its checklist rule applied and one hostile-input test.

## 4. Tests

Write these, each asserting the status code:

- Expired token → 401.
- Tampered token (altered payload, altered signature, `alg: none`) → 401.
- Another user's resource → 403 or 404.
- Another tenant's resource → 403 or 404.
- Role escalation (a member calls an admin action; the body sets its own `role`) → 403.

**Done when** each test fails with its guard deleted. Run that deletion once per guard.

## 5. Review

Map the diff's signals to checklist sections and walk each one yes/no:

| Diff touches | Walk |
| --- | --- |
| Login, signup, reset, password code | Identity |
| Cookies, tokens, JWT, OAuth callbacks, logout | Sessions & tokens |
| `WHERE` by id, tenant filters, roles, policies, response shapes | Authorization |
| Env files, config, keys, `.gitignore` | Secrets |
| `child_process`, `fs`, `fetch(url)`, uploads, HTML rendering, parsers, webhooks | Untrusted input |
| `Set-Cookie`, CSP, CORS, CSRF, headers | Browser |
| Log statements, error handlers | Logging |
| `.github/workflows`, lockfiles, manifests | Dependencies |

Every "no" on the changed path becomes a `bar-raiser` finding, evidence tier sourced, with severity by what the miss exposes: **critical** when it opens an authn or authz bypass, a secret, or an injection on the changed path; **major** when it removes a defence-in-depth layer (CSP, CSRF token, rate limit, dependency audit); **minor** for hardening headers and policy hygiene. A "no" outside the change's blast radius is a `bar-raiser` proposal, not a finding. Each finding cites the rule's tag and URL from the checklist's source key. A rule the diff gives no evidence for stays an open verification gap. This skill issues no verdict and no report; `bar-raiser` owns both, and its `Skills:` line names `security`.

**Done when** every touched section is walked, every in-scope "no" is a finding in the `bar-raiser` report, and every out-of-scope one is a proposal.
