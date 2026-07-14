---
id: TASK-2.18
title: Add global crude production section to dashboard from INDPROD
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 20:18'
updated_date: '2026-07-08 20:20'
labels:
  - dashboard
  - production-data
  - visualization
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
parent_task_id: TASK-2
priority: high
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a new dashboard section below the crude candidate universe and before crude trade dynamics that shows the worldwide crude production breakdown using the INDPROD signal from crude_oil_country_flows_2025_domestic_crude_refined_calc.xlsx. The section should make it easy to see which countries produce the most crude and cite the source clearly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Dashboard includes a new crude production section placed below crude candidate universe and above crude trade dynamics
- [x] #2 The section is built from the INDPROD signal in crude_oil_country_flows_2025_domestic_crude_refined_calc.xlsx
- [x] #3 The new section includes a visible source citation
- [x] #4 Dashboard still generates successfully and tests/checks pass
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the country-flow workbook for the INDPROD rows and determine a clean aggregation for country crude production.
2. Add a dashboard figure for global crude production by country and insert it below the crude candidate universe and above crude trade dynamics.
3. Add a visible source citation for the new section, update the smoke test, regenerate the dashboard, and finalize the task.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added a new dashboard section, `Global crude production`, positioned below the crude candidate universe and above crude trade dynamics.
- Built the new figure from `crude_oil_country_flows_2025_domestic_crude_refined_calc.xlsx` using `FLOW_BREAKDOWN = INDPROD` and `UNIT_MEASURE = KBD`, aggregated as the average across the 2025 monthly rows for each country.
- Added a visible citation explaining the INDPROD/KBD source and aggregation basis.
- Updated the dashboard smoke test to assert the new section exists.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_visual_dashboard.py` (1 passed) and regenerated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a new global crude production section to the dashboard using the INDPROD signal from the country-flow workbook. The new section sits below the crude candidate universe, cites the source clearly, and shows the largest producing countries based on average 2025 monthly KBD rows. Verified with the dashboard smoke test and regenerated the HTML artifact.
<!-- SECTION:FINAL_SUMMARY:END -->
