---
id: TASK-3.1
title: Refactor repository entrypoints and shared library seams
status: In Progress
assignee:
  - '@codex'
created_date: '2026-07-09 14:35'
updated_date: '2026-07-09 15:29'
labels: []
dependencies:
  - TASK-3.5
references:
  - CONTEXT.md
parent_task_id: TASK-3
priority: medium
ordinal: 24000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reduce ad hoc script logic across the repository by consolidating supported workflows behind clearer entrypoints and reusable library functions, without changing intended scientific behavior. This includes refinery-model, crude-matching, emissions, economics, plotting, and other analysis flows where practical, while aligning code with the target repository areas refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Supported workflows run through documented entrypoints rather than scattered top-level script logic where practical
- [ ] #2 Shared logic used by multiple scripts or analyses is extracted or consolidated to reduce duplication
- [ ] #3 Refactored entrypoints preserve existing intended behavior aside from explicitly documented fixes
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Apply a safe library-seam cleanup inside refinery_process_model/ by physically redistributing the current functions/ bucket into clearer subareas while preserving compatibility. 2. Create new subpackages such as utils/, io/, and models/ (using models/ instead of core/ because refinery_process_model/core.py already exists at the package root). 3. Move the existing functions/*.py modules into those new subpackages by role and leave symlinks behind in functions/ so both modern and legacy imports continue to work during the transition. 4. Add package __init__.py files and clean transient files, then run representative tests and smoke commands to confirm the move did not break imports or file-path behavior. 5. Leave higher-risk import-path rewrites for a later pass after the filesystem reorganization proves stable.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Starting with a compatibility-first split of refinery_process_model/functions/. Because a top-level core.py module already exists, the replacement buckets for this pass are utils/, io/, and models/ rather than a conflicting core/ directory.

Split the old refinery_process_model/functions/ bucket into clearer physical subpackages: refinery_process_model/utils/, refinery_process_model/io/, and refinery_process_model/models/. Moved utility-style modules (CEPCI_index.py, cost_functions.py, dcfror.py, depreciation.py, equipment_cost_curves.py, functions.py, labor_hours.py, location_factor.py, sensitivity_analysis.py) into utils/, moved data/plot helper modules (plot_API_sulfur_content_crudes.py, range_molecular_type_vs_boiling_pt.py) into io/, and moved domain interpolation/property modules (aromatics_content.py, experimental_hydrotreatment_kerosene_data.py, liquid_product_yield.py, LLE_calculate_num_stages.py, LLE_performance.py) into models/. Left compatibility symlinks behind in refinery_process_model/functions/ so existing modern and legacy imports continue to resolve during the transition. Added __init__.py files for the new subpackages and cleaned transient __pycache__/.DS_Store files. Revalidated with ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py tests/refinery_process_model/test_smoke_distillation.py tests/refinery_process_model/test_operating_costs.py -q (6 passed) plus RUN_LEGACY_EXCEL=0 ./venv/bin/python refinery_process_model/run.py (succeeded).

Updated modern non-legacy imports to use the new module layout directly instead of routing through refinery_process_model/functions symlinks. Modern modules now import from refinery_process_model.utils, refinery_process_model.models, and (where applicable) refinery_process_model.io. This included cost/capital/operating modules, distillation and treatment slices, workbook_builder, dcf_adapter, experiments, and sensitivity runners. Also updated internal moved-module imports such as utils/dcfror.py and utils/cost_functions.py to point at the new package paths. Left legacy/main.py and legacy/main1.py on their old functions.* imports for now to avoid expanding scope into the preserved legacy monoliths. Revalidated with ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py tests/refinery_process_model/test_smoke_distillation.py tests/refinery_process_model/test_operating_costs.py tests/refinery_process_model/test_capital_costs.py tests/refinery_process_model/test_hydrotreatment_run_slice.py tests/refinery_process_model/test_utilities_treated.py -q (9 passed) plus RUN_LEGACY_EXCEL=0 ./venv/bin/python refinery_process_model/run.py (succeeded).
<!-- SECTION:NOTES:END -->
