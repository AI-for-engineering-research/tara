---
id: TASK-2.14
title: >-
  Upgrade dashboard trade sections to use Crude_TradeData_2024 and add
  section-level citations
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 19:36'
updated_date: '2026-07-08 19:38'
labels:
  - dashboard
  - trade-data
  - visualization
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
parent_task_id: TASK-2
priority: high
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the dashboard trade visualizations so they use refinery_process_model/excel_files/Crude_TradeData_2024.xlsx instead of TradeData.xlsx, add both import and export trade maps to the interactive dashboard, and add visible source citations to each dashboard section (UN Comtrade for trade, GlobalData for refinery data, BP/Exxon for crude assays with a note that the crude list is not exhaustive).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Dashboard trade maps are driven by Crude_TradeData_2024.xlsx rather than TradeData.xlsx
- [x] #2 The dashboard includes both an imports trade map and an exports trade map
- [x] #3 Each dashboard section shows an explicit source citation
- [x] #4 The crude section notes that the BP+Exxon crude list is not exhaustive
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect Crude_TradeData_2024.xlsx structure and adapt/reuse the existing trade-map code around its schema.
2. Add separate imports and exports trade maps to the dashboard and wire them into the generated HTML.
3. Add explicit source citations to each dashboard section, including the note that the BP+Exxon crude set is not exhaustive.
4. Update tests, regenerate the dashboard artifact, and finalize the task with verification notes.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Switched the dashboard trade-data source from `TradeData.xlsx` to `refinery_process_model/excel_files/Crude_TradeData_2024.xlsx`.
- Updated the trade-map builder to support both import and export flow directions from UN Comtrade-style workbooks, with top-2 partner routes per importer/exporter and a color-only legend by destination region.
- The dashboard trade section now shows two maps side by side: one for import routes and one for export routes.
- Added visible source citations to every dashboard section, including explicit attribution to GlobalData for refinery views, UN Comtrade for trade views, and BP/Exxon for crude assay coverage, plus a note that the BP+Exxon crude list is not exhaustive.
- Updated the smoke test to assert the presence of the source attributions and non-exhaustive crude note.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_visual_dashboard.py` (1 passed) and regenerated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated the interactive dashboard to use `Crude_TradeData_2024.xlsx` for trade analysis, added separate import and export maps, and added explicit source citations throughout the site. The crude-universe section now notes that the BP+Exxon candidate list is not exhaustive. Verified with the dashboard smoke test and regenerated the HTML artifact.
<!-- SECTION:FINAL_SUMMARY:END -->
