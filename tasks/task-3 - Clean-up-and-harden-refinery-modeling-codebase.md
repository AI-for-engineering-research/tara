---
id: TASK-3
title: Clean up and harden the Aromatics_removal_desulfurization_refining codebase
status: To Do
assignee: []
created_date: '2026-07-09 14:34'
updated_date: '2026-07-09 14:45'
labels: []
dependencies: []
references:
  - CONTEXT.md
priority: medium
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Improve maintainability of the entire Aromatics_removal_desulfurization_refining repository, not only the refinery/crude matching workflow. Focus on clarifying module boundaries across modeling, analysis, plotting, data-preparation, and workflow scripts; reducing ad hoc or duplicated logic; organizing legacy/generated artifacts; and making the codebase easier to understand, rerun, validate, and extend without changing scientific intent. Target a clearer top-level structure centered on repository areas such as refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/, with supporting shared/docs/tests/legacy areas where needed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Core workflows across the repository are organized behind clearer entrypoints with duplicated or ad hoc logic reduced
- [ ] #2 Obsolete, superseded, or confusing code paths/files across the repository are identified and either removed or explicitly documented as legacy
- [ ] #3 Documentation explains the supported workflow families, major modules, and regeneration steps for important outputs across the project
- [ ] #4 A focused validation pass confirms cleanup changes do not alter intended outputs beyond documented fixes
<!-- AC:END -->
