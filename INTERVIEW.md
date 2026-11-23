# Interview questions for quality-template

The 12 hardest questions a reviewer could ask about this repo. The notes under each question come from the repo. Write your own answer under each one, in your own words. Answers are left empty on purpose.

## 1. Why does CI call only `make check`, and what breaks if someone adds a CI-only step?

Repo notes: Local and CI can disagree. A CI-only step is a check nobody can run before pushing. See ADR 0001.

My answer:

## 2. How do you prove a gate blocks a fault, rather than assume it?

Repo notes: `python/proofs/test_gates.py` copies the repo, injects one fault, runs `make check-core`, asserts failure and the right gate name. A clean copy must pass.

My answer:

## 3. What can a contributor do to bypass these gates, and what stops them?

Repo notes: `--no-verify` skips hooks. They could edit the Makefile or lower a threshold. CI runs `make check` on the PR. Branch protection forces it on `main`; see the README results for the proof.

My answer:

## 4. Why is a coverage threshold a weak signal, and what do you use as well?

Repo notes: Coverage shows code ran, not that a test would notice a change. The mutation score on the core module covers that gap.

My answer:

## 5. What does mutation testing tell you that coverage does not, and what does it cost?

Repo notes: It changes the code and checks a test fails. Cost is run time. Here it is a few seconds because the core is 20 lines.

My answer:

## 6. How do you handle equivalent mutants?

Repo notes: In this repo all 40 mutants were killed, so none needed a decision. Your answer: what you would do if one survived and was equivalent.

My answer:

## 7. Why pin hooks and Actions to commit SHAs, and what does it cost?

Repo notes: A tag can be moved. A SHA cannot. Cost: Dependabot PRs to update them.

My answer:

## 8. What does gitleaks miss?

Repo notes: Secrets with no known pattern, encoded or split strings, and anything in a file the config allowlists. It runs on the working tree and on git history.

My answer:

## 9. Why a copy script, not a template repo or a reusable workflow?

Repo notes: See ADR 0002. A template repo only works at creation. A reusable workflow does not share local hooks.

My answer:

## 10. How do two repos drift after adoption, and how do you find out?

Repo notes: Each repo owns its copy. `.quality-template-version` records the source commit. Automatic drift detection is not built.

My answer:

## 11. Which gates are slow, and how do you keep `make check` short?

Repo notes: The proofs are the slowest because each runs the gates on a repo copy. See the Results table for the measured time.

My answer:

## 12. What would you change for a team of 20 instead of one person?

Repo notes: Points to consider: required reviews, branch protection, shared caches, signed commits.

My answer:
