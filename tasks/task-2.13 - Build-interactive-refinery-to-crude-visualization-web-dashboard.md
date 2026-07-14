---
id: TASK-2.13
title: Build interactive refinery-to-crude visualization web dashboard
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 18:42'
updated_date: '2026-07-08 18:45'
labels:
  - visualization
  - dashboard
  - matching
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
  - backlog/docs/validation/doc-2
parent_task_id: TASK-2
priority: high
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a single interactive web experience that helps inspect the refinery/crude universe and understand the matching logic. The dashboard should include refinery visualizations, a country-level view of refinery type mix, a crude-origin map, and a human-readable explanation of how the refinery-to-crude matcher works.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A generated web dashboard exists that combines multiple refinery/crude visualizations into one navigable HTML experience
- [x] #2 The dashboard includes a global refinery visualization and a country-level visualization showing refinery type mix by country
- [x] #3 The dashboard includes a crude-origin map covering the combined crude universe used by the matcher
- [x] #4 The dashboard includes an explanation of the refinery-to-crude matching logic, including hard filters, soft scoring, and major caveats
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reuse the generated refinery/crude outputs and existing plotting utilities where possible.
2. Build a single standalone HTML dashboard that includes: a refinery map colored by refinery type, a country-level refinery-type mix view, a crude-universe map, and a matching-logic explainer section with caveats.
3. Add at least a smoke-level automated test for dashboard generation, generate the dashboard artifact, and update docs/run instructions.
4. Note that the requested visual annotator tool is not available in this harness, so implement the dashboard directly with Plotly and custom HTML/CSS.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added `refinery_process_model/build_visual_dashboard.py`, which builds a single standalone HTML dashboard from the generated refinery/crude matching outputs.
- The dashboard includes: a global refinery map colored by refinery type, a country-level refinery-type capacity mix chart, a country-by-refinery-type heatmap, a combined BP+Exxon crude-universe map, and a matching-logic explainer section with both narrative cards and a sankey-style flow diagram.
- Because the requested visual annotator tool is not available in this harness, the dashboard was implemented directly with Plotly plus custom HTML/CSS for a more presentation-style web experience.
- Added smoke test `tests/refinery_process_model/test_visual_dashboard.py` to verify that the dashboard writes and includes the expected sections.
- Generated `refinery_process_model/plots/refinery_crude_visual_dashboard.html`.
- Updated `refinery_process_model/README.md` and `refinery_process_model/RUNNERS.md` to document the new dashboard entrypoint.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_visual_dashboard.py` (1 passed).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Built an interactive refinery-to-crude visualization dashboard as a single standalone HTML page. It combines refinery maps, country refinery-type mix views, a combined crude-universe map, and a matching-logic explainer with caveats. The requested visual annotator tool was not available in this harness, so the implementation uses Plotly plus custom HTML/CSS instead. The dashboard was generated successfully and documented in the repo runner/docs files.
<!-- SECTION:FINAL_SUMMARY:END -->
