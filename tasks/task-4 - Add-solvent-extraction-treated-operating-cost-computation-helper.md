---
id: TASK-4
title: Add solvent-extraction treated operating-cost computation helper
status: In Progress
assignee:
  - '@pi'
created_date: '2026-07-10 16:17'
updated_date: '2026-07-10 16:23'
labels: []
dependencies: []
modified_files:
  - refinery_process_model/cost_inputs.py
priority: medium
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a solvent-extraction treated operating-cost computation alongside the existing hydrotreatment treated operating-cost helper so solvent extraction cost paths can reuse a shared implementation instead of duplicating workbook/cost-input logic.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 treated_operating_costs.py exposes a solvent-extraction operating-cost computation API alongside the hydrotreatment API
- [x] #2 The solvent-extraction helper accounts for distillation utilities, solvent-extraction treatment utilities, sulfolane makeup raw-material cost, and fixed-capital inputs
- [x] #3 Regression tests cover the solvent-extraction operating-cost helper with scalar or range utility inputs
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Refactor treated_operating_costs.py to share common energy/raw-material aggregation helpers. 2. Add a solvent-extraction treated operating-cost function that prices sulfolane makeup and reuses the shared operating-cost calculation path. 3. Replace duplicated solvent-extraction operating-cost logic in workbook_builder.py and cost_inputs.py with the shared helper. 4. Add regression tests covering the new solvent-extraction helper with scalar and range utility inputs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Refactored treated_operating_costs.py to share common energy and operating-cost calculation helpers, added solvent_extraction_treatment_totals plus compute_treated_solvent_extraction_operating_costs, and switched workbook_builder's solvent-extraction operating-cost sheet path to reuse the new helper. Added regression coverage in tests/refinery_process_model/test_treated_operating_costs.py.

Refactored refinery_process_model/cost_inputs.py to import solvent_extraction_treatment_totals and compute_treated_solvent_extraction_operating_costs from treated_operating_costs.py, deleting duplicated solvent-extraction treatment-total and operating-cost calculations while preserving DCF arg construction.
<!-- SECTION:NOTES:END -->
