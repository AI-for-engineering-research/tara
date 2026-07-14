---
id: TASK-2.7
title: Generate canonical v1 Excel workbook
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-08 16:38'
labels: []
dependencies:
  - TASK-2.6
references:
  - CONTEXT.md
parent_task_id: TASK-2
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Generate the inspectable Excel workbook defined in CONTEXT.md from code, using normalized inputs, scores, matches, and config-derived assumptions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The workbook contains Refineries, BP_Crudes, Country_Flows, Scores, Matches, and Assumptions sheets
- [x] #2 Workbook content is produced entirely from code and config rather than manual Excel editing
- [x] #3 The Matches sheet includes top matches, rationale text, match_count, and coverage_note fields
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the current matching outputs, config helpers, and existing workbook-related seams.
2. Build a dedicated workbook generator that assembles Refineries, BP_Crudes, Country_Flows, Scores, Matches, and Assumptions sheets entirely from code/config.
3. Add tests that verify the canonical sheet set and required Matches-sheet columns.
4. Update runner/docs references, generate the workbook artifact, and verify with the relevant pytest subset.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added `refinery_process_model/build_matching_workbook.py`, a dedicated workbook generator that assembles the canonical v1 matching workbook entirely from code and config.
- The workbook now writes six inspectable sheets: `Refineries`, `BP_Crudes`, `Country_Flows`, `Scores`, `Matches`, and `Assumptions`.
- Extended `build_country_sourcing_profiles(...)` and `build_match_engine_outputs(...)` to accept in-memory DataFrames so workbook generation can run directly from code without relying on preexisting CSV artifacts.
- Added `tests/refinery_process_model/test_matching_workbook.py` to verify the canonical sheet set, required Matches columns, and workbook write path behavior.
- Updated `refinery_process_model/README.md` and `refinery_process_model/RUNNERS.md` to document the new workbook generator entrypoint.
- Generated `refinery_process_model/outputs/refinery_crude_matching_workbook_v1.xlsx` and verified sheet names plus Matches columns.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_matching_workbook.py tests/refinery_process_model/test_build_crude_master.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py tests/refinery_process_model/test_matching_config.py tests/refinery_process_model/test_build_country_sourcing_profiles.py` (19 passed).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Built the canonical v1 refinery-to-crude matching workbook generator and tests. The new workflow produces Refineries, BP_Crudes, Country_Flows, Scores, Matches, and Assumptions sheets entirely from code/config, writes `refinery_crude_matching_workbook_v1.xlsx`, and preserves the required Matches-sheet rationale, match_count, and coverage_note fields. Verified with the 19-test pytest subset.
<!-- SECTION:FINAL_SUMMARY:END -->
