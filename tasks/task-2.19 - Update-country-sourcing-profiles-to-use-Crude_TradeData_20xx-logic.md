---
id: TASK-2.19
title: Update country sourcing profiles to use Crude_TradeData_20xx logic
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 20:36'
updated_date: '2026-07-08 20:50'
labels:
  - sourcing
  - trade-data
  - matching
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
  - backlog/docs/validation/doc-4
parent_task_id: TASK-2
priority: high
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Change refinery_process_model/build_country_sourcing_profiles.py so the actual matcher uses the newer Crude_TradeData_20xx workbooks rather than the old TradeData.xlsx source. The sourcing-profile build should adopt the new trade-data logic consistently, regenerate sourcing outputs, and then regenerate downstream match/workbook artifacts that depend on sourcing.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 build_country_sourcing_profiles.py uses the Crude_TradeData_20xx workbook family instead of TradeData.xlsx
- [x] #2 The chosen trade-data method is implemented consistently for sourcing outputs (e.g. multi-year averaging and/or World-total handling as decided during implementation)
- [x] #3 Country sourcing outputs are regenerated and downstream refinery-crude scores, matches, and workbook are regenerated from the updated sourcing profiles
- [x] #4 Relevant tests/checks pass and documentation/notes reflect the new sourcing-trade input logic
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the existing country sourcing profile builder and its tests to identify where TradeData.xlsx is loaded and how import shares are computed.
2. Replace that trade input path/logic with the newer Crude_TradeData_20xx workflow, likely aligning the matcher with the dashboard's multi-year averaged trade approach unless the implementation reveals a better fit.
3. Regenerate sourcing outputs and downstream crude-match/workbook artifacts, run relevant tests, and update docs/notes to reflect the new trade-data source and method.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Replaced the matcher's trade input path/logic in `build_country_sourcing_profiles.py` so it now reads the `Crude_TradeData_2014.xlsx` … `Crude_TradeData_2025.xlsx` workbook family instead of `TradeData.xlsx`.
- Implemented multi-year averaged import-source logic for the matcher: annual crude import rows are normalized across the available annual files, route volumes are averaged across the available 2014–2025 years, partner-country rows drive import shares, and `W00` world totals are retained for coverage checks.
- Preserved canonical country harmonization by reusing the newer trade-country alias logic so names like USA / Rep. of Korea / Viet Nam resolve consistently in sourcing outputs.
- Kept the override mechanism active for weak/ambiguous refinery-country sourcing cases such as Oman/UAE, so the prior repair logic still applies when the newer trade inputs remain unusable for ranking.
- Regenerated `country_import_source_shares_v1.csv`, `country_sourcing_profiles_v1.csv`, `country_sourcing_summary_v1.csv`, downstream `refinery_crude_scores_v1.csv`, `refinery_crude_matches_v1.csv`, and `refinery_crude_matching_workbook_v1.xlsx`.
- Updated `data_inventory_v1.md` and `CONTEXT.md` to describe the new Crude_TradeData_20xx sourcing input logic.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_country_sourcing_profiles.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py tests/refinery_process_model/test_matching_workbook.py -q` (11 passed).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated the actual country sourcing profile builder to use the annual `Crude_TradeData_20xx.xlsx` workbooks rather than `TradeData.xlsx`. The matcher now uses a multi-year averaged import-source signal with world-total coverage checks, the sourcing outputs and downstream refinery-crude artifacts were regenerated, and the sourcing/trade documentation was updated. Verified with the relevant sourcing, matching, and workbook tests.
<!-- SECTION:FINAL_SUMMARY:END -->
