# CLAUDE.md

This is Project 9, `quality-template`, in Abdul Muizz's public engineering portfolio. It holds the shared local and CI quality gates that every later portfolio repo reuses.

Read `PORTFOLIO_BRIEF.md` in full at the start of every session. It is the master brief. If this file and the brief differ, the brief wins.

## Non-negotiable rules

1. Synthetic data only. No patient, student, staff or client data. No production code, lexicons, thresholds or prompts from any private system.
2. Permission before naming. Do not name any private company or system in any public file until Muizz confirms written permission.
3. No invented facts. Never invent a number, a date, a past result, an employer detail or a story. If a fact about Muizz is needed, stop and ask. Leave a visible `TODO(Muizz): ...`.
4. Every number is reproducible. State date, commit SHA, dataset, machine, model and version, and the exact command. Never estimate. If something was not run, say so.
5. One command to run. `make demo` or `docker compose up`, plus a seed script. A fresh clone must work on a clean machine.
6. Same gates locally and in CI. CI calls `make check` and nothing else, so the two cannot drift. Badges must be green before publishing.
7. Honest limits. The README ends with "What this does not show" and "What I would do next". Do not call demo code "production". Do not add a tool to the CV until a repo uses it.
8. Real history. Small, meaningful commits with clear messages. Never one giant commit. Record design decisions as short ADRs in `docs/adr/`.
9. Build along. Muizz must understand every line. Explain each design decision in 2 or 3 plain sentences as you make it. End with the interview drill.
10. Writing style. No em dashes in any file. Short sentences, plain words. No filler such as "seamless", "robust", "cutting-edge" or "leverage".
11. Secrets. Read keys from environment variables only. gitleaks runs in pre-commit and CI. Never print a key.
12. Spend cap. Any script that calls a paid model reads `MAX_USD_PER_RUN` and a monthly cap, stops before the cap and reports spend.

Never weaken, skip or delete a gate, test or threshold to make a check pass. If a gate looks wrong, stop and ask.

## Session protocol

One project per session.

1. Plan first (PLAN MODE). Restate the goal in 3 lines. List files, ADRs, tests, evidence and questions for Muizz. Stop and wait for the word "approved". Write no code before it.
2. Build (AUTO). Small commits. `make check` green at every commit.
3. Prove it. Run the evidence commands for real and paste actual output into results tables.
4. Close. Run the vetting checklist (plan section 6 plus the v2 items in the brief) and report pass or fail per item. Write `INTERVIEW.md`. Append a dated entry to `PROGRESS.md` in the portfolio-site repo: what was done, open items, next step.

Extra v2 vetting items: no sentence claims more than the evidence shows; `INTERVIEW.md` answered by Muizz in his own words.

## This repo

Goal: one set of gates, defined once, that any repo adopts in one command. Required targets: `make check`, `make test`, `make demo`, `make eval-smoke`. Also required: a PR template with an evidence checklist and `GATES.md` explaining why each gate exists.

Each gate must be proven by an automated test in this repo: a fake secret, a type error, a lint error, a failing test and coverage below threshold must each be blocked locally and in CI.

Pin every tool version. Add no dependency without saying why.
