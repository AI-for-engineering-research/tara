---
id: TASK-2.17
title: >-
  Use World totals in dashboard importer/exporter rankings when partner detail
  is missing
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 20:07'
updated_date: '2026-07-08 20:09'
labels:
  - dashboard
  - trade-data
  - world-totals
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
parent_task_id: TASK-2
priority: high
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the dashboard importer/exporter summary views so countries can still appear in the top-volume rankings when only World total rows are available. Use World rows to rank total importer/exporter volume, use country-specific partner rows only when available for stacked source/destination splits, and show a single fallback bar when only World totals exist and destination/source breakdown is unavailable.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Top importer/exporter ranking uses World total rows when country-specific partner detail is missing
- [x] #2 Country-specific partner rows are still used for stacked breakdowns when available
- [x] #3 Countries with only World total rows appear with a single bar labeled that destination/source breakdown is unavailable
- [x] #4 Dashboard still generates successfully and tests/checks pass
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Load averaged trade rows in a way that preserves both World-total rows and country-specific partner rows.
2. Rework the importer/exporter breakdown builders so ranking uses World totals when present, while stacked partner bars still use country-level partners when available.
3. For reporters with only World totals and no country partner detail, emit a single fallback segment labeled that breakdown is unavailable.
4. Update tests if needed, regenerate the dashboard, and verify Saudi Arabia / similar cases can appear in the exporter rankings.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Updated the averaged trade-row loader to preserve `World` total rows while still filtering them out of the route maps.
- Reworked the importer/exporter breakdown charts so ranking uses `World` totals when present, while stacked country-partner segments use country-specific rows only.
- Added a fallback segment label `World total only / breakdown unavailable` for reporters such as Saudi Arabia that have total export volume but no country-destination detail.
- Verified that Saudi Arabia now appears in the exporter ranking with a fallback single bar, while countries with real partner detail still show stacked breakdowns.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_visual_dashboard.py` (1 passed) and regenerated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated the dashboard importer/exporter summary logic to rank countries using World total rows when partner-country detail is missing, while preserving stacked country-partner breakdowns when available. Countries like Saudi Arabia now appear with a single fallback bar labeled that destination/source breakdown is unavailable. Verified with the dashboard smoke test and regenerated the HTML artifact.
<!-- SECTION:FINAL_SUMMARY:END -->
