---
id: TASK-2.21
title: >-
  Evaluate all top-3 crude matches per refinery, average downstream costs, and
  map refinery average hydrotreatment cost
status: Done
assignee:
  - '@codex'
created_date: '2026-07-09 00:11'
updated_date: '2026-07-09 14:33'
labels: []
dependencies:
  - TASK-2.9
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/core.py
  - refinery_process_model/config.py
  - refinery_process_model/cost_inputs.py
  - refinery_process_model/treated_operating_costs.py
  - refinery_process_model/run_costs_all_refineries_top_match.py
  - refinery_process_model/outputs/all_refineries_top_match_treating_costs.csv
  - >-
    refinery_process_model/outputs/all_refineries_top_match_treating_costs_summary.csv
  - refinery_process_model/plots/refinery_avg_hydrotreatment_cost_map.html
  - tests/refinery_process_model/test_downstream_refinery_run_inputs.py
parent_task_id: TASK-2
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend the downstream refinery-model integration so batch costing runs evaluate each refinery against every available top-3 standalone crude match rather than only one selected downstream-ready match. Persist per-match downstream results, derive refinery-level average hydrotreatment cost metrics from the successful top-match runs, regenerate the all-refineries cost output CSV using the richer multi-match structure, and build a color cost map of refinery average hydrotreatment cost for kerosene hydrotreatment.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The downstream batch workflow evaluates each refinery against each supported top-3 standalone crude match and records match-rank-specific outputs reproducibly
- [x] #2 A regenerated output artifact records per-refinery per-match downstream cost results and a refinery-level average cost summary derived from successful top-match runs
- [x] #3 A map artifact visualizes refinery average hydrotreatment cost with color encoding and is generated from code
- [x] #4 Documentation explains how to regenerate the multi-match cost outputs and average-cost map
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Refactor downstream-run input preparation so each refinery emits up to three supported downstream candidate rows, one per match rank, while preserving unsupported reasons and refinery metadata.
2. Rework the batch runner to evaluate all supported rank-1/2/3 matches, regenerate `all_refineries_top_match_treating_costs.csv` as a per-refinery-per-match result table using the updated price data, and write a refinery-level average-cost summary artifact.
3. Add a plotting script that builds a color cost map from the refinery-level average hydrotreatment cost summary.
4. Add focused tests for multi-match preparation/batch aggregation/map generation, update docs, and regenerate the requested outputs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Refactored downstream candidate preparation so  now emits one row per refinery per top-match rank (2,466 rows total), preserving unsupported reasons rank-by-rank while using the updated crude price data.

Reworked  to execute all supported top-3 matches, rewrite  as a per-match result table, and write refinery average summaries to .

Added  and generated  using average treated mid-cost per barrel across successful supported top-match runs.

Added/updated focused tests in ; verified with ...                                                                      [100%] (3 passed).

Regenerated outputs with the updated price data. Current batch counts in : 1,527 ok, 912 skipped, 27 error across 2,466 refinery-match runs. Summary file contains 750 refineries with at least one successful supported run; mean successful matches per summarized refinery is 2.036.

Remaining skips are mostly Exxon assay candidates not yet supported downstream plus 31 missing-capacity rows. Remaining errors are the known large-capacity interpolation limit ().

Correction: generated 2,466 downstream candidate rows, rewrote the per-match cost CSV, wrote the refinery average-cost summary CSV, generated the average-cost map HTML, and verified the focused pytest file with 3 passing tests. Current run counts are 1,527 ok, 912 skipped, and 27 error; remaining issues are mostly unsupported Exxon ranks, 31 missing-capacity rows, and known large-capacity interpolation limits.

Updated  to color refineries by average premium cost per gallon (midpoint of average premium min/max, converted from $/bbl to $/gal) instead of average treated cost per barrel. Updated the map script and focused test, re-ran the pytest file, and regenerated the HTML map.

Updated the multi-match downstream runner to use spatial wind prices again: for wind runs it now loads refinery_process_model/excel_files/US_wind_electricity data_2020.xlsx, assigns each refinery the nearest LCOE value by latitude/longitude, and passes that as an explicit electricity-price override through the maintained core/config path.

Extended ScenarioConfig and pricing code so electricity price overrides flow through both DCF argument construction and treated operating-cost calculations instead of falling back to the fixed near_term_wind assumption.

Revalidated with ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py -q (3 passed), reran the full downstream batch, and regenerated the average-premium map HTML. The batch still yields 2,466 rows with 1,527 ok / 912 skipped / 27 error, but wind price columns now vary spatially (override mean about 0.0966 $/kWh; min about 0.0402; max about 0.3411).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Extended the downstream batch workflow to run every supported top-3 crude match per refinery, regenerated per-match and refinery-average output artifacts, and added a generated average-cost map plus documentation/tests for reproducing the workflow. Verified with focused pytest coverage and a full regenerated batch/map run; remaining skipped/error rows are documented known downstream constraints rather than unresolved scope within this task.
<!-- SECTION:FINAL_SUMMARY:END -->
