---
id: TASK-2.1
title: Inventory source datasets and define canonical schemas
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:42'
updated_date: '2026-07-08 15:03'
labels: []
dependencies: []
references:
  - CONTEXT.md
modified_files:
  - data_inventory_v1.md
parent_task_id: TASK-2
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Inventory the source workbooks and scripts referenced in CONTEXT.md, identify the exact input files needed for v1, and define canonical schemas for BP crude data, refinery data, and country flow inputs. This task establishes the data contract for later extraction and scoring tasks.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A documented inventory lists each v1 source file, its role, and the required tabs/fields
- [x] #2 Canonical schemas are defined for BP crude, refinery, and country flow inputs with field names, types, and key identifiers
- [x] #3 Known data gaps, ambiguous columns, and normalization risks are recorded for downstream tasks
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect CONTEXT.md, referenced scripts, and candidate source workbooks to identify the exact v1 inputs.
2. Extract workbook sheet names and representative columns for BP crude, refinery, domestic crude refined, and trade data sources.
3. Write a project document that inventories the v1 source files, defines canonical schemas, and records known ambiguities/normalization risks.
4. Append progress notes and keep the task updated as the inventory is completed.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Read `CONTEXT.md`, inspected referenced workbooks/scripts, and confirmed the next dependency-ordered task is TASK-2.1.
- Created `data_inventory_v1.md` with a v1 source inventory, canonical schemas for BP crude/refinery/country-flow inputs, extraction rules, and normalization risks.
- Confirmed current source structure: 35 BP assay workbooks, refinery master workbook header at Excel row 12, domestic crude workbook requires `DOMCRREF_CALC` + unit/month aggregation, and trade workbook requires `Import` + `cmdCode=2709` filtering with `W00` total-row handling.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented the v1 source inventory in `data_inventory_v1.md`, including required source files/sheets, canonical schemas for BP crude/refinery/country-flow inputs, and key normalization risks. Verified by inspecting the referenced workbooks and scripts directly.
<!-- SECTION:FINAL_SUMMARY:END -->
