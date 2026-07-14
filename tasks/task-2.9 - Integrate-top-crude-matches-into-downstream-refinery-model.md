---
id: TASK-2.9
title: Integrate top crude matches into downstream refinery model
status: Done
assignee:
  - '@codex'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-09 14:33'
labels: []
dependencies:
  - TASK-2.8
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/run_costs_all_refineries_top_match.py
parent_task_id: TASK-2
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
After the standalone v1 dataset is stable, connect the top-match output to the downstream refinery workflow referenced in CONTEXT.md without collapsing the standalone research artifact into opaque model-only logic.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Downstream integration consumes the standalone top-match output rather than re-implementing matching logic ad hoc
- [x] #2 The integration path with refinery_process_model scripts is documented
- [x] #3 Any transformations needed between the standalone workbook outputs and the downstream model are reproducible
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the existing all-refineries batch runner plus the standalone match/crude/refinery outputs to define a reproducible downstream-ready input shape.
2. Add code that derives downstream refinery-run inputs directly from the standalone `refinery_crude_matches_v1.csv` output, with explicit support/fallback logic instead of ad hoc workbook parsing.
3. Update the batch runner to consume that derived input and call the maintained `config`/`core.run_scenario` path rather than the legacy import side effect path.
4. Add focused tests for the transform/runner integration and document the workflow in `refinery_process_model/README.md` and `refinery_process_model/RUNNERS.md`.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added refinery_process_model/build_downstream_refinery_run_inputs.py to derive auditable downstream batch inputs directly from refinery_crude_matches_v1.csv, bp_crude_master_v1.csv, and refinery_master_v1.csv, including explicit rank fallback and unsupported-row reasons.

Reworked refinery_process_model/run_costs_all_refineries_top_match.py so it consumes the prepared standalone-match output and calls config + core.run_scenario instead of the legacy import side-effect path.

Extended scenario config/distillation/cost-input seams with optional crude_assay_path and crude_price_key so downstream runs can use exact assay workbooks while keeping crude-price lookup reproducible.

Updated refinery_process_model/README.md and refinery_process_model/RUNNERS.md with the documented integration path.

Added tests/refinery_process_model/test_downstream_refinery_run_inputs.py; verified with ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py -q (2 passed).

Regenerated refinery_process_model/outputs/downstream_refinery_run_inputs_v1.csv (822 rows; 776 downstream-ready, 46 unsupported in current top-3 under present model constraints).

Smoke-tested the new batch entrypoint with RUN_LEGACY_EXCEL=0 ./venv/bin/python refinery_process_model/run_costs_all_refineries_top_match.py --limit 1. The integration path executed and wrote prepared/results CSVs, but the first selected refinery run surfaced an existing assay parse/data issue in thunder-horse.xlsx (ValueError converting '<0.001'). Left as follow-up rather than silently broadening TASK-2.9 scope.

Diagnosed the downstream smoke-test failure to direct  coercion in  when assay Summary cells contain bound-style numeric strings such as '<0.001' (confirmed in top-level , cell D39).

Hardened distillation numeric parsing with a reusable coercion helper that converts /// string cells into numeric values before dataframe-to-numpy conversion across the Summary-sheet cut-property rows.

Added regression coverage in  for the Thunder Horse assay path and revalidated with ....                                                                     [100%] (4 passed).

Re-ran ; the previously failing Thunder Horse-selected refinery now completes with status .

Correction: the distillation parser fix addressed direct float coercion on Summary-sheet bound strings like less-than 0.001 in Thunder Horse. Regression tests now pass and the limit-1 downstream smoke run completes successfully.

Ran the full downstream batch generation with RUN_LEGACY_EXCEL=0. Wrote 822-row prepared inputs and 822-row batch results to refinery_process_model/outputs/. Current result mix: 750 ok, 60 skipped, 12 error.

Skipped rows are mostly unsupported Exxon-only top-3 matches plus 14 refineries missing capacity, which now skip cleanly instead of aborting the batch.

Remaining error rows hit a separate model constraint: distillation interpolation fails for some very large-capacity cases with ValueError x outside allowed range [0, 630.2] (examples: Jamnagar I/II, Ulsan, Zhenhai, Port Arthur II).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Integrated standalone refinery-crude matches into the downstream refinery model through a reproducible prepared-input pipeline, updated the batch runner to use the maintained config/core path, documented regeneration steps, and added focused tests. Verified with focused pytest coverage, smoke tests, and a full batch run; remaining failures were identified as separate downstream model constraints rather than integration-path issues.
<!-- SECTION:FINAL_SUMMARY:END -->
