---
id: TASK-3.5
title: 'Audit repository workflows, code paths, and cleanup targets'
status: In Progress
assignee:
  - '@codex'
created_date: '2026-07-09 14:35'
updated_date: '2026-07-09 14:51'
labels: []
dependencies: []
references:
  - CONTEXT.md
parent_task_id: TASK-3
priority: medium
ordinal: 28000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Inventory the major workflows across the full Aromatics_removal_desulfurization_refining repository, including refinery modeling, crude matching, emissions analysis, economics/costing, plotting, and supporting data-preparation scripts. Identify canonical entrypoints, duplicated logic, legacy scripts, generated artifacts, and high-value cleanup targets before editing code. The audit should evaluate and refine a target repository breakdown centered on refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A concise inventory identifies the major workflow families in the repository, their current entrypoints, and the key modules/files involved
- [ ] #2 Known duplicated, legacy, or confusing code paths across the repository are listed with recommended keep/remove/document decisions
- [ ] #3 Cleanup recommendations are scoped into an actionable sequence for the remaining TASK-3 subtasks
- [ ] #4 The audit maps current files and scripts into a proposed repository breakdown centered on refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/, plus any needed shared/docs/tests/legacy areas
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Audit refinery_process_model/ first as phase 1 of the repository cleanup, treating it as the pilot folder structure for later repo-wide reorganization. 2. Inventory current refinery_process_model areas (runs, matching builders, config/text inputs, assay workbooks, reference spreadsheets, outputs, plots, experiments, legacy code, helper modules). 3. Propose a target internal layout with clearer buckets such as core/, io/, utils/, inputs/, crude_assays/, outputs/, plots/, docs/, experiments/, and legacy/. 4. Map current folders like excel_files/ and functions/ into named destinations based on purpose, and identify ambiguous or mixed-content areas that need splitting. 5. Turn the refinery_process_model audit into a concrete move/refactor plan that can feed TASK-3.1, TASK-3.2, and TASK-3.4 before expanding the same cleanup approach to cost_benefit_analysis/ and nvpm_correlations/.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Initial refinery_process_model inventory suggests the following major buckets: BP crude assays/, excel_files/, input_text_files/, functions/, experiments/, legacy/, outputs/, plots, runner/build scripts, and core modeling modules such as config.py/core.py/distillation.py/operating_costs.py. The current functions/ and excel_files/ directories are mixed-purpose and should likely be split by role rather than retained as generic buckets.

Drafted refinery_process_model move-map direction: top-level code splits into runs/, core/, io/, utils/, plotting/, config/, docs/, experiments/, legacy/, crude_assays/, and inputs/ subareas such as reference_data/, trade_data/, cost_data/, market_data/, lca_data/, and config/. Generic functions/ helpers should be redistributed by purpose instead of retained. outputs/ should be split conceptually between canonical tables, plots, and scenario-run artifacts, with large scenario directories grouped under outputs/scenario_runs/.
<!-- SECTION:NOTES:END -->
