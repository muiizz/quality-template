# ADR 0002: Other repos adopt the gates by a copy script

Status: accepted, 23 Nov 2026

## Context
Later portfolio repos need the same gates. Options: a GitHub template repo, a reusable workflow,
or a script that copies the gate files.

## Decision
`scripts/adopt.sh <sha>` copies the gate files into the current repo, never overwrites without
`--force`, and writes the template commit to `.quality-template-version`.

## Why not the others
- A template repo only helps when a repo is created. Existing repos could not adopt later.
- A reusable workflow shares CI but not the local hooks, so local and CI could drift again.

## Consequences
- Each repo owns its copy, so a repo can see exactly what runs. The cost is drift.
  `make update-gates` re-copies from the template. Detecting drift automatically is not built.
- The Makefile paths assume a `python/` and `ts/` layout. An adopter edits them.
