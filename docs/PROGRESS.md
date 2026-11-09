# quantXoa persistent checkpoint

Updated: 2026-11-09. Project mode: **RESEARCH / BACKTEST ONLY**.
Research verdict: **NO STRATEGY VALIDATED** (no historical trials executed).

## Resume here

Read [audit](repository-audit.md), [architecture](architecture.md),
[protocol](research-methodology.md), and [milestones](quantxoa-roadmap.md).
Do not infer completion of M1–M9 from this M0 baseline. The original examples
and public engine interfaces are preserved.

## M0 — Repository audit and reproducible baseline

Status: **COMPLETE** — implementation, verification, diff review and local commit complete.

Objective: establish the actual engine/data boundaries and a reproducible
Windows baseline before implementing hourly research.

Starting Git state: clean `main`, SHA
`8d1a600a2b857e831560e4d552932b8d843fa90c`.
Working branch: `feat/quantxoa-research`.
Origin: `https://github.com/xoawtaka/quantXoa.git`.
Upstream: `https://github.com/QuantJourneyOrg/quantjourney-bt.git`.
Implementation commit: `f842a29b93837e2fb955e2ccbf97ef20fb82b2bc`
(`Establish quantXoa M0 audit and reproducible Windows baseline`).
This subsequent checkpoint records the verified implementation SHA; its own
documentation-only commit is discoverable with `git log -1 -- docs/PROGRESS.md`.
No changes were pushed or merged.

Completed work:

- Inspected requested source files, all strategy categories, test families,
  repository workflow, execution/accounting/risk, local input, and walk-forward.
- Created feature branch without discarding work; installed frozen dependencies
  in project `.venv` using Python 3.12.10 and existing `uv.lock` (unchanged).
- Reproduced baseline test and sample failures. Added failing tests, fixed
  redirected console encoding and portable test execution/network guards.
- Fixed the type gate's CRLF-sensitive lockfile hash with a failing regression;
  canonical LF identity matches the reviewed baseline. Neither `uv.lock` nor
  `quality/mypy-baseline.json` was changed.
- Documented architecture, research constraints and proposed evaluation protocol.
- Made `AGENTS.md` trackable. Preserved upstream roadmap; use
  `quantxoa-roadmap.md` because Windows cannot distinguish `ROADMAP.md` and
  `roadmap.md` as separate paths. No renames performed.

Changed files this cycle:

- `.gitignore`, `AGENTS.md`, `README.md`, `WINDOWS.md`.
- `backtester/cli/strategy_runner.py` (escape unsupported terminal characters).
- `tests/test_strategy_runner.py`, `tests/test_observations.py`,
  `tests/test_public_repo.py` (regressions and Windows portability).
- `tools/check_mypy_baseline.py`, `tests/test_mypy_baseline.py` (portable
  lockfile identity while still rejecting dependency/content changes).
- `docs/architecture.md`, `docs/repository-audit.md`,
  `docs/research-methodology.md`, `docs/quantxoa-roadmap.md`, `docs/PROGRESS.md`.
- `release/public_artifacts.txt` (explicitly include new Markdown docs in the
  existing source distribution; no runtime package expansion).

### Commands and results actually observed

All commands from repository root. Python commands use
`.\.venv\Scripts\python.exe`; outputs below `reports/m0/` are ignored.

| Command / stage | Result |
|---|---|
| `git status --short`, branch/remotes/log/HEAD | Clean start on main; SHA above |
| `git switch -c feat/quantxoa-research` | Succeeded |
| `uv sync --frozen --python 3.12 --extra dev --extra data --extra wf --extra typecheck --extra parquet` | Succeeded; 94 packages installed in isolated .venv |
| `-m pytest -q --junitxml=reports/m0/baseline-pytest.xml` | 252 passed, 12 failed, 11 warnings, 19.36s; log saved |
| `.\strategy.bat example_weights_01_sma_daily --sample-data --output reports/m0/sample` before fix | Exit 1 after report generation: CP1252 UnicodeEncodeError in summary |
| New targeted regressions before fix (`redirected_streams or offline_guard`) | 2 failed, 1 passed, 42 deselected, 1.59s; reproduced actual causes |
| Focused observation/runner/launcher/public-repo suite | 79 passed, 4 warnings, 10.12s; `focused-pytest.log/xml` |
| Intermediate full regression after runner/test fixes | 267 passed, 4 warnings, 14.06s |
| Exact sample command rerun after fix | Exit 0; `sample.log`; dashboard, metrics, equity CSV/PNG, weights, summaries, metadata, 21 plots |
| Initial `tools/check_mypy_baseline.py` | Failed: CRLF checkout hash differed from LF baseline despite identical dependencies/configuration |
| Lock identity tests before / after fix | Before: 1 failed, 1 passed (0.33s); after: 2 passed (0.23s) |
| Final `-m pytest -q --junitxml=reports/m0/final-pytest.xml` | **269 passed, 4 warnings, 13.93s**; `final-pytest.log/xml` |
| `-m ruff check .` | Passed |
| `-m ruff format --check .` | Passed: 187 files already formatted |
| `tools/check_mypy_baseline.py` after fix | Passed: **760 reviewed diagnostics, 0 changes**; `mypy.log`; not a zero-error codebase |
| `tools/verify_public_release.py` | Passed source-manifest verification (distribution build/publish not performed) |
| `git diff --check` and source diff review | Passed |
| `git diff --cached --check`, staged file review, local implementation commit | Passed; 16 intended files committed; clean tree immediately afterward |

The four remaining warnings are Seaborn's pending Matplotlib `set_bad`
deprecation in report smoke tests. No tests were skipped in the final run.
The temporary format check failure on the new type-gate line was corrected;
the final format check above passed.

Sample identity: `ExampleWeights01_DailySMATrend`, `data_source=sample`,
`granularity=1d`, configured synthetic period 2015-01-01–2025-01-01,
AAPL/MSFT/NVDA/GOOGL/AMZN, weight mode, initial capital 100000, package 0.13.1.
It contains 2610 synthetic business-day rows and is not the hourly ETF study.
Artifacts: `reports/m0/sample/ExampleWeights01_DailySMATrend/`.
No historical trial, strategy ranking, or holdout result is implied.

Frozen dependency identity (canonical LF SHA256):
`6c5d9efee322b2daf5f125ecacc17a189adf8cc236c34524aab13d40a252b669`.
Windows CRLF file-byte SHA256:
`66df4486fe85445fe9bd95816d4de6e208322944c964b3af98966c42abdc7fd7`.

### Limitations and decisions

- The shell sandbox failed before commands could start (`setup refresh had
  errors`); successful shell operations required elevated execution. No test
  result is inferred from a failed tool call.
- No existing authenticated intraday dataset was found in inspected local
  data locations. No historical prices were downloaded, selected, or scored.
- Local reader is daily USD equity-only; sample data is synthetic daily even
  when an example is configured as hourly. No hourly functionality is claimed.
- Existing futures continuous proxies, full-notional cash, generic tick/partial
  fill behavior and opt-in static margin do not establish executable futures.
- Walk-forward return slices are not OOS refits. Existing purge/date semantics
  need intraday adaptation; canonical PBO/CPCV and cost-grid execution are absent.
- Python 3.11/3.13/3.14 and non-Windows runs are not executed in this cycle.
- The type baseline retains 760 pre-existing diagnostics; passing the gate
  establishes no diagnostic changes, not full static-type cleanliness.
- No active brokerage integration, paper connection, or order submission added.

Next action after M0 acceptance: **M1**, validate one experiment specification
and reproducibility manifest, make research source trackable without exposing
data, then implement M2's session-aware adapter with fixtures. Historical
ranking waits for authenticated/provenance-verified intraday data and costs.

Approvals required: none for the next local research milestone. A paid data
subscription or new external commitment would require approval. Push/merge,
remote changes, and paper execution remain separately authorized operations.

## Remaining milestone state

M1–M9: **NOT STARTED**. M10: **BLOCKED** by missing separate paper-execution
authorization and prior validation/readiness gates. Real performance
conclusions are blocked by missing validated intraday data and unimplemented
research/evaluation layers, not by a presumed lack of strategy edge.
