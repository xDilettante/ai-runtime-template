# AI Check Matrix

A matrix of recommended checks by change type and risk profile.

## 1) Change Type vs Required Checks
### Bugfix (low risk)
- run targeted unit tests
- run lint/static checks for touched package
- verify reproduction no longer fails

### Bugfix (medium risk)
- all low-risk checks
- run adjacent package tests
- run at least one integration path if affected

### Bugfix (high risk)
- all medium-risk checks
- run broader suite for impacted domain
- add rollback note and residual risk summary

### Feature (low risk)
- feature-specific tests
- docs update for usage impact
- lint/static checks

### Feature (medium risk)
- all low-risk checks
- boundary interaction tests
- compatibility note

### Feature (high risk)
- all medium-risk checks
- migration/compatibility validation
- release-readiness summary

### Refactor (behavior-preserving)
- regression suite for touched behavior
- static checks
- clear no-behavior-change statement

### Build/CI change
- run altered pipeline steps locally if possible
- verify deterministic behavior
- document changed assumptions

## 2) Check Depth Policy
- low risk: focused checks only
- medium risk: focused + adjacent checks
- high risk: focused + adjacent + broad checks

## 3) Failure Handling Matrix
### Check fails with clear root cause
- fix and rerun only affected checks first

### Check fails with ambiguous cause
- isolate failing boundary
- add probe logs/tests
- rerun focused checks

### Check fails intermittently
- run stability repeats
- inspect timing/state assumptions
- avoid sleep-based masking

## 4) Evidence Matrix
For each check capture:
- command
- outcome
- key output line(s)
- interpretation

## 5) Risk Matrix for Common Changes
### API contract change
- risk: high
- required: compatibility review, migration note, contract tests

### Config default change
- risk: medium/high
- required: startup behavior verification, docs update

### Parsing/validation change
- risk: medium
- required: boundary tests with invalid/edge inputs

### Concurrency change
- risk: high
- required: race/stability checks and deterministic assertions

### Logging-only change
- risk: low/medium
- required: lint/build; verify no secret leakage

## 6) Docs Matrix
### Behavior changed
- update user-facing docs

### Runtime command changed
- update README/how-to

### Config key changed
- update reference docs and examples

### Workflow changed
- update STATUS/DEVLOG and SUMMARY where applicable

## 7) Delivery Matrix
### success
- include full evidence packet

### partial
- include completed scope + blocked scope + next unblock action

### blocked
- include blocker proof + options + recommendation

## 8) Merge Matrix (Multi-agent)
- verify ownership of each step output
- deduplicate overlapping claims
- resolve contradictions with reruns
- keep only evidence-backed statements

## 9) Practical Thresholds
- if no checks run, result cannot be full success for non-trivial change
- if high-risk path changed, broad validation is expected
- if assumptions are critical, mark them explicitly in final report

## 10) Minimal Check Sets by Task Class
### Documentation-only
- link/format sanity

### Small internal logic fix
- targeted tests + lint

### Cross-module behavior change
- targeted + adjacent tests + docs update

### Infrastructure/runtime behavior change
- targeted + broad checks + operator note

## 11) Operator-Facing Output Matrix
- Always provide:
  - what changed,
  - what passed,
  - what was not run,
  - why,
  - what to do next.

## 12) Escalation Matrix
Escalate when:
- validation cannot be completed due missing capability,
- risk too high for current evidence,
- conflicting acceptance criteria,
- architectural choice required.

Escalation output:
- blocker
- evidence
- options
- recommended option
