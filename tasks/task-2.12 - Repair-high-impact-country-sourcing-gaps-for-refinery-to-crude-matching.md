---
id: TASK-2.12
title: Repair high-impact country sourcing gaps for refinery-to-crude matching
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 18:27'
updated_date: '2026-07-08 18:34'
labels:
  - data
  - sourcing
  - validation
  - calibration
dependencies: []
documentation:
  - CONTEXT.md
  - data_inventory_v1.md
  - backlog/docs/validation/doc-2
parent_task_id: TASK-2
priority: high
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Repair the highest-impact missing or weak country sourcing inputs that currently distort refinery-to-crude rankings, focusing first on countries that actually have refineries in the dataset and already showed validation failures or high leverage on output quality. Priority targets include Oman and the United Arab Emirates, followed by high-capacity import-driven refinery countries with ambiguous trade coverage and any closely related Gulf proxy/candidate-crude gaps needed to make the sourcing signal useful.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A ranked target list is defined for the highest-impact refinery countries with missing, weak, or ambiguous sourcing signals, with explicit rationale based on refinery count, capacity, and validation impact
- [x] #2 Country sourcing inputs are repaired or improved for the first-priority refinery countries, especially Oman and the United Arab Emirates, using reproducible source data and documented assumptions
- [x] #3 Any remaining high-impact ambiguities for major import-refining countries (for example United Kingdom, Italy, Spain, Singapore, Belgium) are documented together with the practical limitation they impose on matching quality
- [x] #4 Regenerated sourcing profiles, scores, matches, and validation notes show whether the repaired country signals improved the affected refinery rankings
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the domestic and trade source tables plus country-normalization logic to determine why Oman and UAE currently have no sourcing signal.
2. Build a ranked target list of the highest-impact refinery countries with missing, weak, or ambiguous sourcing based on refinery count, capacity, and validation findings.
3. Repair reproducible sourcing coverage for the first-priority countries (starting with Oman and UAE), update documentation/notes, regenerate sourcing and matching outputs, and compare the affected refinery rankings.
4. Document remaining high-impact ambiguities for major import-refining countries and update validation notes with the before/after effect.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Inspected the raw domestic and trade source files and confirmed that Oman (`OM`) and the UAE (`AE`) have `DOMCRREF_CALC` rows but all-zero KBD values, while crude import-source rows are absent for `OMN` and `ARE` in the current trade table.
- Added documented fallback overrides in `refinery_process_model/input_text_files/country_sourcing_overrides_v1.csv` for Oman and the United Arab Emirates so active refinery capacity can be used as a domestic producer-state sourcing proxy only when the normal source tables provide no usable crude-flow signal.
- Updated `refinery_process_model/build_country_sourcing_profiles.py` to load/apply the override file after normal source extraction and to surface `override_applied` in the summary output.
- Updated `data_inventory_v1.md` to document the override source and its intended use.
- Added test coverage in `tests/refinery_process_model/test_build_country_sourcing_profiles.py` to verify that Oman now receives a moderate-confidence override-backed sourcing signal.
- Created validation note `doc-4` (`backlog/docs/validation/doc-4 - High-impact-country-sourcing-gap-repair.md`) with a ranked target list, root-cause findings, before/after ranking impact for Oman/UAE refineries, and remaining major import-country ambiguities.
- Regenerated country sourcing outputs, refinery-crude scores/matches, and the canonical workbook.
- Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_build_country_sourcing_profiles.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py tests/refinery_process_model/test_matching_workbook.py` (11 passed).
- Observed improvement after regeneration: Sohar I and Duqm I now rank `Oman Export Blend` first; Fujairah I now ranks `Murban` first. Mina Al Fahal and the UAE condensate-splitter cases remain constrained by capability rules and candidate-universe gaps.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Repaired the highest-impact country sourcing gaps that were clearly harming Gulf refinery rankings by adding documented Oman/UAE fallback sourcing overrides and regenerating all dependent outputs. The repair improved several affected rankings (for example Sohar I, Duqm I, and Fujairah I), while the remaining weak Gulf cases are now more clearly attributable to capability-threshold choices and missing Gulf candidate crudes rather than absent country sourcing alone. The work is documented in `doc-4`, and the remaining high-impact ambiguities for major import-refining countries are explicitly recorded there.
<!-- SECTION:FINAL_SUMMARY:END -->
