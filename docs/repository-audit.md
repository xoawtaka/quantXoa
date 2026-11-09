# Repository audit — M0

Inspected 2026-11-09 at starting SHA
`8d1a600a2b857e831560e4d552932b8d843fa90c`, clean `main`; feature branch
`feat/quantxoa-research`. No existing `AGENTS.md` was found in the repository or
checked ancestor directories. `CONTRIBUTING.md`, CI, and repository skills
provide the existing workflow. Applied `skills/qj-strategy-reviewer/SKILL.md`.

## Scope and baseline

Reviewed README, WINDOWS, pyproject, both Windows/Python launchers, the full
strategy catalog, all test-module responsibilities, local downloader/reader,
core entrypoints, execution, accounting, risk, walk-forward, and skills.
The package is 0.13.1; README also describes an older published 0.12.5 build.
The installed checkout and frozen lockfile, not the published package, define
this audit. Python 3.12.10 on Windows, project `.venv`, 94 locked packages.

Initial full suite: **252 passed, 12 failed, 11 warnings, 19.36 seconds**.
Nine failures came from an offline fixture blocking Windows asyncio's internal
loopback socket pair. Three invoked `strategy.sh` directly on Windows
(`WinError 193`). The daily sample generated a dashboard and 21 plots but
exited 1 when summary printing encountered a Unicode arrow on CP1252 stdout.

M0 fixes preserve the stream encoding and escape unsupported characters at
the isolated runner boundary; allow only socket-pair construction within the
offline fixture; and invoke the shared Python launcher in portable tests.
New tests first reproduced both failures (2 failed, 1 passed), then the full
affected test set passed (79 passed, 4 dependency warnings, 10.12 seconds).
The type gate also failed because Git converted `uv.lock` to CRLF. A new
regression reproduced the mismatch; normalizing line endings for its hash
restores the existing reviewed identity without changing dependencies or the
baseline. Final result: **269 passed, 4 warnings, 13.93 seconds**; lint,
format and source-manifest checks pass. The type gate passes with **760
reviewed diagnostics, zero changes**, not zero type errors. Full command
results are in [PROGRESS](PROGRESS.md).
Generated evidence lives in ignored `reports/m0/`; this document preserves
the durable baseline results. Synthetic returns are not research evidence.

## Discovery answers

1. **Engine capabilities.** Fast weight accounting, stateful rebalancing,
   execution-aware weight orders, explicit order callbacks, market/limit/stop/
   stop-limit/trailing/bracket/OCO orders, cancellation/expiry, participation
   partial fills, configurable commissions/slippage, contract specifications,
   cash/position/NAV ledger, static margin and exposure reporting, opt-in
   pre-trade checks, risk overlays, strategy books, metadata and local reports.
2. **Reusable strategies.** W09 is the exact hourly trend reference; O01 is a
   market-order trend pattern; O20 provides prior-window Donchian and ATR
   sizing; W07/O02 and W21 provide RSI/Bollinger patterns; W08 provides EMA;
   W17/W18 and risk modules provide volatility controls. Reuse rules and
   conventions, then validate new timing and market assumptions.
3. **Frequencies/assets.** Core accepts 1m, 2m, 5m, 15m, 30m, 90m, 1h, 1d,
   5d, 1wk, 1mo, 3mo, with aliases. **2h is rejected.** Provider availability
   remains independent of these accepted strings. Specs model equities,
   futures, FX and crypto; an option enum does not establish option lifecycle
   support. FX accounting rejects unsupported quote/settlement conversion.
4. **Local hourly futures.** Unsupported: `local_data.prepare_local_data`
   requires midnight UTC daily dates and adjusted USD equity OHLC; the SDK
   mixin also rejects granularity other than 1d and non-equity specs. The
   local Yahoo downloader hardcodes 1d. CSV/Parquet/DataFrame readers include
   validation and hashes, but have no hourly session/calendar adapter.
5. **Signal timing.** `ExecutionSimulator.run`: build bars, process pending
   fills, mark NAV, call strategy, record state. Callback orders first become
   eligible on a subsequent row, normally at its open. Open-fill slippage
   references prior completed HLCV and participation uses lagged volumes.
   This protects fill sequencing; it does not prevent a strategy reading
   future rows from its full data frames, nor define provider bar timestamps.
6. **Economics.** Orders and weight-orders apply contract multipliers and
   quantity conversion. Commission minima accumulate by order across partial
   fills. Slippage and notional fees are modeled. `round_price` exists but
   generic fills are not tick-rounded. Static margin requirements and
   configurable pre-trade/fill-time checks exist; they default to pass-through
   portfolio limits. O20 supplies no such limits and adds only a sizing cap.
7. **Futures approximations.** O20 uses provider continuous symbols, full
   notional cash accounting, reference margin, and assumed fees/slippage.
   No dated contract selection, controlled rolls, variation margin, current
   broker buying power, or exchange fee schedule. W25 is a price-return proxy
   without multiplier-based executable PnL. Neither validates MES/MNQ trading.
8. **Walk-forward.** WF01–03 default to full-run `slice_diagnostics`. A
   `backtester_factory` enables per-fold reruns; an optimizer passed to the
   runner searches only train_start through effective_is_end. Example refit
   factories rerun fixed rules; rerunning alone is not parameter fitting.
   WF04/05 search their configured period and are selection diagnostics.
   The refit strategy runs over train plus test; authors still must isolate
   learned transforms and initial position/warm-up policy.
9. **Correctness evidence.** See coverage below. Tests establish local
   software contracts, not exchange fidelity, subscription access, actual
   historical data quality, or strategy profitability.
10. **Research layer without API rewrite.** Yes: orchestration, bounded
    configuration, experiment registry, comparison and validation can wrap
    existing strategies and the standalone simulator. Intraday local
    preparation still needs an explicit additive implementation; do not
    bypass daily validation or claim the current local interface suffices.

## Strategy catalog inventory

| Family | Examples and reuse assessment |
|---|---|
| Weight trend / rotation / allocation | W01–06, W09–12: SMA, momentum, defensive rotation, inverse volatility, drift/cost/circuit controls |
| Intraday | W07 RSI 15m, W08 EMA 1m, W09 SMA 1h; O15 bracket 5m, O16 stop breakout 30m; hypotheses, not a fair performance comparison |
| Long/short relative value | W13–16 pairs and cross-sectional momentum/reversal; omitted borrow/financing |
| Portfolio risk | W17–20 volatility targeting and ERC; test lookback units and annualization for intraday use |
| Other indicator rules | W21 Bollinger, W22 MACD; reusable feature/intent patterns |
| FX / futures | W23–25 price proxies; O19 FX lots, O20 futures contracts; execution limitations above |
| Observations | W26 receipt-aware replay with provenance/freshness; useful availability pattern, not hourly bar ingestion |
| Order lifecycle | O01–14 cover market, passive/stop, trailing, brackets and OCO; O17–18 show order-based rebalance triggers |
| Validation | WF01–03 fold diagnostics/refit; WF04 grid and WF05 Optuna search |

All **51** examples remain intact (26 weights, 20 orders, 5 WF).

### Specific hourly and futures findings

| Severity for research use | Location | Finding and required treatment |
|---|---|---|
| Blocking | `backtester/sample_data.py:build_sample_bt_payload` | Always generates business-day synthetic data; no granularity input, extends short requests to at least 260 rows. An hourly example using `--sample-data` is not an hourly test. Add real interval fixtures in M2. |
| Blocking | `backtester/local_data.py` and `mixins/sdk_client.py` | Daily equity-only local gate; no authenticated hourly snapshot was supplied or found in the inspected data locations. Implement and verify M2 before performance comparisons. |
| High | W09 `_compute_weights`, `main` | SMA(10/30), SPY/QQQ/IWM, long/cash, per-name cap 25%, signal-change rebalance, fixed 2026-05-11–2026-07-11. Up to 75% target exposure before cash buffer; not equal-weight fully invested. Preserve this reference and register variants separately. No explicit cost model in main. |
| High | `core._compute_performance_weight_based` | Weights shift one row and use close-return accounting; not the same fill contract as next-open orders. Use common explicit order economics for comparison. |
| High | O20 `_compute_orders` | Breakout excludes current high/low, ATR(20) includes the completed current bar; 55-bar breakout, 0.5% ATR sizing risk, 25% per-instrument notional and 15% reference-margin caps. Rebalances target quantity and reverses on opposite breakout; ATR sizing is not a protective stop. User default 0.25% is not implemented here. |
| High | `FillEngine.submit`, `_fill_quantity` | Direct submissions lack a general duplicate-ID rejection gate. Participation takes a numeric minimum without contract-step rounding; whole-contract targets can yield fractional partial fills. Add contract-aware/idempotency tests in M6. |
| High | `walkforward/folds/purge.py` | `purge_days` counts supplied index rows. An hourly index makes it bars, not sessions. Fold dates and factory strings are day-oriented; adapt and test intraday boundaries before reuse. |
| High | `walkforward/config.py`, `folds/cpcv.py` | CPCV is unimplemented and raises. Legacy `embargo_pct` is extra pre-test purge, not post-test embargo. Top-K rank failure is not canonical PBO. |
| High | `walkforward/config.py`, result/engine | Cost-sensitivity fields exist; no cost-grid rerun loop was found. The research runner must execute stress cases rather than merely populate configuration. |
| Medium | O15 `_compute_orders` | Long RSI<30, 20% NAV share sizing, absolute brackets derived from decision close (+0.6%/-0.4%), next-row entry can gap. No session-end flatten rule. Docstring claims of a preferred cadence are hypotheses. |
| Medium | W25 `build_continuous_futures_trend` | Daily 63/252 trend and 63-bar inverse volatility, monthly rebalance, hardcoded sqrt(252); copying to hourly requires explicit sampling changes. |
| Medium | `reporting_frequency.infer_periods_per_year` | Annualization is heuristic (median bars per normalized date times 252/365). Overnight futures, partial sessions and DST need session-aware verification. |

The O20 docstring says margin is not enforced. The engine now supports
configured static margin checks; the example does not configure them. This
distinction matters: static collateral capability is not broker fidelity.

## Test coverage map

| Test modules (`tests/test_*.py`) | Evidence |
|---|---|
| `execution_architecture`, `weight_order_execution`, `p0_regressions` | Next-bar fills, prior-bar open information, lagged participation, risk rejection, costs, partial orders, ledger identities, gaps, initial costs and circuit reconciliation |
| `contract_spec_hardening`, `multi_asset_data_contract`, `fx_futures_strategies` | Metadata validation, FX currency rejection, futures negative prices, multiplier sizing and risk/notional/margin caps |
| `local_csv`, `local_download` | Invalid/duplicate/missing panels, reader equivalence and hashes, daily adjusted Yahoo inputs, no-network local replay and snapshot preservation |
| `strategy_data_contract`, `strategy_book` | Output index/schema validation, zero intent, immutable inputs, lagged allocations, sleeve accounting |
| `observations` | Receipt-time causality, missing/stale/revised observations, provenance, failure propagation and synthetic labeling |
| `walkforward_statistics` | DSR/trial counts, honest diagnostic labels, pre-OOS purge alias, factory date bounds and credential failures |
| `performance_refactors`, `portfolio_plots` | Reference parity for risk/ledger/indicator optimizations and plot layout |
| `strategy_launcher`, `strategy_runner`, `public_repo` | Imports/catalog, offline sample/report smoke, process errors, environment handling and public artifact boundaries |
| `sdk_cache_isolation`, `qj_data_cli`, `release_verifier` | Auth/tenant cache separation, metadata CLI, distribution allowlist and entrypoints |
| `mypy_baseline` (new in M0) | LF/CRLF checkout equivalence; actual lock content changes still invalidate the type context |

Not established: historical hourly snapshots, session/DST/holiday aggregation,
partial session bars, hourly-to-finer availability, arbitrary feature leakage,
dated-futures rolls and settlement, contract-step partial fills, broker margin,
daily loss latch, global idempotency, realistic borrow, or end-to-end holdout
governance. No coverage-percentage claim is made. CI tests Python 3.11–3.14
on Ubuntu; this cycle executes only Windows Python 3.12.

## Data provider assessment

The existing hosted SDK prepares provider data with credentials and product
entitlements; its public catalog describes capabilities, not guaranteed symbol
coverage. No authenticated historical request was made. The existing direct
Yahoo downloader is daily; local readers need no network. No real price
download or holdout access occurred in M0.

The [yfinance download reference](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html)
lists intraday intervals and a limited historical window; coverage must be
measured for the actual symbol/interval and pinned in the manifest. It also
documents provider-side 30m resampling, so common raw input is preferable for
controlled timeframe comparisons. Its [project documentation](https://ranaroussi.github.io/yfinance/)
describes research/personal-use expectations and points to Yahoo terms; retain
data locally and record applicable permissions. These pages were checked on
2026-11-09; no entitlement or licensing clearance is implied.

CME documents MES at $5/index point and 0.25-point ticks, and MNQ at $2/index
point with 0.25-point ticks: [MES specifications](https://www.cmegroup.com/markets/equities/sp/micro-e-mini-sandp-500.contractSpecs.html),
[CME equity futures comparison](https://www.cmegroup.com/markets/equities/sp-500-and-nasdaq-100-futures.html).
The repository's reference margin constants are not current broker quotes.
M6 needs licensed dated-contract history, dated specification/fee/margin
assumptions and roll rules. ETF research cannot substitute for that evidence.

## Research verdict

**NO STRATEGY VALIDATED.** No historical comparison was executed. Whether 1H
beats other horizons, trend beats reversion, shorts help, or finer execution
adds value is unresolved. Robustness, failure regimes, sensitivity, capacity
and paper readiness require M2–M9. Passing M0 proves a reproducible software
baseline only; [the protocol](research-methodology.md) defines the next evidence.
