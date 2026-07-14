---
id: TASK-2.2
title: Build normalized BP crude master table
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:42'
updated_date: '2026-07-08 15:06'
labels: []
dependencies:
  - TASK-2.1
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/build_bp_crude_master.py
  - tests/refinery_process_model/test_build_bp_crude_master.py
parent_task_id: TASK-2
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a reproducible extraction pipeline that converts the 35 BP assay sources into one normalized BP crude master table with the v1 technical-fit attributes and any supporting identifiers needed downstream.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The pipeline outputs one normalized row per BP crude with API, sulfur, latitude/longitude, production, and source identifiers where available
- [x] #2 Extraction handles missing or inconsistent source formatting explicitly rather than relying on manual workbook edits
- [x] #3 Output is saved in a format that downstream scoring code can load reproducibly
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Build a reusable BP crude extraction module that reads the 35 assay workbooks plus the master lat/lon workbook and normalizes one row per crude.
2. Handle semi-structured assay sheets explicitly with label-based parsing and an explicit crude-name/file manifest for known inconsistencies.
3. Add a small CLI/script entry point that writes a reproducible downstream-loadable output file (CSV).
4. Add focused tests for parsing, row counts, and key field completeness; then run the relevant test subset and generate the output artifact.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added `refinery_process_model/build_bp_crude_master.py` to build a normalized BP crude master table from the 35 assay workbooks plus the master lat/lon workbook.
- Implemented explicit crude-to-workbook mapping and label-based parsing of semi-structured assay `Summary` sheets to extract reference, assay name, origin, sample date, API, and sulfur.
- Added `tests/refinery_process_model/test_build_bp_crude_master.py`; verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_bp_crude_master.py` (3 passed).
- Generated reproducible output CSV at `refinery_process_model/outputs/bp_crude_master_v1.csv`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented `refinery_process_model/build_bp_crude_master.py` to extract one normalized row per BP crude from the 35 assay workbooks plus the master lat/lon workbook, using explicit crude-file mapping and label-based parsing for semi-structured sheets. Added tests in `tests/refinery_process_model/test_build_bp_crude_master.py`, verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_bp_crude_master.py`, and generated `refinery_process_model/outputs/bp_crude_master_v1.csv`.
<!-- SECTION:FINAL_SUMMARY:END -->
