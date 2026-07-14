---
id: TASK-3.2
title: Consolidate repository configuration and path management
status: In Progress
assignee:
  - '@codex'
created_date: '2026-07-09 14:35'
updated_date: '2026-07-09 15:40'
labels: []
dependencies:
  - TASK-3.5
references:
  - CONTEXT.md
parent_task_id: TASK-3
priority: medium
ordinal: 25000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Centralize important paths, filenames, switches, and workflow assumptions across the repository so reruns do not depend on scattered hardcoded values in refinery, emissions, plotting, economics, or data-preparation modules. This includes path cleanup needed to support a clearer folder breakdown such as refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 High-value hardcoded paths, filenames, and workflow switches across the repository are moved to clearer shared configuration points where practical
- [ ] #2 Supported workflows can be regenerated without hunting through many modules for key path or parameter changes
- [ ] #3 Configuration changes are documented for future reruns and extensions
- [ ] #4 Path/config changes support the agreed repository breakdown, including moves into folders such as refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/ where appropriate
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Apply a safe path-management slice inside refinery_process_model/ by categorizing the current excel_files assets under inputs/ while preserving backward compatibility. 2. Create subdirectories such as inputs/cost_data, inputs/trade_data, inputs/refinery_data, inputs/market_data, inputs/chemistry_data, and inputs/climate_lca. 3. Move each workbook/data file into its category and replace its old excel_files root path with a compatibility symlink so existing code paths keep working. 4. Validate representative tests that exercise distillation and downstream batch inputs, then record the resulting categorized layout for later path refactors.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
This slice keeps the excel_files/ root as a compatibility layer made of symlinks, so existing code can continue to reference refinery_process_model/excel_files/<file> while the physical files live under inputs/ by category.

Categorized refinery_process_model/excel_files into physical input buckets under refinery_process_model/inputs/: cost_data, trade_data, refinery_data, market_data, chemistry_data, and climate_lca. Moved the underlying files into those folders and left symlinks at refinery_process_model/excel_files/<filename> so existing code paths keep working unchanged during the transition. Validated representative compatibility with ./venv/bin/python -m pytest tests/refinery_process_model/test_smoke_distillation.py -q and ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py -q (both passed).

Updated the central path helper to reflect the reorganized refinery_process_model layout explicitly. RepoPaths now exposes structured directories and files such as inputs_dir, config_inputs_dir, cost_data_dir, trade_data_dir, refinery_data_dir, market_data_dir, chemistry_data_dir, climate_lca_dir, crude_assays_root_dir, bp_crude_assays_dir, docs_dir, runs_dir, plotting_dir, user_inputs_toml, refinery_matching_toml, density_conversion_xlsx, wind_electricity_xlsx, and global_refinery_data_xlsx. Kept backward-compatible alias properties (input_text_files_dir, crude_assays_dir, excel_files_dir) during the transition. Updated config.py and matching_config.py to use RepoPaths-based defaults instead of hardcoding the old input_text_files layout. Revalidated with ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py tests/refinery_process_model/test_smoke_distillation.py tests/refinery_process_model/test_operating_costs.py tests/refinery_process_model/test_capital_costs.py tests/refinery_process_model/test_hydrotreatment_run_slice.py tests/refinery_process_model/test_utilities_treated.py -q (9 passed), RUN_LEGACY_EXCEL=0 ./venv/bin/python refinery_process_model/run.py, and a small RepoPaths probe script confirming the new explicit paths resolve correctly.

Extended the path cleanup across additional non-legacy refinery_process_model modules to use RepoPaths-backed explicit locations instead of hardcoded pre-reorganization paths. Updated high-value runtime modules and helpers including build_bp_crude_master.py, build_downstream_refinery_run_inputs.py, build_country_sourcing_profiles.py, build_refinery_master.py, distillation.py, hydrotreatment_slice.py, solvent_extraction_slice.py, runs/run_costs_all_refineries_top_match.py, runs/run_global_sensitivity_analysis.py, runs/run_local_sensitivity_analysis.py, runs/build_visual_dashboard.py, plotting/plot_crude_trade_arrows_map.py, plotting/plot_global_refineries_map.py, plotting/plot_refineries_with_bp_matches_map.py, plotting/refinery_capacity_nci_plots.py, utils/functions.py, utils/labor_hours.py, utils/equipment_cost_curves.py, utils/dcfror.py, utils/sensitivity_analysis.py, io/range_molecular_type_vs_boiling_pt.py, and models/* data-loader modules. Remaining visible old-layout references are now mostly compatibility aliases, comments/docstrings, or deliberate preserved legacy code. Revalidated with ./venv/bin/python -m pytest tests/refinery_process_model/test_downstream_refinery_run_inputs.py tests/refinery_process_model/test_smoke_distillation.py tests/refinery_process_model/test_operating_costs.py tests/refinery_process_model/test_capital_costs.py tests/refinery_process_model/test_hydrotreatment_run_slice.py tests/refinery_process_model/test_utilities_treated.py -q (9 passed) plus RUN_LEGACY_EXCEL=0 ./venv/bin/python refinery_process_model/run.py (succeeded).
<!-- SECTION:NOTES:END -->
