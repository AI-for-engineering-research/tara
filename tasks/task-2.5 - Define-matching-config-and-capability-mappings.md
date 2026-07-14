---
id: TASK-2.5
title: Define matching config and capability mappings
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-08 15:22'
labels: []
dependencies:
  - TASK-2.2
  - TASK-2.3
  - TASK-2.4
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/input_text_files/refinery_matching_v1.toml
  - refinery_process_model/matching_config.py
  - tests/refinery_process_model/test_matching_config.py
parent_task_id: TASK-2
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the external config structure for v1 matching assumptions, including refinery capability mappings, score weights, explanation bands, and the initial hard-filter rule shapes for API and sulfur.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A machine-readable config format is defined and stored outside Excel
- [x] #2 The first-pass refinery type capability mapping from CONTEXT.md is encoded in config
- [x] #3 Hard-filter rule shapes for refinery type compatibility, API mismatch, and sulfur mismatch are represented in config even if numeric thresholds are still provisional
- [x] #4 Config content is suitable for rendering into the workbook Assumptions sheet
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define a TOML-based v1 matching config under `refinery_process_model/input_text_files/` covering score weights, NCI explanation bands, refinery capability mappings, and provisional hard-filter rule shapes.
2. Add a small loader/adapter module that reads the config, validates required sections, and exposes a flattened assumptions-table view suitable for workbook rendering.
3. Add focused tests to verify the config loads, the CONTEXT.md first-pass capability mapping is encoded, hard-filter rule shapes are represented, and assumptions rows can be rendered reproducibly.
4. Run the relevant test subset and record the generated config artifacts for downstream matching work.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added machine-readable config file `refinery_process_model/input_text_files/refinery_matching_v1.toml` for v1 matching assumptions, including weights, NCI explanation bands, hard-filter rule shapes, and refinery capability mappings.
- Added `refinery_process_model/matching_config.py` to load/validate the config and flatten it into assumption rows/dataframe form suitable for workbook `Assumptions` rendering.
- Encoded the CONTEXT.md first-pass refinery capability mapping directly in config, plus a documented provisional `Topping` fallback mapping for the refinery types present in the source dataset.
- Represented hard-filter rule shapes for refinery type compatibility, API mismatch, and sulfur mismatch with explicit `threshold_status` markers so scoring code can use the config before numeric calibration is finalized.
- Added `tests/refinery_process_model/test_matching_config.py`; verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_matching_config.py` (4 passed).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented TOML-based matching config in `refinery_process_model/input_text_files/refinery_matching_v1.toml` plus loader/rendering helpers in `refinery_process_model/matching_config.py`. The config now encodes first-pass refinery capability mappings, scoring weights, NCI explanation bands, and provisional hard-filter rule shapes outside Excel, and can be flattened for workbook `Assumptions` rendering. Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_matching_config.py`.
<!-- SECTION:FINAL_SUMMARY:END -->
