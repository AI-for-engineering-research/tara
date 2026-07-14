---
id: TASK-2.15
title: Add year-fallback logic for dashboard crude trade coverage
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 19:47'
updated_date: '2026-07-08 20:33'
labels:
  - dashboard
  - trade-data
  - data-fallback
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
parent_task_id: TASK-2
priority: high
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the dashboard trade pipeline so it reads Crude_TradeData_2025.xlsx first, then fills missing country import/export coverage from Crude_TradeData_2024.xlsx, then 2023, 2022, and 2021 as needed. The fallback should improve country coverage while keeping the dashboard trade maps and summaries reproducible.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Dashboard trade views use Crude_TradeData_2025.xlsx as the primary source
- [x] #2 Missing import/export country coverage is filled from 2024, then 2023, then 2022, then 2021 when available
- [x] #3 The fallback behavior is reflected in the dashboard citations or notes
- [x] #4 Tests or checks verify the dashboard still generates successfully with the fallback pipeline
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Extend the fallback year list from 2025→2021 to 2025→2014.
2. Regenerate the dashboard using the expanded fallback stack and re-audit missing import/export reporter coverage.
3. Update citation text implicitly via the fallback metadata, run the smoke test, and report the remaining missing countries.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added fallback-aware trade loading for the dashboard: imports/exports now start from `Crude_TradeData_2025.xlsx` and backfill missing reporter-country coverage from 2024, then 2023, 2022, and 2021.
- Updated the dashboard trade maps and importer/exporter summaries to use the fallback-aware datasets.
- Updated trade citations to describe the primary 2025 workbook and list any fallback years used.
- Kept the existing dashboard smoke test and extended it to assert the 2025 workbook citation is present.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_visual_dashboard.py` (1 passed) and regenerated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.

- Cleanup note: this year-fallback implementation was an intermediate step and has since been superseded by the later dashboard trade-data changes in TASK-2.16 (multi-year averaging across annual files) and TASK-2.17 (use of World totals when partner-country detail is missing).
- The task remains historically accurate as completed work, but it is no longer the current dashboard trade-data behavior.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented an intermediate year-fallback version of the dashboard trade pipeline using Crude_TradeData_2025.xlsx with earlier annual files as backfill sources. This was valid at the time, but the current dashboard has since moved beyond this approach to use multi-year averaging and World-total ranking logic (see TASK-2.16 and TASK-2.17).
<!-- SECTION:FINAL_SUMMARY:END -->
