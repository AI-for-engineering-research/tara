---
id: TASK-2.4
title: Derive country crude sourcing profiles
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-08 15:18'
labels: []
dependencies:
  - TASK-2.1
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/build_country_sourcing_profiles.py
  - tests/refinery_process_model/test_build_country_sourcing_profiles.py
parent_task_id: TASK-2
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the country-level sourcing prior described in CONTEXT.md by combining domestic crude refined volumes with crude import source shares. The result should be a reusable country sourcing table for refinery-level matching.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Domestic refined volume is computed from DOMCRREF_CALC in the specified country flow workbook
- [x] #2 Country crude import source shares are derived reproducibly from TradeData.xlsx
- [x] #3 A combined country sourcing table is produced with enough detail to act as a refinery prior or plausibility modifier
- [x] #4 Weak or ambiguous sourcing signals are identified for fallback-to-technical-fit behavior
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the domestic-flow and trade workbooks plus existing normalized refinery output to define a practical country-harmonization and share-calculation approach.
2. Build a reusable country-sourcing module that computes domestic crude refined volume from `DOMCRREF_CALC`, derives crude import source shares from `TradeData.xlsx`, and harmonizes country identifiers for refinery-country use.
3. Produce reproducible CSV outputs for domestic volumes, import shares, and the combined country sourcing prior, including confidence/ambiguity flags for fallback-to-technical-fit behavior.
4. Add focused tests for filtering, aggregation, country harmonization, share logic, and output reproducibility; then run the relevant test subset and generate the artifacts.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added `refinery_process_model/build_country_sourcing_profiles.py` to compute domestic crude refined volumes from `DOMCRREF_CALC`, derive crude import source shares from `TradeData.xlsx`, harmonize country identifiers, and build combined refinery-country sourcing priors.
- Output now includes four reproducible CSVs: domestic refined volumes, import source shares, combined sourcing profiles, and country-level sourcing summaries with `confidence_flag`, `confidence_note`, and `fallback_to_technical_fit` markers.
- Trade volume estimation uses explicit basis rules (`altQty` liters/m3 when available, otherwise mass-to-barrel conversion via a documented standard kg/bbl assumption) and records coverage/ambiguity notes from W00 world-total comparisons.
- Added `tests/refinery_process_model/test_build_country_sourcing_profiles.py`; verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_country_sourcing_profiles.py` (4 passed).
- Generated outputs under `refinery_process_model/outputs/`: `country_domestic_crude_refined_v1.csv`, `country_import_source_shares_v1.csv`, `country_sourcing_profiles_v1.csv`, and `country_sourcing_summary_v1.csv`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented `refinery_process_model/build_country_sourcing_profiles.py` to compute domestic crude refined volumes from `DOMCRREF_CALC`, derive crude import source shares from `TradeData.xlsx`, and combine them into refinery-country sourcing priors with confidence/fallback flags. Added tests in `tests/refinery_process_model/test_build_country_sourcing_profiles.py`, verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_country_sourcing_profiles.py`, and generated four output CSVs under `refinery_process_model/outputs/` for domestic volumes, import shares, sourcing profiles, and sourcing summaries.
<!-- SECTION:FINAL_SUMMARY:END -->
