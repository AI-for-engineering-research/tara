---
id: TASK-2.16
title: Average dashboard crude trade data across annual files
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 20:02'
updated_date: '2026-07-08 20:04'
labels:
  - dashboard
  - trade-data
  - averaging
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
parent_task_id: TASK-2
priority: high
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the current year-priority fallback logic in the dashboard trade views with an average across the available annual crude trade workbooks from 2014 onward. For each trade flow, average across the years that exist and ignore missing years. If no 2026 workbook exists, use the available 2014-2025 files.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Dashboard trade maps and summaries are built from averaged annual crude trade data rather than year-priority fallback selection
- [x] #2 The averaging logic uses all available Crude_TradeData_2014-2025 workbooks and ignores missing years
- [x] #3 Dashboard trade citations/notes explain that the trade views are averaged across available years
- [x] #4 Tests or checks verify the dashboard still generates successfully with the averaging pipeline
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Replace the fallback loader with an averaging loader that reads all available Crude_TradeData_2014-2025 workbooks, standardizes country aliases, and averages trade values across available years by route.
2. Feed the averaged trade dataset into the import/export maps and importer/exporter summaries.
3. Update dashboard citation text to explain that the trade views are multi-year averages across available annual files (2014-2025; no 2026 file present).
4. Run the dashboard smoke test, regenerate the HTML artifact, and report any remaining caveats.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Replaced year-priority fallback selection with multi-year averaging across all available `Crude_TradeData_2014.xlsx` through `Crude_TradeData_2025.xlsx` files.
- For each import/export route, the dashboard now averages `primaryValue` across the years where that route exists; missing years are ignored rather than backfilled sequentially.
- Updated the trade citation text to explain that the trade views are multi-year averages across available annual files and to note that no 2026 workbook is currently present in the repo.
- Regenerated the dashboard and re-audited missing reporter coverage after averaging; remaining missing countries are unchanged from the alias-normalized coverage audit because averaging does not create coverage where no annual rows exist.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_visual_dashboard.py` (1 passed) and regenerated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated the dashboard trade pipeline to use averaged annual crude trade data across the available 2014-2025 UN Comtrade workbooks, ignoring missing years instead of using year-priority fallback. The dashboard citations now explain the averaging approach and note the absence of a 2026 workbook. Verified with the dashboard smoke test and regenerated the HTML artifact.
<!-- SECTION:FINAL_SUMMARY:END -->
