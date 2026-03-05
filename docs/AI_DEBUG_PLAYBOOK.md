# AI Debug Playbook

Structured debugging procedures for fast and reliable issue resolution.

## 1) Debugging Goals
- reproduce reliably,
- isolate root cause,
- implement minimal fix,
- verify no regression.

## 2) Reproduction Ladder
1. exact command/path
2. environment snapshot
3. deterministic input
4. expected vs actual output
5. repeatability check

## 3) Isolation Ladder
1. narrow module boundary
2. identify failing condition
3. trace data flow
4. test hypothesis
5. confirm root cause

## 4) Hypothesis Logging
For each hypothesis capture:
- statement,
- evidence for,
- evidence against,
- next probe.

## 5) Fast Triage Map
- crash at startup -> config/bootstrap boundaries
- intermittent failures -> timing/state/race boundaries
- wrong output -> transformation/contract boundaries
- performance drop -> hot path + allocations + I/O

## 6) Probe Patterns
- input probe
- state probe
- branch probe
- output probe
- timing probe

## 7) Common Root Cause Buckets
- contract mismatch
- stale assumptions
- boundary validation gaps
- concurrency order issues
- environment drift

## 8) Fix Patterns
- add missing validation
- align contract mapping
- move side effects to boundaries
- enforce deterministic sequencing
- add explicit error context

## 9) Regression Shielding
- add focused regression test
- rerun known failing path
- rerun adjacent path for collateral risk

## 10) Debug Evidence Packet
- repro command
- key output excerpts
- root cause statement
- fix summary
- validation summary

## 11) Flake Strategy
- repeat targeted runs
- detect shared mutable state
- eliminate arbitrary sleeps
- use condition-based waits

## 12) Config/Env Strategy
- print effective config (non-sensitive)
- compare expected vs actual runtime config
- isolate environment-specific branches

## 13) External Dependency Strategy
- isolate with stubs/mocks where feasible
- classify retryable vs terminal external errors
- protect boundary with clear diagnostics

## 14) Debug Exit Criteria
- issue reproduced,
- root cause identified,
- fix validated,
- no new regression observed,
- evidence documented.

## 15) Post-Fix Note Template
- symptom
- root cause
- fix
- tests/checks
- follow-up
