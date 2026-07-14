---
id: TASK-3.3
title: Document supported repository workflows and add cleanup regression checks
status: To Do
assignee: []
created_date: '2026-07-09 14:35'
updated_date: '2026-07-09 14:45'
labels: []
dependencies:
  - TASK-3.1
  - TASK-3.2
  - TASK-3.4
references:
  - CONTEXT.md
parent_task_id: TASK-3
priority: medium
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Write concise developer documentation for the canonical workflow families across the repository and run a focused validation pass so cleanup work is proven not to break intended outputs. Documentation should explain the final repository layout, including the intended roles of refinery_process_model/, cost_benefit_analysis/, and nvpm_correlations/.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Documentation explains the canonical workflow families, major modules, and regeneration commands for key artifacts across the project
- [ ] #2 Focused tests or smoke checks cover the most fragile cleanup-sensitive paths across the repository
- [ ] #3 Validation results are recorded, including any intentional output differences or remaining known limitations
- [ ] #4 Documentation explains the final repository layout and the intended roles of refinery_process_model/, cost_benefit_analysis/, nvpm_correlations/, and any shared/supporting areas
<!-- AC:END -->
