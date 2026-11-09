# Research protocol — proposed before historical selection

Version M0, 2026-11-09. **NO STRATEGY VALIDATED.** This is the protocol to
implement and freeze in machine-readable configuration in M1–M7; it is not
an executed experiment. No historical holdout has been accessed in this cycle.
1H is a falsifiable hypothesis, not the mandated winner.

## Evidence and reproducibility

Keep synthetic correctness runs separate from historical research. Before a
historical run, require a source/retrieval manifest, raw and normalized hashes,
actual coverage, instrument/contract identity, price basis, timezone, exchange
calendar version, cleaning decisions, and data rights. Quarantine outliers
for inspection; never silently delete, forward-fill, or replace symbols.
Validate finite coherent OHLCV, duplicates, ordering, expected-session gaps,
non-trading days, splits and adjustment consistency. Negative futures prices
need asset-specific validation rather than equity positivity rules.

Every trial records exact resolved configuration, data/code/lockfile hashes,
dirty state, seed, decision/fill contract, split boundaries, parameter search
space, start/end, failures/rejections and artifacts. Count all considered
hypotheses, including failed and manually inspected alternatives. A canonical
manifest hash is the reproducibility ID. Record effective independent-trial
assumptions separately from raw trial counts.

## Market and time contract

Begin with SPY/QQQ/IWM regular-session ETF observations from a common finest
available snapshot. The initial desired base is 15m; it supports 15m/30m/1h/2h
aggregation and the first hourly-bias/finer-execution comparison. Treat any
later 5m experiment as an additional registered trial. Provider coverage may
prevent a sufficiently long study; fixtures can verify the adapter meanwhile.

Store UTC bar start/end and availability explicitly; use America/New_York for
session boundaries. Regular equity sessions normally run 09:30–16:00 Eastern,
with published holidays and early closes; pin these from the
[NYSE calendar](https://www.nyse.com/trade/hours-calendars), checked 2026-11-09.
Use a maintained, pinned exchange calendar and verify DST/early-close cases.
Futures require their own exchange-session and maintenance-break schedule.

Session-anchor aggregations at 09:30. Define intervals as [start, end), with
features available no earlier than end plus configured publication delay.
Preserve a final partial session bar with its actual duration and a partial
flag. Initial higher-timeframe entry signals require full-duration bars;
partial bars may mark positions and process existing protection. Do not
combine overnight data to complete a regular-session bar. Document overnight
holding, session-end order expiry, and final liquidation. Compare clock-anchor
alternatives only as separately counted trials.

At 10:00, the 09:30–10:30 hourly bar is unavailable. At 10:30, the completed
bar may produce intent only after its availability time. A next-bar-open fill
with zero publication/submission delay is an explicit optimistic bar-model
assumption, not a measured executable fill. Run delayed eligibility and cost
stress cases. Select the first execution opportunity whose time satisfies
submission plus delay; never fill against an earlier price. Apply identical
rules to all horizons. An hourly signal stays frozen until the next completed
hourly observation; use backward/as-of alignment with an availability bound.

Required adversarial tests: mutate future OHLC and require identical prior
features/intents/fills; reject incomplete bars and timestamps without a clear
timezone; inject missing/duplicate/out-of-order bars; test DST, holidays, early
closes and partial bars; test next-bar gaps, latency and exact-boundary
availability; show that finer decisions cannot read a forming hourly close.

## Bounded experiments

Preserve upstream examples. The following is an initial bounded proposal;
freeze exact costs, dates and configuration before observing historical
performance. Do not extend the search after a disappointing result without
registering a new research cycle and revising the testing burden.

| Experiment | Initial registered specification |
|---|---|
| A: 1H trend | SMA pairs (10,30), (5,20), (20,60); EMA pairs (10,30), (20,60); each long-only, short-only and symmetric (15 configurations). Entry after warm-up when fast/slow imply direction; exit on reversal/neutral or risk control. EMA initialization is fixed and recorded. |
| B: 1H Donchian | Prior completed high/low windows 20, 40, 55; each direction mode (9). Breakout from the completed close, excluding that bar from the channel. ATR(20) risk reference, objective protective distance 2 ATR fixed at entry; opposite breakout exits/reverses. |
| C: 1H reversion | RSI(14) thresholds 30/70 or 35/65, exit at 50; Bollinger(20) width 2 or 2.5 standard deviations, exit at midline. Three direction modes per rule (12). Fix RSI smoothing, standard-deviation convention and zero-variance behavior. |
| D: horizons | SMA(10,30), Donchian(40), RSI(14,30/70), Bollinger(20,2), each direction at 15m, 30m and 2h (36 additional); reuse their 1H runs. Native 2h support is currently absent and must pass M2/M5 acceptance. |
| E: finer execution | The same four hourly rules and three directions, frozen hourly intent executed on 15m observations (12 additional). No extra entry filter initially; measure timing, protection, turnover and costs. |
| F: baselines | No-trade cash, capped passive equal-dollar ETF basket, and long/cash close>SMA(30), each horizon (12 baselines). Include dividends/adjustments consistently and report both capital- and exposure-matched comparisons. |

Core plan: 84 signal/execution configurations plus 12 baselines. These are
planned counts, **zero historical trials executed**. Indicator periods initially
mean bars, so changing horizon also changes economic memory. Add a predeclared
matched-duration sensitivity before attributing an effect solely to horizon;
record its separate count and round rules in M5.

Optional overlays are a separate bounded tranche: on the four 1H representative
rules and three directions, test ATR scaling on versus the base sizing, and
test volatility suppression alone versus none (24 additional). Proposed
suppression threshold is the training-only 90th percentile of ATR(20)/price;
freeze it per fold. Do not cross every overlay or add regimes after inspecting
test results. ATR sizing and protective exits are distinct concepts.

Use time-shift/random controls only with a fixed protocol that preserves
exposure/holding durations and stays inside each split; predeclare seeds and
include control counts. There is no unbounded optimizer search in this plan.

## Execution, risk and transaction economics

All comparable candidates use the same order-based accounting with available
OHLCV. W09 fast-weight output is a reference, not the executable comparator.
Initially use market entries after completed signals; brackets/stops require
explicit gap handling and adverse same-bar stop/target ambiguity assumptions.
OHLC cannot identify queue position or exact intrabar path. Reject incomplete
execution data rather than substituting close for missing OHLC in research.

Candidate safeguards, to implement/test before comparisons: 0.25% equity risk
per trade using stop distance plus estimated costs; 1% session loss latch
measured from session-start equity including realized/unrealized PnL and costs;
gross exposure <=100% NAV, per instrument <=25%, and aggregate equity-index
bucket <=75% for SPY/QQQ/IWM or MES/MNQ. These are initial constraints, not
optimized parameters or current implemented defaults. Treat index products
as correlated exposure; later covariance models require their own validation.

Latch blocks new/increasing exposure, cancels entry orders, preserves risk
reduction, requests flattening at the next eligible market observation, and
verifies the ledger is flat. Missing prices may delay liquidation; report the
unresolved exposure. No doubling to recover losses. Reject nonfinite/zero
stop distance, below-minimum quantity, missing/stale data, duplicate orders,
insufficient margin and unreconciled positions. Unexpected safety failures
disable new orders until an explicit recovery condition is satisfied.

No user-specific account size or broker costs are verified. Before historical
ranking fix and disclose capital, per-side commission/minimums, exchange fees,
spread, slippage, participation/impact assumptions, borrow and financing. Run
base, doubled and tripled cost cases plus delayed fills. Zero-cost results are
diagnostics only. Do not tune size to maximize historical profits. Capital
and participation sweeps assess feasibility, not an assurance of capacity.

MES/MNQ eligibility additionally requires dated contracts, multipliers, tick
and quantity steps at order and partial-fill time, rollover before expiry,
explicit close/open roll fills and costs, dynamic dated margin assumptions,
settlement and reconciliation. A continuous series may inform features if
its adjustment/roll construction is known; executable PnL uses dated contracts.
ETFs and futures receive separate verdicts.

## Selection, validation and sealed holdout

1. Choose data by quality/coverage before examining strategy returns. Record
   session boundaries for chronological development/validation/holdout blocks.
   Proposed allocation is 60%/20%/20% of complete sessions; reject this setup
   if it cannot support adequate folds and independent observations.
2. Inside development, use rolling 12-month training / 3-month test windows,
   stepping 3 months, plus an expanding-window stability check where coverage
   permits. Fewer than four non-overlapping test folds is insufficient for
   this initial robustness protocol. Short provider windows can test software,
   not fulfill this evidence requirement.
3. Fit each fold's thresholds, scalers, sizing estimates and searched parameters
   using training only. Train-only optimization chooses settings before OOS.
   Supply warm-up observations without scoring them. Register whether folds
   restart flat or carry causal positions; initial plan restarts flat and
   charges initialization/terminal liquidation costs.
4. Purge overlapping labels/positions using their actual time intervals and
   maximum holding horizon. Define any needed post-test embargo explicitly.
   Do not feed hourly rows into the existing day-count purge unmodified.
5. Use chronological validation for one final model/rule decision. Freeze code,
   parameter selection rule, risk, cost and latency policy, acceptance criteria,
   trial ledger and artifact hashes before opening the sealed holdout.
6. Evaluate holdout once. Log access and decisions. Any selection prompted by
   holdout results contaminates it; a genuinely new period is required. An
   unsuccessful holdout yields rejection or insufficient evidence, not a
   second optimization on the same test data.

`slice_diagnostics` is descriptive only. Existing per-fold factories verify
outer date bounds but cannot detect all learned-feature leakage. DSR and
stationary-block-bootstrap Sharpe intervals are reusable diagnostics after
their sampling/trial inputs are checked. The existing 5th/95th-percentile
interval is a **90% interval**; do not relabel it as 95%. Canonical CSCV/PBO
and CPCV are not implemented. Multiple comparisons can produce apparently
good backtests; the research rationale is supported by Bailey et al.,
[The Probability of Backtest Overfitting](https://escholarship.org/uc/item/4w1110bb).

## Metrics and acceptance

Compute net round-trip PnL with partial fills/reversals allocated consistently;
define a trade as an instrument position episode from flat to flat, splitting
reversals. Report open positions separately and account for terminal liquidation.
Report total gross/net return, net expectancy, profit factor, trade count,
win rate, average win/loss, maximum drawdown, Sharpe/Sortino, return/drawdown,
exposure/leverage, turnover, commissions/slippage/borrow, and holding duration.
Zero trades or zero downside/loss require explicit undefined cases, not
infinite scores promoted as winners.

Report direction, instrument, hour/session, month/year and fold attribution;
predeclare observable trend/volatility regimes and estimate thresholds using
training only. Aggregate NAV by actual session for risk-adjusted comparisons,
with an explicit annualization convention. Show native-frequency diagnostics
separately. Trades and hourly bars are not automatically independent samples.
Estimate effective sample size with a disclosed dependence method; use seeded
session/block resampling for expectancy and paired performance differences,
with block-length sensitivity and reported confidence levels. Do not pool
overlapping OOS windows as independent evidence.

Rank by positive net OOS expectancy and uncertainty, controlled drawdown,
temporal/instrument stability, parameter-neighborhood robustness, realistic
cost/delay survival, feasible sizing/capacity and simplicity. Compare paired
net outcomes against baselines on identical sessions. Account for all trials
in multiple-testing diagnostics. Statistical significance, economic magnitude,
and practical executability are separate conclusions. No PF/Sharpe cutoff
alone validates a candidate. A positive return can still be rejected.

Final report must answer all ten requested research questions (horizon,
family, direction, finer execution, robust candidate, failure regimes,
parameter sensitivity, paper eligibility, scaling, and unfinished evidence),
with exact configuration/period/provenance/ID and actual trial counts. Include
equity/drawdown, costs/turnover, parameter and fold plots with uncertainty.
`NO STRATEGY VALIDATED` remains the verdict when evidence is insufficient.
Passing M7 only permits M9 readiness work; paper trading needs separate approval.
