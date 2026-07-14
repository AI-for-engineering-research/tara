---
id: TASK-2
title: Build v1 refinery-to-BP-crude matching workflow
status: Done
assignee: []
created_date: '2026-07-08 13:42'
updated_date: '2026-07-09 14:33'
labels: []
dependencies: []
references:
  - CONTEXT.md
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the reproducible v1 workflow described in CONTEXT.md to infer up to the top 3 plausible BP crude matches for each active refinery. The initiative should produce an inspectable research workbook, keep rules/config in code, and support manual spot-check validation without claiming plant-level ground truth.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A reproducible code path generates the canonical workbook described in CONTEXT.md
- [x] #2 The workflow returns up to 3 plausible BP crude matches per refinery with rationale fields and coverage notes
- [x] #3 Thresholds, weights, and capability mappings are stored outside Excel and surfaced in the workbook assumptions output
- [x] #4 Validation notes document spot-check results and known limitations of the heuristic model
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed the v1 refinery-to-BP-crude matching workflow end to end: normalized source datasets, generated the canonical standalone workbook with top-3 plausible crude matches and documented assumptions, validated the heuristic with spot-check notes, and integrated the outputs into downstream refinery-model and dashboard artifacts. Verification across the child tasks included focused tests, regenerated CSV/workbook/map outputs, smoke/full batch runs, and documentation updates; remaining skips/errors are documented model/data limitations rather than incomplete workflow implementation.
<!-- SECTION:FINAL_SUMMARY:END -->
