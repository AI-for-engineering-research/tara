---
id: TASK-2.10
title: Add Exxon crude assay workbooks to the crude matching universe
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 15:39'
updated_date: '2026-07-08 16:09'
labels: []
dependencies:
  - TASK-2.6
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/input_text_files/exxon_crude_latlon_inventory_v1.csv
  - refinery_process_model/build_bp_crude_master.py
  - refinery_process_model/build_refinery_bp_crude_matches.py
  - tests/refinery_process_model/test_build_crude_master.py
  - tests/refinery_process_model/test_build_refinery_bp_crude_matches.py
parent_task_id: TASK-2
priority: high
ordinal: 8500
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Incorporate the newly found Exxon crude assay Excel workbooks into the crude-matching workflow so they become part of the candidate crude universe alongside the existing BP assay set. This task should inventory the new assay files, extend the crude master extraction and provenance model, and update downstream matching outputs so the expanded crude universe can be used before workbook generation and validation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The new Exxon assay workbooks are inventoried and inclusion/provenance rules are documented
- [x] #2 The crude master pipeline is extended so supported Exxon assay workbooks are normalized reproducibly alongside the existing BP crude set
- [x] #3 Downstream matching inputs/outputs are updated so the scoring engine evaluates the expanded crude universe and preserves source provenance in results
- [x] #4 Any schema or config changes required by the expanded crude universe are documented and regenerated artifacts are produced reproducibly
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Gather representative lat/lon points for the Exxon assay set from web-search/geocoded origin proxies, record provenance/notes, and update the Exxon inventory artifact with those coordinates.
2. Extend the crude master pipeline to carry Exxon lat/lon inventory fields into the combined candidate universe where available, while preserving provenance and missing-value notes for any unresolved cases.
3. Rename crude-master and match-test/output naming from BP-specific labels to source-neutral crude labels, and regenerate the combined refinery–crude score/match outputs so they clearly represent both BP and Exxon candidates.
4. Update tests and artifacts, run the relevant pytest subset, and refresh generated outputs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Inventoried 31 Exxon assay workbooks in `Exxon crude assays/`; all inspected files use `Summary (C)` + `Yield Graph (C)` sheets and expose assay reference, crude name, origin, assay date, API, and sulfur fields.
- Extended `refinery_process_model/build_bp_crude_master.py` so the crude master now combines 35 BP assay rows and 31 Exxon assay rows into one source-aware candidate universe with provenance columns (`assay_source`, `assay_source_company`, `provenance_status`).
- Generated `refinery_process_model/outputs/exxon_crude_assay_inventory_v1.csv` to document the Exxon inclusion set and provenance gaps; Exxon rows currently ingest assay-derived fields only and explicitly flag missing lat/lon + representative stream volume metadata.
- Updated `refinery_process_model/build_refinery_bp_crude_matches.py` so the scoring engine evaluates the expanded 66-crude universe, handles missing Exxon geography/production metadata gracefully, and preserves assay provenance in match outputs.
- Updated `data_inventory_v1.md` to document the Exxon source family, parsing rules, and expanded crude-master schema.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_bp_crude_master.py tests/refinery_process_model/test_build_country_sourcing_profiles.py tests/refinery_process_model/test_matching_config.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py` (16 passed).
- Regenerated `refinery_process_model/outputs/bp_crude_master_v1.csv`, `refinery_process_model/outputs/exxon_crude_assay_inventory_v1.csv`, `refinery_process_model/outputs/refinery_bp_crude_scores_v1.csv`, and `refinery_process_model/outputs/refinery_bp_crude_matches_v1.csv`.

- Added curated Exxon proxy location inventory in `refinery_process_model/input_text_files/exxon_crude_latlon_inventory_v1.csv`, using representative origin proxies and Wikidata source links to supply lat/lon for all 31 Exxon assays.
- Updated `refinery_process_model/build_bp_crude_master.py` to merge the Exxon proxy lat/lon inventory into the combined crude master and to write both CSV and Excel versions of the Exxon inventory (`exxon_crude_assay_inventory_v1.csv` and `.xlsx`).
- Renamed the crude-master test file to `tests/refinery_process_model/test_build_crude_master.py` and updated assertions for the new Exxon coordinate/provenance behavior.
- Renamed combined match outputs to source-neutral names: `refinery_crude_scores_v1.csv` and `refinery_crude_matches_v1.csv`, reflecting that the matcher now ranks both BP and Exxon candidates together.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_crude_master.py tests/refinery_process_model/test_build_country_sourcing_profiles.py tests/refinery_process_model/test_matching_config.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py` (16 passed).
- Regenerated `refinery_process_model/outputs/exxon_crude_assay_inventory_v1.xlsx`, `refinery_process_model/outputs/refinery_crude_scores_v1.csv`, and `refinery_process_model/outputs/refinery_crude_matches_v1.csv`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Expanded the Exxon integration to include curated proxy lat/lon points for all 31 Exxon assays, written to both `exxon_crude_assay_inventory_v1.csv` and `exxon_crude_assay_inventory_v1.xlsx`. Updated the combined crude master to carry Exxon coordinate provenance, renamed the crude-master test file to `test_build_crude_master.py`, and renamed combined match outputs to `refinery_crude_scores_v1.csv` and `refinery_crude_matches_v1.csv` so they clearly represent joint BP+Exxon candidate matching. Verified with the 16-test pytest subset and regenerated the affected artifacts.
<!-- SECTION:FINAL_SUMMARY:END -->
