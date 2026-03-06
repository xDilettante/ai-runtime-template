# Release Freeze Pass (2026-03-05)

## Status
- Historical note only.
- This file previously described a release pass for repository contents that are not present in the current template baseline.
- Do not use this file as current release guidance.

## Why it was downgraded
- Prior text referenced:
  - `cmd/server`
  - `/vpn/status`
  - `go test ./...`
  - `go vet ./...`
  - `Makefile`
- Those references do not match the current `ai-runtime-template` contents and created status drift against [`STATUS.md`](../STATUS.md).

## Current rule
- `STATUS.md` is the only release-state source of truth for this repository.
- Historical release notes must either match current contents or be explicitly marked archival, as done here.
