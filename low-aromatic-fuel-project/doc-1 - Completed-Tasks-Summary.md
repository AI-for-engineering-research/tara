---
id: doc-1
title: Completed Tasks Summary
type: guide
created_date: '2026-07-16 19:23'
updated_date: '2026-07-20 15:15'
---
# Completed Tasks Summary

_Last updated: 2026-07-20_

## Cost-benefit / climate LCA

- **TASK-1.1 — Define cost_benefit_analysis model framing**
  - Set the initial model boundary.
  - Defined canonical inputs and outputs.
  - Chose a climate-only first version.
  - Recorded the 20-year horizon and min/nominal/max uncertainty structure.

- **TASK-1.11 — Add climate LCA outputs to refinery_process_model**
  - Added baseline and treated pathway LCA outputs to repo-native scenario results.
  - Exposed LCA values in CLI summaries and batch CSV outputs.
  - Established a clean in-repo seam for downstream cost-benefit work.

- **TASK-1.12 — Apply energy allocation to shared climate LCA refinery burdens**
  - Allocated shared distillation burdens by kerosene energy share.
  - Kept hydrotreatment burdens fully assigned to treated kerosene.
  - Added solvent-extraction allocation ranges for aromatics coproduct treatment.

## Batch runs, workbooks, and plots

- **TASK-2 — Expand refinery process model batch analysis and comparison plots**
  - Established the larger batch-analysis workflow.
  - Added supporting comparison outputs around the scenario matrix.
  - **Relevant outputs**
    - `outputs/scratch/batch_full_results.csv`
    - `outputs/scratch/batch_full_manifest.csv`
    - `outputs/scratch/batch_full_failures.csv`
    - plot files under `outputs/plot_data/` and `outputs/plots/`

- **TASK-2.1 — Add comprehensive aromatics-removal batch runner**
  - Built the repo-native batch runner.
  - Covered Mars, Oman, and Murban across capacities, pathways, electricity, hydrogen, and boiler combinations.
  - **Relevant outputs**
    - consolidated batch result CSVs used by downstream plots and workbook generation

- **TASK-2.2 — Add refinery cost comparison plotting code**
  - Added comparison plots for treatment-cost results across batch scenarios.
  - **Relevant outputs**
    - `outputs/plot_data/cost_by_crude_capacity.csv`
    - `outputs/plot_data/mars_100k_configuration_cost.csv`
    - `outputs/plots/cost_by_crude_capacity.png`
    - `outputs/plots/cost_by_crude_capacity.pdf`
    - `outputs/plots/mars_100k_configuration_cost.png`
    - `outputs/plots/mars_100k_configuration_cost.pdf`

- **TASK-2.3 — Add Mars configuration LCA comparison plot**
  - Created a Mars-focused LCA comparison figure across treatment configurations.
  - Fixed hydrotreatment treated-energy and hydrogen-source handling so saved LCA results differ correctly between SMR and electrolysis.
  - **Relevant outputs**
    - Mars 100k LCA comparison figure outputs under `outputs/plots/`
    - exact filtered LCA comparison CSV under `outputs/plot_data/`

- **TASK-2.4 — Create workbook for batch scenario runs**
  - Wrote one workbook per successful scenario.
  - Included summary, process, cost, utility, and LCA sheets.
  - **Relevant outputs**
    - `outputs/scenario_runs/batch_workbooks/`
    - `outputs/batch_aromatics_scenarios.csv`
    - `outputs/scratch/batch_aromatics_scenarios_manifest.csv`
    - `outputs/scratch/batch_aromatics_scenarios_failures.csv`

- **TASK-3 — Add Mars 100k cost premium breakdown stacked-bar plots**
  - Visualized treated-vs-baseline premium components for ordered Mars 100 kBPD configurations.
  - **Relevant outputs**
    - `outputs/plot_data/mars_100k_configuration_premium_breakdown.csv`
    - `outputs/plots/mars_100k_configuration_premium_breakdown_min.png`
    - `outputs/plots/mars_100k_configuration_premium_breakdown_min.pdf`
    - `outputs/plots/mars_100k_configuration_premium_breakdown_max.png`
    - `outputs/plots/mars_100k_configuration_premium_breakdown_max.pdf`
    - refreshed full-batch dataset in `outputs/batch_aromatics_scenarios.csv`

## Crude price data

- **TASK-4 — Fix global crude prices**
  - Completed the crude-price cleanup workflow.
  - Updated the project’s crude-price basis.

- **TASK-4.1 — Inventory historical crude price source files**
  - Cataloged available source files and coverage for historical crude pricing.
  - **Where the files are**
    - input workbooks: `excel_files/historical_crude_price_data/`
    - inventory output: `outputs/canonical/global_crude_prices/historical_crude_price_inventory.csv`
  - The inventory CSV records the reviewed workbook list, mappings to project crude names where available, and notes on ambiguous or proxy-style matches.

- **TASK-4.2 — Compute 20-year mean prices for available crudes**
  - Produced long-run average price values from the historical source set.
  - **Crudes with local 20-year mean prices available**
    - Basrah Medium
    - Brent
    - Ekofisk
    - Forties
    - Girassol
    - Heavy Louisiana Sweet
    - Mars
    - Murban
    - Oman Export Blend
    - Terengganu (Tapis assay)
    - Bioko Norte (Zafiro Blend assay)
  - **Crudes without a local 20-year mean price available at this stage**
    - Alaska North Slope
    - Alvheim Blend
    - Azeri (Ceyhan)
    - Azeri Light (Supsa)
    - Bacalhau
    - Bakken
    - Banyu Urip
    - Basrah Heavy
    - Bonga
    - Clair
    - Clov
    - Cold Lake Blend
    - Cossack
    - Culzean
    - Dalia
    - Domestic Sweet
    - Ebok
    - Erha
    - Galeota
    - Gindungo
    - Golden Arrowhead
    - Grane
    - Hebron
    - Hibernia
    - HOOPS Blend
    - Hungo
    - Johan Sverdrup
    - Kearl
    - Kirkuk
    - Kissanje
    - Kutubu Blend
    - Liza
    - Mondo
    - Mostarda
    - Payara Gold
    - Pazflor
    - Plutonio
    - Qua Iboe
    - Saturno Blend
    - Saxi-Batuque Blend
    - Schiehallion
    - Skarv
    - Southern Green Canyon
    - Thunder Horse
    - Unity Gold
    - Upper Zakum
    - Usan
    - WTI Light - Export
    - Yoho

- **TASK-4.3 — Create consolidated crude price reference file**
  - Merged available crude prices into a single reference table used by the repo.
  - **Where the files are**
    - main consolidated reference: `outputs/canonical/global_crude_prices/crude_price_reference_2006_2025.csv`
    - summary table: `outputs/canonical/global_crude_prices/crude_price_summary.csv`
  - The reference CSV gives one row per crude with its 20-year mean price and source metadata.
  - It contains the 11 initially available local price series listed under TASK-4.2.

- **TASK-4.4 — Identify missing price coverage across current crude assays**
  - Mapped which assay crudes lacked direct price coverage.
  - Documented the proxy pre-screen rule used for downstream assignment.
  - **Where the files are**
    - coverage information is reflected in the canonical crude-price outputs under `outputs/canonical/global_crude_prices/`
    - first-stage proxy results: `outputs/canonical/global_crude_prices/crude_price_proxy_assignments.csv`
  - **API / sulfur requirements documented here**
    - candidate proxies must be within **±3.0 °API** of the target crude
    - and within **±0.2 wt% sulfur** of the target crude
    - only after passing both filters does geographic ranking apply
  - **Crudes with a valid first-stage proxy from the original covered set**
    - Alvheim Blend
    - Azeri (Ceyhan)
    - Bacalhau
    - Banyu Urip
    - Bonga
    - Clov
    - Cossack
    - Domestic Sweet
    - Galeota
    - Gindungo
    - Golden Arrowhead
    - Hibernia
    - HOOPS Blend
    - Kissanje
    - Liza
    - Mondo
    - Plutonio
    - Qua Iboe
    - Unity Gold
    - Usan
    - WTI Light - Export
    - Yoho
  - **Crudes with no valid first-stage proxy under the ±3.0 °API / ±0.2 wt% sulfur rule**
    - Alaska North Slope
    - Azeri Light (Supsa)
    - Bakken
    - Basrah Heavy
    - Clair
    - Cold Lake Blend
    - Culzean
    - Dalia
    - Ebok
    - Erha
    - Grane
    - Hebron
    - Hungo
    - Johan Sverdrup
    - Kearl
    - Kirkuk
    - Kutubu Blend
    - Mostarda
    - Payara Gold
    - Pazflor
    - Saturno Blend
    - Saxi-Batuque Blend
    - Schiehallion
    - Skarv
    - Southern Green Canyon
    - Thunder Horse
    - Upper Zakum

- **TASK-4.6 — Research no-fit crude proxy candidates**
  - Identified plausible proxy crudes for assays with no direct price match.
  - **Results from `outputs/canonical/global_crude_prices/no_fit_crudes_v2.csv`**
    - Newly found prices from external research sources (mainly Argus, plus a few other cited sources) were obtained for:
      - Alaska North Slope
      - Azeri Light (Supsa)
      - Bakken
      - Basrah Heavy
      - Cold Lake Blend
      - Dalia
      - Ebok
      - Grane
      - Hungo
      - Johan Sverdrup
      - Kirkuk
      - Kutubu Blend
      - Mostarda
      - Pazflor
      - Saturno Blend
      - Saxi-Batuque Blend
      - Skarv
      - Southern Green Canyon
      - Thunder Horse
      - Upper Zakum
    - Still unpriced after the v2 research pass:
      - Clair
      - Culzean
      - Erha
      - Hebron
      - Kearl
      - Payara Gold
      - Schiehallion

- **TASK-4.7 — Determine proxy-selection method for missing crude prices**
  - Formalized how missing crude prices should be assigned through proxies.
  - **Which code does this**
    - `refinery_process_model/runs/build_crude_price_proxy_assignments.py`
    - `refinery_process_model/runs/build_updated_crude_price_table.py`
  - **Method**
    - `build_crude_price_proxy_assignments.py` loads the crude master table and the direct price reference table.
    - It screens covered candidate crudes against each missing crude.
    - A candidate is only eligible if it passes both thresholds:
      - **API difference ≤ 3.0 °API**
      - **sulfur difference ≤ 0.2 wt%**
    - Eligible candidates are then ranked primarily by **geographic distance**.
    - The script writes explicit assignment, ranking, and summary tables.
  - **Where the files are**
    - first-stage proxy logic outputs live under `outputs/canonical/global_crude_prices/`
    - second-stage compatibility outputs:
      - `outputs/canonical/global_crude_prices/no_fit_crudes_v2_compatibility_assignments.csv`
      - `outputs/canonical/global_crude_prices/no_fit_crudes_v2_compatibility_rankings.csv`
      - `outputs/canonical/global_crude_prices/no_fit_crudes_v2_compatibility_summary.csv`
    - final consolidated price table:
      - `outputs/canonical/global_crude_prices/updated_crude_price_table.csv`
      - `outputs/canonical/global_crude_prices/updated_crude_price_table_summary.csv`
  - **Second-stage proxy assignments from the v2 compatibility pass**
    - Clair → Pazflor
    - Culzean → Skarv
    - Erha → Saxi-Batuque Blend
    - Hebron → Grane
    - Kearl → Cold Lake Blend
    - Payara Gold → Johan Sverdrup
    - Schiehallion → Pazflor
  - **Second-stage proxy-fit details**
    - Clair → Pazflor
      - ΔAPI = 1.10
      - ΔSulfur = 0.033 wt%
    - Culzean → Skarv
      - ΔAPI = 0.40
      - ΔSulfur = 0.084 wt%
    - Erha → Saxi-Batuque Blend
      - ΔAPI = 0.483
      - ΔSulfur = 0.0318 wt%
    - Hebron → Grane
      - ΔAPI = 0.0006
      - ΔSulfur = 0.0370 wt%
    - Kearl → Cold Lake Blend
      - ΔAPI = 0.288
      - ΔSulfur = 0.0406 wt%
    - Payara Gold → Johan Sverdrup
      - ΔAPI = 1.500
      - ΔSulfur = 0.1750 wt%
    - Schiehallion → Pazflor
      - ΔAPI = 1.20
      - ΔSulfur = 0.006 wt%
  - All 7 remaining v2 targets found at least one compatible candidate in this second-stage pass.

## Refinery model and reporting updates

- **TASK-6 — Update scenario-run Excel LCA and utility reporting**
  - Expanded scenario workbook reporting so `LCA Results` shows annual emissions, allocation factors, and emissions per MJ side by side.
  - Preserved the expanded utility reporting while making the allocation logic visible for baseline and treated pathways.
  - Kept workbook generation compatible with hydrotreatment and solvent-extraction cases, including solvent min/max allocation-factor reporting.

- **TASK-7 — Use vacuum-unit flow for vacuum distillation utilities**
  - Aligned utility scaling with vacuum-unit throughput instead of total crude rate.
  - Kept cost and LCA scaling bases consistent.

- **TASK-8 — Add steam and cooling water system costs to batch workbook equipment sheets**
  - Exposed utility-system equipment purchase costs directly in workbook reporting.
  - **Relevant outputs**
    - updated `Equipment Costs` sheets inside scenario workbooks in `outputs/scenario_runs/batch_workbooks/`

- **TASK-9 — Fix wind MSP plotting script and regenerate plots**
  - Restored the missing numpy import.
  - Added regression coverage.
  - Refreshed default plot outputs.
  - **Relevant outputs**
    - refreshed default plot files under `outputs/plots/`
    - refreshed default plot-data files under `outputs/plot_data/`

- **TASK-10 — Use extraction plus crude transportation for upstream crude LCA**
  - Removed crude-specific upstream overrides.
  - Standardized upstream climate impacts on a single emissions basis.

- **TASK-11 — Add detailed LCA waterfall plots by life-cycle stage and unit utilities**
  - Produced stage-by-stage waterfall plots with contributor stacks for Mars 100 kBPD scenarios.
  - **Relevant outputs**
    - `outputs/plot_data/mars_100k_lca_waterfalls.csv`
    - PNG waterfall plots under `outputs/plots/mars_100k_lca_waterfalls/`

- **TASK-12 — Add API-sulfur proxy-arrow crude plot**
  - Created a visual map from each crude assay to its assigned price proxy.
  - Exported the joined arrow-plot data.
  - **Which code does this**
    - `refinery_process_model/plotting/plot_api_sulfur_crude_price_proxies.py`
  - **Where the files are**
    - plot image: `outputs/plots/api_sulfur_crude_price_proxies.png`
    - exported joined plot values: `outputs/plots/api_sulfur_crude_price_proxies_values.csv`
  - **What the image shows**
    - x-axis: sulfur content (`wt%`, log scale)
    - y-axis: API gravity (`°API`)
    - one point per crude assay, colored by region
    - arrows drawn from a target crude to the crude chosen as its price proxy
    - direct-priced crudes remain visible as points without arrows
  - The image is intended as a visual QA check of the proxy assignments, so you can quickly see whether each target crude is being mapped to a nearby crude in API–sulfur space.

- **TASK-13 — Add Mars 100 kBPD equipment cost breakdown bar graph**
  - Added a repo-native stacked equipment-cost comparison for the 8 Mars 100 kBPD wind configurations.
  - Built the figure from saved batch results plus scenario workbooks only, without rerunning the process model inside the plotting script.
  - **Relevant outputs**
    - `outputs/plot_data/mars_100k_configuration_equipment_cost_breakdown.csv`
    - `outputs/plots/mars_100k_configuration_equipment_cost_breakdown.png`
    - `outputs/plots/mars_100k_configuration_equipment_cost_breakdown.pdf`

- **TASK-14 — Expose detailed hydrotreatment equipment costs in saved outputs**
  - Saved explicit hydrotreatment purchase-equipment components for atmospheric distillation, vacuum distillation, hydrotreator, amine gas treating, Claus sulfur recovery, hydrogen production, and distillation/treatment utility systems.
  - Updated scenario workbooks and flattened batch-result columns so downstream plots can use real unit-level equipment categories.
  - Removed the implied residual hydrotreatment bucket from the Mars equipment-breakdown plotting workflow.
  - **Relevant outputs**
    - refreshed Mars 100 kBPD wind rows in `outputs/batch_aromatics_scenarios.csv`
    - hydrotreatment workbook `Equipment Costs` sheets in `outputs/scenario_runs/batch_workbooks/`
    - refreshed `outputs/plot_data/mars_100k_configuration_equipment_cost_breakdown.csv`

- **TASK-15 — Add annual operating-cost breakdown plot by configuration**
  - Added a repo-native annual operating-cost breakdown comparison for the same 8 Mars 100 kBPD configurations.
  - Extended workbook `Utilities` sheets so hydrotreatment cases expose Distillation, Hydrotreatment, Sulfur recovery, and Hydrogen production sections, while solvent cases expose Distillation and Solvent extraction sections.
  - Mapped saved annual costs into scenario-aware categories such as crude input, distillation NG, hydrotreator power, SMR feed gas, electrolysis power, solvent extraction power, and solvent makeup, then reconciled them to total annual operating cost.
  - **Relevant outputs**
    - `outputs/plot_data/mars_100k_configuration_operating_cost_breakdown.csv`
    - `outputs/plots/mars_100k_configuration_operating_cost_breakdown.png`
    - `outputs/plots/mars_100k_configuration_operating_cost_breakdown.pdf`

- **TASK-16 — Add annual utilities-cost breakdown plot by configuration**
  - Added a repo-native annual utilities-cost breakdown comparison using saved workbook `Utilities` sheets only.
  - Broke utility costs into scenario-aware categories across distillation, hydrotreatment, sulfur recovery, hydrogen production, and solvent extraction where applicable.
  - Reconciled plotted category totals to the summed saved utility annual-cost rows for each configuration.
  - **Relevant outputs**
    - `outputs/plot_data/mars_100k_configuration_utilities_cost_breakdown.csv`
    - `outputs/plots/mars_100k_configuration_utilities_cost_breakdown.png`
    - `outputs/plots/mars_100k_configuration_utilities_cost_breakdown.pdf`

- **TASK-17 — Add kerosene property-change figures across treatment pathways**
  - Added a repo-native plotting workflow for paired baseline-versus-treated kerosene property comparisons across Mars, Oman, and Murban.
  - Built three publication-style figures covering energy properties, composition changes, and sulfur changes for mild hydrotreatment, severe hydrotreatment, and solvent extraction.
  - Used explicit total aromatics in the composition figure and a log sulfur axis in the sulfur figure to keep large reductions readable.
  - **Relevant outputs**
    - `outputs/plot_data/kerosene_property_changes_energy.csv`
    - `outputs/plot_data/kerosene_property_changes_composition.csv`
    - `outputs/plot_data/kerosene_property_changes_sulfur.csv`
    - `outputs/plots/kerosene_property_changes_energy.png`
    - `outputs/plots/kerosene_property_changes_energy.pdf`
    - `outputs/plots/kerosene_property_changes_composition.png`
    - `outputs/plots/kerosene_property_changes_composition.pdf`
    - `outputs/plots/kerosene_property_changes_sulfur.png`
    - `outputs/plots/kerosene_property_changes_sulfur.pdf`

- **TASK-18 — Plot global crude prices against API gravity, sulfur, and region**
  - Added a repo-native plotting workflow for the full crude dataset that joins assay attributes to the updated crude price table.
  - Created a price-colored API-vs-sulfur figure that uses marker shape to distinguish region and a colorbar to show crude price in USD/bbl.
  - Added directional annotations so the plot explicitly shows sweet/sour and light/heavy directions.
  - Added regression coverage for join behavior, including downstream-key joins plus assay-slug and crude-name fallback logic for mismatched keys.
  - **Which code does this**
    - `refinery_process_model/plotting/plot_api_sulfur_crude_prices.py`
    - shared directional-annotation helper in `refinery_process_model/plotting/plot_api_sulfur_crude_assays.py`
  - **Where the files are**
    - plot image: `outputs/plots/api_sulfur_crude_prices.png`
    - exported joined plot values: `outputs/plots/api_sulfur_crude_prices_values.csv`
    - regression test: `refinery_process_model/tests/test_plot_api_sulfur_crude_prices.py`
  - **What the image shows**
    - x-axis: sulfur content (`wt%`, log scale)
    - y-axis: API gravity (`°API`)
    - one point per crude assay
    - marker color: crude price (`USD/bbl`)
    - marker shape: region
    - directional arrows labeled `sweet`, `sour`, `light`, and `heavy`


- **TASK-19 — Estimate initial and final fuel seal swell from aromatic content**
  - Added a repo-native plotting workflow that estimates initial and final nitrile-rubber seal swell from aromatic content using the Graham et al. (2011) correlation.
  - Reused the Mars, Oman, and Murban pathway comparison slice to build a publication-style paired before/after figure across mild hydrotreatment, severe hydrotreatment, and solvent extraction.
  - Included the 8.7-23.1% aromatics applicability note in both the figure and exported plot data.
  - **Relevant outputs**
    - `outputs/plot_data/fuel_seal_swell_changes.csv`
    - `outputs/plots/fuel_seal_swell_changes.png`
    - `outputs/plots/fuel_seal_swell_changes.pdf`

- **TASK-20 — Map weighted-average refinery premium by country**
  - Added a country-level premium-mapping workflow that aggregates refinery premiums with `latest_capacity_kbd` as the weighting basis.
  - Built treatment-specific choropleth maps for severe hydrotreatment, mild hydrotreatment, and solvent extraction, with a fixed color-bar cap and treatment label in the title.
  - Added country canonicalization, ISO mapping, and audit fields such as refinery count used and total capacity used.
  - **Relevant outputs**
    - `outputs/plots/mild_hydrotreatment_avg_premium_country_map.html`
    - `outputs/plots/mild_hydrotreatment_avg_premium_country_map_values.csv`
    - `outputs/plots/severe_hydrotreatment_avg_premium_country_map.html`
    - `outputs/plots/severe_hydrotreatment_avg_premium_country_map_values.csv`
    - `outputs/plots/solvent_extraction_avg_premium_country_map.html`
    - `outputs/plots/solvent_extraction_avg_premium_country_map_values.csv`

- **TASK-21 — Add Mars 100 kBPD local premium sensitivity analysis with tornado and spider plots**
  - Added a repo-native local sensitivity workflow for the exact 8 Mars 100 kBPD wind / US Gulf Coast / near-term configurations using saved batch results plus saved `DCFROR Inputs` workbook sheets only.
  - Reran only the DCF seam for one-at-a-time ±5% perturbations of the selected numeric DCF inputs, excluding `FCIDet` from the plotted sweep while keeping it in the parsed DCF record.
  - Produced multi-panel tornado and spider plots using premium midpoint as the displayed sensitivity metric and added publication-friendly labels such as `VOC (Non-utilities Variable Operating Cost)` and flow-rate wording for product outputs.
  - **Relevant outputs**
    - `outputs/plot_data/mars_100k_configuration_premium_sensitivity_detail.csv`
    - `outputs/plot_data/mars_100k_configuration_premium_sensitivity_summary.csv`
    - `outputs/plots/mars_100k_configuration_premium_sensitivity_tornado.png`
    - `outputs/plots/mars_100k_configuration_premium_sensitivity_tornado.pdf`
    - `outputs/plots/mars_100k_configuration_premium_sensitivity_spider.png`
    - `outputs/plots/mars_100k_configuration_premium_sensitivity_spider.pdf`

- **TASK-22 — Wire actual distillation cooling water into SR DCFROR inputs**
  - Replaced the hard-coded zero in the untreated/SR DCF argument list with the real distillation cooling water quantity.
  - Brought `SR Min` and `SR Max` on the workbook `DCFROR Inputs` sheet into line with the actual distillation utilities used elsewhere in the model.
  - Added focused regression coverage for both the DCF arg mapping and the generated workbook sheet.
  - **Relevant outputs**
    - refreshed scenario workbooks under `outputs/scenario_runs/batch_workbooks/`
    - refreshed batch CSV outputs under `outputs/` after rerunning the batch scenario workflow


## Manual checking to old Aromatics project

- Compared the regenerated scenario output workbooks against the older Aromatics-project workbooks to understand why costs diverged.
- Found that the old run was missing steam-system and cooling-water-system equipment costs from TPEC, which in turn understated FCI.
- Updated the crude price data so the refinery economics use a more accurate crude-cost basis.
- Corrected vacuum-distillation energy scaling so utility requirements are based on vacuum-distillation throughput rather than total crude throughput; the old basis had inflated vacuum energy requirements.
- In the legacy Aromatics project, the solvent-extraction DCF appears to assign the upper-bound BTX price to the   max-premium case. That is directionally inconsistent, because increasing BTX price lowers net premium. The upper-bound BTX price should instead be used in the min-premium case, while the lower-bound BTX price should be used in the   max-premium case.

## Notes

- **Current workbook location**
  - `outputs/scenario_runs/batch_workbooks`

- **Archived workbook location**
  - `outputs/batch_workbooks` was archived on 2026-07-16.

- **Tracking**
  - Active and future work should continue to be tracked in Backlog tasks.
