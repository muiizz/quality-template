# Security policy

This is a portfolio template. It holds no real data and runs no service.

## Reporting a problem

Use GitHub private vulnerability reporting on this repository: Security tab, then "Report a vulnerability".
Please do not open a public issue for a security problem. No email address is listed on purpose.

## What is covered

- A secret that slips past the gitleaks gate.
- A gate that can be bypassed without a failing check.
- A pinned dependency or action with a known advisory.

## What is not covered

This repo is not a hosted service. There is no production environment to attack.

## Supply chain

Tools are pinned by lockfile. Hooks and GitHub Actions are pinned to full commit SHAs. Dependabot
proposes updates weekly. CodeQL runs on every pull request and weekly.
