---
id: TASK-2.3
title: Build normalized refinery master table
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-08 15:09'
labels: []
dependencies:
  - TASK-2.1
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/build_refinery_master.py
  - tests/refinery_process_model/test_build_refinery_master.py
parent_task_id: TASK-2
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a reproducible extraction and normalization step for the 822 active refineries, producing the refinery attributes needed for matching and workbook output.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The pipeline outputs one normalized row per active refinery with name, country/region, latitude/longitude, crude capacity, NCI, refinery type/class, and integrated status where available
- [x] #2 Refinery type/class values are normalized and any mapping assumptions are documented
- [x] #3 Output is saved in a format that downstream scoring code can load reproducibly
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Build a reusable refinery extraction module that reads the GlobalData refinery workbook, skips export metadata rows, filters to active refineries, and normalizes one row per refinery.
2. Normalize refinery type/class and integrated-status fields explicitly, documenting any assumptions in code/output fields.
3. Add a CLI/script entry point that writes a reproducible CSV for downstream scoring.
4. Add focused tests for header handling, active-row filtering, field normalization, and output reproducibility; then run the relevant test subset and generate the output artifact.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added `refinery_process_model/build_refinery_master.py` to extract the refinery master table from the GlobalData workbook using the real header row, active-refinery filtering, and normalized fields.
- Normalized refinery type and integrated-status labels explicitly via canonical maps, while retaining raw values and normalization-note columns to document assumptions without introducing later capability mappings.
- Added `tests/refinery_process_model/test_build_refinery_master.py`; verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_refinery_master.py` (4 passed).
- Generated reproducible output CSV at `refinery_process_model/outputs/refinery_master_v1.csv`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented `refinery_process_model/build_refinery_master.py` to extract 822 active refineries from the GlobalData workbook into a normalized refinery master table, using the real header row, canonical type/integrated-status normalization, and reproducible CSV output. Added tests in `tests/refinery_process_model/test_build_refinery_master.py`, verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_refinery_master.py`, and generated `refinery_process_model/outputs/refinery_master_v1.csv`.
<!-- SECTION:FINAL_SUMMARY:END -->
