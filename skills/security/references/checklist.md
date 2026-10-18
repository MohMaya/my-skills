# Security checklist

Yes/no rules. A "no" is a finding. Each rule ends in its verified source tag; [Source key](#source-key) maps tags to URLs. Walk only the sections the diff touches.

OWASP Top 10:2025 is the category map, not a rule source: A01 Broken Access Control → Authorization; A02 Security Misconfiguration → Browser, Secrets; A03 Software Supply Chain Failures → Dependencies; A04 Cryptographic Failures → Identity, Secrets; A05 Injection → Untrusted input; A07 Authentication Failures → Identity, Sessions & tokens; A09 Security Logging and Alerting Failures → Logging.

## Identity

- [ ] Does a maintained provider or library own password hashing, MFA, reset, and ID-token verification, with no hand-rolled primitive? `ASVS 11.2.1` `Firebase verify`
- [ ] Are stored passwords hashed with argon2id (m ≥ 19456 KiB, t ≥ 2, p = 1, or another OWASP-listed equal-strength set) through a maintained library? bcrypt only on legacy systems, cost ≥ 10, input capped at 72 bytes. `ASVS 11.4.2` `CS Password Storage`
- [ ] Is the minimum password length 15 when the password is the only factor and 8 when it is one factor of MFA, with a maximum of at least 64 and no truncation? `NIST 3.1.1.2` `ASVS 6.2.1, 6.2.8, 6.2.9`
- [ ] Are all printing ASCII, space, and Unicode accepted, with paste and password managers allowed? `NIST 3.1.1.2` `ASVS 6.2.7`
- [ ] Is every composition rule, periodic rotation rule, password hint, and security question absent? `NIST 3.1.1.2` `ASVS 6.2.5, 6.2.10, 6.4.2`
- [ ] Is each new password compared whole against a breached and common-password blocklist, rejecting with a stated reason? `NIST 3.1.1.2` `ASVS 6.2.4, 6.2.12`
- [ ] Do login, signup, and password reset return the same message, status code, and work for every outcome (unknown account, wrong password, locked account)? `CS Authentication` `ASVS 6.3.8`
- [ ] Are failed attempts throttled per account with escalating delay, never a permanent lock that lets an attacker lock a victim out, plus per-IP and global limits? Consecutive failures per authenticator stay ≤ 100. `NIST 3.2.2` `CS Authentication` `ASVS 6.1.1, 6.3.1`
- [ ] Are reset and invite tokens CSPRNG-generated, single-use, short-lived, stored hashed, and does reset leave MFA enforced? `CS Forgot Password` `ASVS 6.4.1, 6.4.3, 6.5.1`
- [ ] Is the current credential required again before changing email, phone, MFA, or password? `ASVS 7.5.1` `CS Authentication`
- [ ] Is MFA available to every account? `ASVS 6.3.3`
- [ ] Are default and shared credentials absent? `ASVS 6.3.2, 13.2.3`

## Sessions & tokens

- [ ] Is each session or reference token CSPRNG-generated with ≥ 128 bits of entropy (a UUID does not qualify)? `ASVS 7.2.3, 11.5.1`
- [ ] Is a new session token issued, and the old one destroyed, on login, re-authentication, and every privilege change? `ASVS 7.2.4` `CS Session Management`
- [ ] Does logout, expiry, or account disable end the session on the server (stateful: delete it; self-contained: deny list, per-user cutoff, or key rotation; Firebase: `revokeRefreshTokens` plus `verifyIdToken(token, true)` on sensitive routes)? `ASVS 7.4.1, 7.4.2` `Firebase sessions`
- [ ] Are idle and absolute timeouts enforced server-side? `CS Session Management` `ASVS 7.3.1, 7.3.2`
- [ ] Are access tokens short-lived (Firebase ID tokens last one hour)? `RFC 6819 §5.1.5.3` `Firebase sessions`
- [ ] Is each refresh token opaque, random with ≥ 128 bits, and stored only as its SHA-256 hash, looked up by hashing the presented value? A token with this entropy needs no slow hash; bcrypt or argon2 output cannot be looked up. `RFC 6819 §4.5.2, §5.1.4.1.3` `ASVS 6.5.2, 11.5.1`
- [ ] Does refresh rotate the token, invalidate the old one, and revoke the whole token family when a used token returns? `RFC 9700 §4.14.2` `ASVS 10.4.5`
- [ ] Do refresh tokens expire absolutely and can the user revoke them? `ASVS 10.4.8, 10.4.9`
- [ ] Does JWT verification pin the algorithm per key, reject `none`, verify the signature, take keys only from pre-configured sources (`jku`, `x5u`, `jwk` headers ignored unless allowlisted), and reject on any failed check? `RFC 8725 §3.1–3.3` `ASVS 9.1.1–9.1.3`
- [ ] Are `exp` and `nbf` checked, `iss` matched exactly, `aud` matched against this service, and the token type (`typ`, access versus ID) checked before use? `RFC 8725 §3.8, 3.9, 3.11` `ASVS 9.2.1–9.2.3`
- [ ] Are claims parsed through a schema into a domain type, with no `as` cast on the payload? `kernel`
- [ ] Is the user identified by the pair (`iss`, `sub`), never by email or any other mutable claim? `OIDC §5.7` `ASVS 10.3.3, 10.5.2`
- [ ] Are tokens kept out of URLs, with refresh tokens reachable only from the backend (BFF) and session cookies unreadable by scripts? `RFC 9700 §4.3.2` `CS Session Management` `ASVS 10.1.1, 3.3.4`

### OAuth and OIDC

- [ ] Does every authorization-code flow use PKCE with S256, and are the implicit and password grants unused? `RFC 9700 §2.1.1, 2.1.2, 2.4` `ASVS 10.4.4, 10.4.6`
- [ ] Is `state` (or PKCE) bound to the user-agent session, checked, and invalidated after first use, and is the OIDC `nonce` checked? `RFC 9700 §2.1, 4.2.4` `OIDC §3.1.3.7` `ASVS 10.1.2, 10.2.1, 10.5.1`
- [ ] Is the redirect URI compared by exact string against a pre-registered list? `RFC 9700 §4.1.3` `ASVS 10.4.1`
- [ ] Does ID-token validation match `iss` exactly and require `aud` = this client, and, with several providers, check `iss` against mix-up? `OIDC §3.1.3.7` `RFC 9700 §4.4.2` `ASVS 10.5.4, 10.2.2`
- [ ] Is an existing account linked or created from an email only when the provider reports `email_verified: true`? `OIDC §5.1, 5.7`
- [ ] Are authorization codes single-use and ≤ 10 minutes old? `RFC 9700 §4.2.4` `ASVS 10.4.2, 10.4.3`
- [ ] Are post-login redirect targets (`next`, `returnTo`) allowlisted? `RFC 9700 §4.11.1` `ASVS 3.7.2`

## Authorization

- [ ] Is every route denied by default, with the permission check running on every request in the service layer and never in client code? `CS Authorization` `ASVS 8.2.1, 8.3.1`
- [ ] Is every resource id (path, query, body, filename) authorized against the principal for the requested action, with unguessable ids treated as no substitute? `ASVS 8.2.2` `CS IDOR`
- [ ] Is the tenant derived from the principal's verified membership, with any client-supplied tenant id treated as a selector checked against that membership? `CS Multi-Tenant §1` `ASVS 8.4.1`
- [ ] Does the tenant predicate sit inside the data-access query (or an RLS policy on a role that is neither superuser nor `BYPASSRLS`, with `FORCE ROW LEVEL SECURITY`), so another tenant's row is never fetched? `CS Multi-Tenant` `ASVS 8.4.1`
- [ ] Do writes accept only fields named in an explicit input schema, and do responses return only the fields this caller may see? `CS Mass Assignment` `ASVS 8.2.3, 15.3.1, 15.3.3`
- [ ] Do admin routes check an explicit permission instead of trusting network location? `ASVS 8.4.2`
- [ ] Does a failed check fail closed and get logged? `CS Authorization` `ASVS 16.3.2`
- [ ] Do service accounts hold least privilege, and is any `iam:PassRole` scoped to named role ARNs, never `*`? `ASVS 13.2.2` `AWS PassRole`

## Secrets

- [ ] Is every secret injected at runtime from a secret manager, absent from source, committed env files, container `ENV`/`ARG`, and image layers? `ASVS 13.3.1` `CS Secrets Management`
- [ ] Do backend components authenticate with individual service accounts or short-lived tokens rather than static passwords or API keys? `ASVS 13.2.1`
- [ ] Does each secret have a named store, owner, and rotation path? `ASVS 13.1.4, 13.3.4` `CS Secrets Management`
- [ ] After a secret reached a remote, was it revoked and rotated first, with history rewritten afterwards using `git filter-repo` (forks and cached views still hold the old commit)? `GitHub sensitive data`
- [ ] Does `gitleaks` run before commit and in CI? `gitleaks`
- [ ] Are secrets and MACs compared with a constant-time function (`crypto.timingSafeEqual`, `hmac.compare_digest`, `subtle.ConstantTimeCompare`), never `===`? `ASVS 11.2.4` `Stripe webhooks` `Node crypto` `Python hmac` `Go subtle`
- [ ] Are only approved hashes (no MD5), AEAD ciphers (AES-GCM), and CSPRNG-sourced randomness in use? `ASVS 11.3.2, 11.4.1, 11.5.1`

## Untrusted input

- [ ] Is every input parsed at the boundary, server-side, against an allowlist schema covering syntax and meaning, into a domain type? `kernel` `ASVS 2.2.1, 2.2.2` `CS Input Validation`
- [ ] Do SQL statements bind every value as a parameter (rules in `postgres`)? `ASVS 1.2.4` `CS Query Parameterization`
- [ ] Do OS calls use a built-in library function, or `execFile`/`spawn` with an argument array and `shell` off, validated arguments, and `--` before operands where the tool supports it? `ASVS 1.2.5` `CS OS Command Injection` `Node child_process`
- [ ] Are stored file names generated by the server, and where a user-supplied path is unavoidable, is it resolved to its real path and confirmed inside the root with `path.relative` (no `..` prefix, not absolute), never `startsWith`? `ASVS 5.3.2` `CWE-22` (relative-versus-prefix check: derived, since `/data/up` is a string prefix of `/data/up-evil`)
- [ ] Do outbound fetches of user-influenced URLs allow only listed schemes, hosts, and ports, resolve DNS, reject private, loopback, link-local, and metadata ranges for every address, connect to the validated IP, and follow no redirects? `CS SSRF` `ASVS 1.3.6, 13.2.4, 15.3.2`
- [ ] Are uploads size-capped before processing, matched to an extension allowlist and verified by magic bytes or re-encoding, renamed randomly, stored outside the web root or on a separate host, and scanned for malware? `CS File Upload` `ASVS 5.2.1, 5.2.2, 5.3.1, 5.4.3`
- [ ] Do archives have their uncompressed size and file count checked before extraction, with symlinks and path components ignored? `ASVS 5.2.3, 5.2.5, 5.3.3`
- [ ] Are uploads served with `Content-Disposition: attachment` (or a CSP `sandbox`) and `X-Content-Type-Options: nosniff`? `ASVS 3.2.1, 5.4.1, 3.4.4`
- [ ] Is untrusted data deserialized only as schema-validated JSON, never through `pickle`, unsafe YAML loaders, or native object serialization, and are XML external entities disabled? `ASVS 1.5.1, 1.5.2` `CS Deserialization`
- [ ] Is HTML output encoded by the framework, with every escape hatch (`dangerouslySetInnerHTML`, `innerHTML`) fed only DOMPurify-sanitized HTML and `textContent` used for plain text, and are user URLs limited to `http` and `https`? `CS XSS Prevention` `ASVS 1.2.1, 1.2.2, 1.3.1, 3.2.2`
- [ ] Are inbound webhooks verified with the vendor library over the raw body, compared in constant time, bounded by a non-zero timestamp tolerance, and de-duplicated by event id? `Stripe webhooks`
- [ ] Are costly or abusable endpoints rate-limited? `ASVS 2.4.1`

## Browser

- [ ] Do session cookies set `Secure`, `HttpOnly`, `SameSite=Lax` or `Strict`, the `__Host-` prefix, and no `Domain`? `ASVS 3.3.1–3.3.4` `CS Session Management`
- [ ] Is every state-changing, cookie-authenticated request protected by the framework's CSRF defence, else a synchronizer token (stateful) or signed double-submit cookie (stateless) plus `Origin`/`Sec-Fetch-Site` verification, with `SameSite` as a second layer and GET free of side effects? `CS CSRF` `ASVS 3.5.1, 3.5.3`
- [ ] Is `csurf` absent (the repository is archived)? `csurf`
- [ ] Is `Access-Control-Allow-Origin` a fixed value or checked against an allowlist, never `*` or a reflected `Origin` on a response that carries credentials or sensitive data? `ASVS 3.4.2` `CS HTML5 Security`
- [ ] Does every response carry a CSP with `object-src 'none'`, `base-uri 'none'`, and per-response nonces or hashes for scripts (`'strict-dynamic'` optional), plus `frame-ancestors`? `ASVS 3.4.3, 3.4.6` `CS CSP`
- [ ] Is `Strict-Transport-Security` set for at least a year with subdomains, along with `X-Content-Type-Options: nosniff` and a `Referrer-Policy`? `ASVS 3.4.1, 3.4.4, 3.4.5`
- [ ] Is `X-XSS-Protection` absent or `0`? `CS HTTP Headers`
- [ ] Are third-party scripts static, versioned, and loaded with Subresource Integrity? `ASVS 3.6.1`

## Logging

- [ ] Do logs and traces exclude passwords, access tokens, refresh tokens, session ids (hash them if correlation is needed), keys, and unneeded PII? `CS Logging` `ASVS 16.2.5` (alerting and retention design: `operability`)
- [ ] Are authentication outcomes and authorization failures logged with who, what, and when, and are CR/LF neutralized against log injection? `ASVS 16.3.1, 16.3.2, 16.4.1`
- [ ] Do error responses stay generic, with no stack traces, queries, keys, or tokens, and debug modes off in production? `ASVS 16.5.1, 13.4.2`
- [ ] Do unexpected errors fail closed? `ASVS 16.5.3`

## Dependencies

- [ ] Does CI run the ecosystem audit (`npm audit`, `pip-audit`, `govulncheck`) against a documented remediation time frame? `ASVS 15.1.1, 15.2.1` `npm audit` `pip-audit` `govulncheck`
- [ ] Do installs use the lockfile from the expected registry? `ASVS 15.2.4`
- [ ] Is every third-party GitHub Action pinned to a full commit SHA taken from the action's own repository? `GitHub secure-use`
- [ ] Does the workflow default `GITHUB_TOKEN` to read-only and raise permissions per job? `GitHub secure-use`
- [ ] Are untrusted `github.event.*` values passed to `run` steps through an environment variable, and does `pull_request_target` never check out PR code? `GitHub secure-use`
- [ ] Does CI reach the cloud through OIDC with a trust condition on `sub` (and `aud`), with no long-lived cloud keys stored? `GitHub secure-use` `GitHub OIDC AWS`

## Source key

Every tag was read against the primary text on 2026-10-18. Detail per source lives in [SOURCE.md](../SOURCE.md).

| Tag | URL |
| --- | --- |
| `ASVS n.n.n` | https://github.com/OWASP/ASVS/tree/master/5.0/en (chapter files `0x10`–`0x25`; V6 Authentication, V7 Session, V8 Authorization, V9 Tokens, V10 OAuth/OIDC) |
| `NIST §` | https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ (SP 800-63B-4, final July 2025) |
| `RFC 9700` | https://www.rfc-editor.org/rfc/rfc9700.html |
| `RFC 8725` | https://www.rfc-editor.org/rfc/rfc8725.html |
| `RFC 6819` | https://www.rfc-editor.org/rfc/rfc6819.html |
| `OIDC §` | https://openid.net/specs/openid-connect-core-1_0.html |
| `CS <name>` | https://cheatsheetseries.owasp.org/cheatsheets/<Name_With_Underscores>_Cheat_Sheet.html (`CS Multi-Tenant` = `Multi_Tenant_Security`, `CS IDOR` = `Insecure_Direct_Object_Reference_Prevention`, `CS CSP` = `Content_Security_Policy`, `CS XSS Prevention` = `Cross_Site_Scripting_Prevention`, `CS CSRF` = `Cross-Site_Request_Forgery_Prevention`, `CS SSRF` = `Server_Side_Request_Forgery_Prevention`, `CS Session Management`, `CS Authentication`, `CS Authorization`, `CS Logging`, `CS Mass Assignment`, `CS Input Validation`, `CS Query Parameterization`, `CS OS Command Injection` = `OS_Command_Injection_Defense`, `CS Deserialization`, `CS File Upload`, `CS Forgot Password`, `CS Password Storage`, `CS HTML5 Security`, `CS HTTP Headers`, `CS Secrets Management`) |
| `CWE-22` | https://cwe.mitre.org/data/definitions/22.html |
| `Firebase verify` | https://firebase.google.com/docs/auth/admin/verify-id-tokens |
| `Firebase sessions` | https://firebase.google.com/docs/auth/admin/manage-sessions |
| `Node child_process` | https://nodejs.org/api/child_process.html |
| `Node crypto` | https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b |
| `Python hmac` | https://docs.python.org/3/library/hmac.html#hmac.compare_digest |
| `Go subtle` | https://pkg.go.dev/crypto/subtle#ConstantTimeCompare |
| `Stripe webhooks` | https://docs.stripe.com/webhooks |
| `GitHub sensitive data` | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository |
| `GitHub secure-use` | https://docs.github.com/en/actions/reference/security/secure-use |
| `GitHub OIDC AWS` | https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws |
| `AWS PassRole` | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html |
| `gitleaks` | https://github.com/gitleaks/gitleaks#pre-commit |
| `csurf` | https://github.com/expressjs/csurf |
| `npm audit` | https://docs.npmjs.com/cli/v10/commands/npm-audit |
| `pip-audit` | https://github.com/pypa/pip-audit |
| `govulncheck` | https://go.dev/doc/security/vuln/ |
| `kernel` | `~/.agents/AGENTS.md`, "Writing code": parse untrusted input into domain types at the boundary |
