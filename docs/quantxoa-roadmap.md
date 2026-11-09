# quantXoa milestone roadmap

Ordered acceptance gates, not delivery promises. The upstream
[ROADMAP.md](ROADMAP.md) is preserved separately. This filename avoids a
case-only collision on Windows. Current execution state is in [PROGRESS](PROGRESS.md).

| Milestone | Objective and acceptance gate | Current status |
|---|---|---|
| M0 | Audit source/tests, preserve starting SHA, create feature branch and agent workflow, reproduce sample/full suite, fix baseline blockers, publish architecture/protocol/checkpoint; local reviewable commit | COMPLETE |
| M1 | Track research source without exposing data; one validated experiment configuration/manifest schema, reproducibility IDs, bounded trial registration and research-only default; invalid/unknown configuration tests | NOT STARTED |
| M2 | Explicit intraday ETF ingestion, provenance/hash/Parquet snapshots, calendar/session/DST/partial-bar validation and deterministic 15m/30m/1h/2h construction; fixture tests and authentic sample if available | NOT STARTED |
| M3 | Preserve W09, implement exact hourly baseline plus common order-based comparator and cash/passive baseline; prefix-invariance and decision-to-fill tests; label synthetic demonstrations | NOT STARTED |
| M4 | Bounded SMA/EMA, Donchian, RSI/Bollinger alternatives; explicit stops/sizing/directions and risk safeguards; independent feature/order tests | NOT STARTED |
| M5 | Same-market/date/cost horizon and direction comparisons plus frozen hourly intent on finer execution; causal-boundary tests and matched-duration sensitivity | NOT STARTED |
| M6 | Dated MES/MNQ adapter, contract selection/rolls, multipliers/ticks/whole-contract partial fills, fee/margin/settlement ledger and idempotency; fixture failure cases before historical claims | NOT STARTED |
| M7 | Training-only fitting, rolling/expanding validation, interval purge/embargo, cost and parameter stress, uncertainty/multiple trials; freeze candidate before sealed holdout; allow no validated strategy | NOT STARTED |
| M8 | Reproducible consolidated comparisons and local HTML interface with configuration, data identity, trade/cost attribution, plots and limitations; verify artifact completeness | NOT STARTED |
| M9 | Only for a validated candidate: historical replay, paper adapter contract and readiness tests for stale/duplicate/rejected orders, disconnect, inconsistent positions, restart and emergency disable | NOT STARTED |
| M10 | Separately authorized paper brokerage integration; paper-only credentials/account verification and reconciliation before submission | BLOCKED |

M10 is blocked by absent separate authorization and preceding validation gates.
No paper or live orders are authorized by this plan.

## Dependencies and stop conditions

- M2 adapter development can proceed with fixtures. Authentic historical
  comparisons are blocked until a provenance-verified intraday snapshot with
  adequate coverage is available. A provider name is not evidence of coverage.
- M6 development can likewise use fixtures; futures profitability cannot be
  evaluated with ETF substitution or undocumented continuous-contract returns.
- Insufficient independent samples, missing fee/borrow assumptions, or invalid
  contract sizing prevents candidate promotion even if net return is positive.
- M0 intentionally fixes Windows baseline reproducibility rather than adding
  an unverified experiment platform. Each subsequent milestone gets tests,
  diff review, progress update, and an independent local commit.
