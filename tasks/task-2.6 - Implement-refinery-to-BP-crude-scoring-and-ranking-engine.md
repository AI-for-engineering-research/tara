---
id: TASK-2.6
title: Implement refinery-to-BP-crude scoring and ranking engine
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-08 15:29'
labels: []
dependencies:
  - TASK-2.2
  - TASK-2.3
  - TASK-2.4
  - TASK-2.5
references:
  - CONTEXT.md
modified_files:
  - refinery_process_model/build_refinery_bp_crude_matches.py
  - refinery_process_model/input_text_files/refinery_matching_v1.toml
  - tests/refinery_process_model/test_build_refinery_bp_crude_matches.py
parent_task_id: TASK-2
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the v1 hybrid matcher that applies hard filters first and then ranks technically plausible BP crudes using technical fit plus country sourcing as a plausibility modifier.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The engine evaluates every refinery against every BP crude and records hard-filter pass/fail state
- [x] #2 Soft scoring incorporates refinery type/class, NCI, API, sulfur, and country sourcing context
- [x] #3 The output returns up to top 3 plausible BP crude matches per refinery without forcing 3 matches when fewer are plausible
- [x] #4 Per-match rationale fields and coverage notes are generated for downstream workbook output
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect the normalized BP crude/refinery/country-prior outputs, matching config, and any legacy match artifacts to define the v1 score table and top-match output shape.
2. Implement a reusable matching engine that evaluates every refinery × BP crude pair, applies config-driven hard filters, computes soft-score components, and records rationale fields.
3. Emit reproducible CSV outputs for the full score table and the top matches table with up-to-3 ranked matches, `match_count`, and coverage notes.
4. Add focused tests for pair-count coverage, hard-filter recording, top-3 behavior, country-sourcing integration, and rationale generation; then run the relevant test subset and generate the artifacts.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added `refinery_process_model/build_refinery_bp_crude_matches.py` to evaluate all refinery × BP crude pairs, apply config-driven hard filters, compute soft-score components, and build up-to-top-3 refinery match outputs.
- Extended `refinery_process_model/input_text_files/refinery_matching_v1.toml` with provisional capability envelopes, ideal points, and hard-filter starter margins so the matcher can execute from external config rather than hard-coded Excel rules.
- The score table records hard-filter pass/fail state, component scores for refinery type, API, sulfur, NCI, country sourcing, geography, and crude production signal, plus fail reasons.
- The match summary output provides one row per refinery with `match_count`, `coverage_note`, top-3 crude names/scores, and per-rank rationale text for workbook integration.
- Added `tests/refinery_process_model/test_build_refinery_bp_crude_matches.py`; verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_matching_config.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py` (8 passed).
- Generated outputs under `refinery_process_model/outputs/`: `refinery_bp_crude_scores_v1.csv` and `refinery_bp_crude_matches_v1.csv`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented `refinery_process_model/build_refinery_bp_crude_matches.py` to score all 822 × 35 refinery–BP crude pairs, apply hard filters, and generate top-match outputs with rationale text. The matcher now uses external config from `refinery_matching_v1.toml`, records per-pair hard-filter state and score components, and writes reproducible `refinery_bp_crude_scores_v1.csv` and `refinery_bp_crude_matches_v1.csv` outputs. Verified with `./venv/bin/python -m pytest tests/refinery_process_model/test_matching_config.py tests/refinery_process_model/test_build_refinery_bp_crude_matches.py`.
<!-- SECTION:FINAL_SUMMARY:END -->
