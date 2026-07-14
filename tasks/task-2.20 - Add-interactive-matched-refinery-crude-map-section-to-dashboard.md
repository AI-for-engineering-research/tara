---
id: TASK-2.20
title: Add interactive matched refinery-crude map section to dashboard
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 23:14'
updated_date: '2026-07-08 23:18'
labels: []
dependencies: []
parent_task_id: TASK-2
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a new section to the Refinery-to-Crude Matching Dashboard that shows refinery markers alongside crude-origin markers and makes refinery-to-top-crude relationships inspectable from the map itself. Hovering a refinery should show its top crude fits and concise why/rationale text, and the corresponding crude markers should visually light up so the relationship is easy to follow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Dashboard includes a dedicated matched refinery-crude map section
- [x] #2 Map shows both refinery markers and crude-origin markers in the same view
- [x] #3 Hovering a refinery shows its top crude fits and concise why/rationale text
- [x] #4 Hovering a refinery visually emphasizes the crude markers for that refinery's matched candidates
- [x] #5 Tests cover the new dashboard section output and hover/light-up wiring
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the existing dashboard builder and matched-refinery map code to identify reusable refinery/crude hover data and figure-building logic.
2. Add a dedicated interactive matched refinery-crude map figure that renders refinery markers and crude-origin markers together and carries enough custom data for refinery hover explanations plus matched-crude highlighting.
3. Embed the new map as a new dashboard section and attach client-side Plotly hover/unhover logic so hovering a refinery brightens its matched crude markers.
4. Extend tests to assert the new section and hover-highlighting wiring are present, then regenerate the dashboard HTML as needed.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added a new matched refinery/crude dashboard map section in `refinery_process_model/build_visual_dashboard.py`.
- Built a combined Plotly geo figure with refinery markers plus crude-origin markers in the same view.
- Refinery hover text now shows top 1–3 crude fits and stored rationale text from `refinery_crude_matches_v1.csv`.
- Added client-side Plotly hover/unhover wiring so matched crude markers brighten, grow, and outline when the user hovers a refinery.
- Updated `tests/refinery_process_model/test_visual_dashboard.py` and regenerated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.
- Validation run: `PYTHONPATH=. venv/bin/pytest tests/refinery_process_model/test_visual_dashboard.py -q` (passed) and `PYTHONPATH=. python3 -m refinery_process_model.build_visual_dashboard`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a new interactive dashboard section that overlays refinery markers and crude-origin markers, shows top matched crudes plus rationale text on refinery hover, and highlights the corresponding crude markers client-side when a refinery is hovered. Verified by regenerating `refinery_process_model/plots/refinery_crude_visual_dashboard.html` and running `PYTHONPATH=. venv/bin/pytest tests/refinery_process_model/test_visual_dashboard.py -q`.
<!-- SECTION:FINAL_SUMMARY:END -->
