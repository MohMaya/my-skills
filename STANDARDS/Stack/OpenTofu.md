# Stack/OpenTofu.md

Load for OpenTofu or Terraform-style infrastructure work.

## Toolchain

- Use the repo's chosen IaC toolchain.
- Keep provider, module, and version constraints explicit.

## Structure

- separate reusable modules from environment composition
- keep variable names boring and clear
- keep outputs intentional

## State and safety

- treat state changes as production changes
- know the backend and locking model before you edit
- do not hand-wave import, drift, or forced replacement risk

## Change discipline

- read the plan output before apply
- understand destroys and replacements
- separate refactors from behavior-changing infra edits where possible

## Security

- principle of least privilege
- avoid sprawling wildcard IAM or role grants

## Testing and verification

- use plan output as a review artifact
- verify blast radius before apply

## Anti-patterns

- modules for trivial repetition
- magic locals no one can read
- hidden provider assumptions
- unsafe replacement of stateful resources without rollout thought

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md` (here: format and validate). Additionally:
- plan output read and understood
- no accidental destroy or replacement of stateful resources
- secrets externalized
