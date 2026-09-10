# Workflow/Delivery.md

Load for CI/CD, runtime safety, observability, rollback, feature flags, and delivery gates.

## Pipeline baseline

Every production path should have these stages:

1. format or lint
2. static checks or type checks
3. tests
4. security scan
5. build
6. deploy gate

Failing quality gates block merge or deploy.

## Pre-commit minimum

Run repository-required checks and the checks relevant to the changed behavior before committing. Use the existing lint, type, test, or smoke checks as applicable. Stack files supply domain-specific requirements. A prose-only edit needs no unrelated application build unless CI requires it.

## Security review skills

Use `commit-security-scan` for a scoped diff, `threat-model-generation` for trust boundaries, and `vulnerability-validation` to investigate a concrete finding. `security-review` combines these workflows when a broader review is requested. Reuse the repository's canonical threat model. Assess attacker access, data flow, and deployed controls from evidence; a file type, UUID, CLI, or environment-variable source alone establishes neither safety nor exploitability.

Keep findings in the requested review surface. Creating threat-model files, posting comments or issues, committing generated artifacts, and running exploit demonstrations follow the authorized task scope. Confirm the target environment and permitted effects before an active exploit test. Keep credentials and captured sensitive data out of reports.

## Observability baseline

### Logging

- structured logs
- consistent levels
- request or trace identifiers
- operation name and duration where it matters
- never log secrets or PII

### Metrics

Minimum runtime metrics:
- request count
- error count
- latency distribution
- resource saturation

### Error tracking

Unhandled exceptions should land in a central error tracker with enough context to debug the failure.

## Rollback policy

Use the project's rollback runbook and authorized incident response scope. Before deployment, establish thresholds from its service objectives and baseline. Error spikes, latency regressions, critical failures, and threatened data integrity require immediate assessment. Execute rollback when the runbook or user authorizes it; otherwise surface the evidence and proposed action.

Rules:
- rollback should be one command or one obvious platform action
- schema changes must be backward-compatible with the previous app version
- do not treat destructive migration rollback as routine

## Feature flags

Use flags for:
- risky rollouts
- incomplete but mergeable work
- percentage or allowlist rollouts

Rules:
- every flag has an owner
- every flag has an expiry date
- cleanup is tracked work
- flag checks live in service or application logic, not presentation

## Caching

Cache only when the consistency tradeoff is acceptable.

Rules:
- choose invalidation and expiry from the data's consistency requirements; document the tolerated staleness
- safe cache-miss behavior
- cache logic lives in service or data layers, with one named owner per cache

## ADR linkage

If delivery or rollout constraints force a durable change in architecture, ADR triggers are in `Core/Planning.md` and the template is in `Core/Documents.md`.
