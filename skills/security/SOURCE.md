# Sources

Written for this repository on 2026-10-18. Rules are rewritten, not copied; each was read against the primary text on that date. Upstream skills were imported in commit `40c5f7c` and are consolidated here:

- [wshobson/agents](https://github.com/wshobson/agents) `plugins/developer-essentials/skills/auth-implementation-patterns` (no license file or frontmatter license on disk): the authn/authz split, refresh-token flow, and RBAC/ownership checks, with the bcrypt-hash refresh lookup, redirect-query tokens, unlinked-email account linking, missing session regeneration, and `as`-cast JWT claims corrected.
- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) `secure-code-guardian`, `security-reviewer`, `fullstack-guardian`, `test-master` (MIT, per frontmatter): the validation checkpoints, per-feature checklist, secret-scanning step, and the security test set. Corrected: composition rules, the 2017 OWASP list, `csurf`, `X-XSS-Protection: 1`, `startsWith` path checks, hostname-only SSRF allowlists, lockout by email, `!==` token compare, trufflehog via pip, `git filter-branch`.
- AWS agent skills `aws-auth` and `aws-iam` (no license on disk, not in `.skill-lock.json`): the point that locally verified JWTs outlive revocation until `exp`, the full-teardown lesson, least-privilege `iam:PassRole`, and OIDC CI roles with a `sub` condition.

## Verification

| Rule family | Primary source |
| --- | --- |
| Category map | [OWASP Top 10:2025](https://top10.owasp.org/2025) (published; the landing page shows no release date) |
| Password length 15 / 8 with MFA, max ≥ 64, no composition or rotation, blocklist, no truncation or hints; 100-failure cap | [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/) §3.1.1.2, §3.2.2 (final, July 2025) |
| argon2id m=19456 KiB, t=2, p=1; bcrypt cost ≥ 10 and 72-byte cap | [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) |
| Generic responses and timing; per-account throttling; lockout as denial of service; re-authentication | [OWASP Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html); ASVS 6.1.1, 6.3.1, 6.3.8, 7.5.1 |
| Session regeneration, server-side invalidation, cookie attributes, timeouts, no ids in URLs | [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html); ASVS 7.2.3, 7.2.4, 7.3.x, 7.4.x, 3.3.x |
| Token entropy 128 bits (ASVS overrides the cheat sheet's 64) | ASVS 7.2.3, 11.5.1 |
| Refresh tokens stored as hashes; SHA-256 suffices at ≥ 128 bits | [RFC 6819](https://www.rfc-editor.org/rfc/rfc6819.html) §4.5.2, §5.1.4.1.3; ASVS 6.5.2 (standard hash acceptable at ≥ 112 bits), 11.5.1 |
| Refresh rotation with replay detection; PKCE; exact redirect URI; no implicit or password grant; `state`; mix-up; no tokens in query strings; open redirectors | [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) §2.1, 2.1.1, 2.1.2, 2.4, 4.1.3, 4.2.4, 4.3.2, 4.4.2, 4.11.1, 4.14.2; ASVS 10.x |
| JWT algorithm pinning, `none`, key source, `iss`/`aud`/`exp`/`typ` | [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html) §3.1–3.3, 3.8, 3.9, 3.11; ASVS 9.1.x, 9.2.x |
| Identify users by (`iss`, `sub`); `email_verified` | [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) §3.1.3.7, §5.1, §5.7; ASVS 10.3.3, 10.5.2 |
| Firebase token verification, revocation, one-hour ID tokens | [verify-id-tokens](https://firebase.google.com/docs/auth/admin/verify-id-tokens), [manage-sessions](https://firebase.google.com/docs/auth/admin/manage-sessions) |
| Object-level, field-level, and tenant authorization; service-layer enforcement | ASVS 8.2.x, 8.3.1, 8.4.x; [Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [IDOR](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html), [Multi-Tenant](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html), [Mass Assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html) |
| Tenant predicate inside the query rather than after fetch | Derived from the Multi-Tenant sheet's query and RLS examples; no source states the after-fetch case |
| Secrets in a manager, rotation, no Docker `ENV`/`ARG` | ASVS 13.1.4, 13.3.x; [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) |
| Rotate before history rewrite; `git filter-repo` | [GitHub: removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) |
| Constant-time compare | ASVS 11.2.4; [Stripe webhooks](https://docs.stripe.com/webhooks); [Node](https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b), [Python](https://docs.python.org/3/library/hmac.html#hmac.compare_digest), [Go](https://pkg.go.dev/crypto/subtle#ConstantTimeCompare) |
| Command execution without a shell | ASVS 1.2.5; [OS Command Injection Defense](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html); [Node child_process](https://nodejs.org/api/child_process.html) (`shell` defaults to `false`) |
| Path confinement | ASVS 5.3.2; [CWE-22](https://cwe.mitre.org/data/definitions/22.html) (canonicalize with `realpath`). The `path.relative` check in place of `startsWith` is derived: `/data/up` is a string prefix of `/data/up-evil` |
| SSRF | [SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html); ASVS 1.3.6, 13.2.4, 15.3.2 |
| Uploads; `Content-Disposition` and `nosniff` | [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) (silent on serving headers); ASVS 5.2.x, 5.3.x, 5.4.x, 3.2.1, 3.4.4 |
| Deserialization; XSS encoding and sanitizing | ASVS 1.2.x, 1.3.1, 1.5.x; [Deserialization](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html), [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) |
| CSRF; `csurf` archived | [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) (SameSite is defence in depth; silent on `csurf`); [expressjs/csurf README](https://github.com/expressjs/csurf) |
| CORS, CSP, security headers, `X-XSS-Protection` absent or `0` | ASVS 3.4.x; [HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html), [CSP](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html), [HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html) |
| Logging exclusions, log injection, generic errors | [Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html); ASVS 16.2.5, 16.3.x, 16.4.1, 16.5.x |
| Webhook verification | [Stripe webhooks](https://docs.stripe.com/webhooks) (raw body, constant-time compare, non-zero tolerance, event-id de-duplication) |
| Dependency audit, secret scanning | ASVS 15.1.1, 15.2.x; [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit), [pip-audit](https://github.com/pypa/pip-audit), [govulncheck](https://go.dev/doc/security/vuln/), [gitleaks](https://github.com/gitleaks/gitleaks#pre-commit) |
| Actions pinned to a commit SHA, read-only `GITHUB_TOKEN`, no interpolated event context, no `pull_request_target` checkout, OIDC | [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use); [OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) (`sub` condition) |
| `iam:PassRole` scoped to named roles | [AWS IAM: PassRole](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html) |

ASVS is [ASVS 5.0](https://github.com/OWASP/ASVS/tree/master/5.0/en); requirement numbers cite that edition.

## Left out

The upstream skills' penetration-testing, SAST-tooling, compliance-framework (SOC2, ISO27001), CVSS, and report-template material: out of scope for build-time guidance, and `bar-raiser` owns the report. Cognito-specific mechanics (`update-user-pool-client` full-replace semantics, Lambda triggers, managed-login branding): they belong to a Cognito task, and the project's provider is Firebase by default. IAM edge cases beyond `iam:PassRole`. Rules not read against a primary source: Vite `VITE_*` variables reaching client bundles, and the `trufflehog` install route.
