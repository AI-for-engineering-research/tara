---
id: TASK-2.11
title: >-
  Add representative stream volume metadata for Exxon crude assays via web
  research
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 16:15'
updated_date: '2026-07-08 16:31'
labels:
  - data
  - exxon
  - crude-matching
dependencies: []
references:
  - refinery_process_model/input_text_files/exxon_crude_latlon_inventory_v1.csv
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
parent_task_id: TASK-2
priority: high
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fill the remaining Exxon crude metadata gap by researching representative stream production or export volume values for the Exxon assay universe and incorporating those values, provenance notes, and any unresolved caveats into the reproducible crude-master workflow. This work should improve the production-signal component for Exxon candidates without overstating precision.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A reproducible Exxon stream-volume inventory is created or updated with representative volume values, units, source links/notes, and explicit missing-value handling for unresolved crudes
- [x] #2 The crude master pipeline carries Exxon representative stream volume metadata into the combined crude universe with provenance fields preserved
- [x] #3 Any caveats about proxy, approximate, or date-specific Exxon volume values are documented in project docs and/or generated inventory outputs
- [x] #4 Tests cover the expected Exxon stream-volume behavior and regenerated outputs remain reproducible
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the current Exxon inventory schema and crude-master integration points.
2. Research representative production/export volume values for the 31 Exxon assay crudes from web-accessible source material, preferring operator/company pages or secondary references with explicit caveats when primary values are unavailable.
3. Extend the Exxon inventory artifact to carry representative stream volume values, units, source links, dates/notes, and unresolved-missing markers.
4. Update the crude-master pipeline and generated inventory outputs to propagate Exxon stream-volume metadata with provenance.
5. Update docs/tests, regenerate affected outputs, and verify with the relevant pytest subset.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Extended `refinery_process_model/input_text_files/exxon_crude_latlon_inventory_v1.csv` with representative stream-volume columns (`representative_stream_volume_bpd`, unit, basis, source URL, note) and populated defensible public values where found.
- Used a conservative policy: preserve blanks for marketed blends or weakly documented streams rather than force synthetic values. Current coverage is 17 of 31 Exxon rows with sourced representative stream-volume proxies and 14 explicit blanks.
- Updated `refinery_process_model/build_bp_crude_master.py` so Exxon rows now ingest stream-volume metadata, preserve provenance for both resolved and unresolved rows, and surface mixed provenance statuses depending on whether stream volume is present.
- Updated `tests/refinery_process_model/test_build_crude_master.py` to assert mixed present/missing Exxon stream-volume behavior and provenance-status coverage.
- Updated `data_inventory_v1.md` to document that Exxon proxy metadata now includes partial stream-volume coverage with explicit blanks and caveats.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_crude_master.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py tests/refinery_process_model/test_matching_config.py tests/refinery_process_model/test_build_country_sourcing_profiles.py` (16 passed).
- Regenerated `refinery_process_model/outputs/bp_crude_master_v1.csv`, `refinery_process_model/outputs/exxon_crude_assay_inventory_v1.csv`, `refinery_process_model/outputs/exxon_crude_assay_inventory_v1.xlsx`, `refinery_process_model/outputs/refinery_crude_scores_v1.csv`, and `refinery_process_model/outputs/refinery_crude_matches_v1.csv` during validation.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added conservative representative stream-volume support for the Exxon assay inventory. Publicly defensible field/project production or capacity proxies are now captured for 17 Exxon crudes, while 14 remain intentionally blank with provenance notes rather than using guessed values. Updated the crude-master pipeline, documentation, and tests, and verified with the 16-test pytest subset plus regenerated crude-master and match outputs.
<!-- SECTION:FINAL_SUMMARY:END -->
