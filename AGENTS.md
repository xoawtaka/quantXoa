# quantXoa agent workflow

## Scope and progression

- Read `docs/PROGRESS.md`, `docs/repository-audit.md`, and
  `docs/research-methodology.md` before research work. Follow
  `docs/quantxoa-roadmap.md`, one verified milestone at a time.
- Keep the upstream `backtester` package, public interfaces, and examples.
  Project display name is quantXoa. Add project modules only when needed.
- Research/backtesting is the default. Synthetic runs verify software only.
  `NO STRATEGY VALIDATED` is an acceptable research conclusion.
- Paper account connection/order submission requires separate explicit user
  authorization. Do not create an active live-order path or submit real orders.

## Repository safety

- Start with `git status --short`, current branch, remotes, and starting SHA.
  Preserve user changes. Work on a feature branch; do not reset or clean them.
- Local edits and reviewable commits are authorized. Do not push, merge,
  rewrite history, force-push, delete branches, rename remote repositories,
  change visibility, or alter accounts without explicit authorization.
- Never print credentials or commit `.env`, downloaded data, or generated reports.
  Keep outputs in ignored `reports/` and input snapshots in ignored `data/`.
- Search references before renaming; use `git mv`, update references, test the
  affected interfaces, and explain the reason. Avoid case-only path collisions
  on Windows. `docs/ROADMAP.md` is the upstream roadmap.

## Implementation and verification

- Use Python 3.11+ and the repository `.venv`; prefer the reviewed `uv.lock`:
  `uv sync --frozen --python 3.12 --extra dev --extra data --extra wf --extra typecheck --extra parquet`.
- Keep functions focused, type public interfaces, use explicit configuration,
  deterministic seeds, and fail closed on invalid data. Follow the repository
  Ruff configuration and applicable `skills/` guidance.
- For meaningful behavior changes, add a failing regression first, implement,
  then run focused tests and practical full regression checks. Do not weaken
  assertions to hide failures. Report commands actually executed.
- Required checks from the root, using `.venv/Scripts/python.exe` on Windows:
  `-m pytest -q`, `-m ruff check .`, `-m ruff format --check .`,
  `tools/check_mypy_baseline.py`, and `tools/verify_public_release.py`.
  Do not adjust the mypy baseline just to pass. New packaged documentation or
  sources must be explicitly listed in `release/public_artifacts.txt`.
- Use `.\strategy.bat ...` on Windows. Launcher integration tests should use
  `sys.executable` and `strategy.py`; do not require a Unix shell.
- Inspect `git diff --check`, the diff, and status before a local commit.
  Commit only an independently reviewable cycle with passing relevant checks.

## Research contract and handoff

- Separate bar start, bar close, availability, decision, submission, and fill
  timestamps. Signals may use only observations available at decision time.
- Never relabel continuous futures proxies as dated executable contracts, or
  full-history return slices as per-fold out-of-sample evaluation.
- Record data provenance, checksums, exact configuration, costs, seeds, code
  SHA, trials including failures, and holdout access. Do not infer profitability
  from passing software tests or bundled sample data.
- After each cycle update `docs/PROGRESS.md`: status, objective, changed files,
  actual tests/results, limitations, decisions, next action, commit reference,
  and approvals needed. Use NOT STARTED / IN PROGRESS / BLOCKED / COMPLETE /
  REJECTED. Leave incomplete acceptance criteria visibly incomplete.
