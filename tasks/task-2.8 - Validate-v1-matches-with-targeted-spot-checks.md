---
id: TASK-2.8
title: Validate v1 matches with targeted spot checks
status: Done
assignee:
  - '@pi'
created_date: '2026-07-08 13:43'
updated_date: '2026-07-08 17:40'
labels: []
dependencies:
  - TASK-2.7
references:
  - CONTEXT.md
parent_task_id: TASK-2
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Perform the v1 validation pass described in CONTEXT.md using a small set of refineries with known or strongly expected crude relationships. Document where the heuristic behaves plausibly, where it fails, and what should be calibrated next.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A spot-check set is chosen and the expected refinery-crude relationships are stated
- [x] #2 Validation results record whether top-ranked BP crudes are technically and regionally plausible
- [x] #3 Observed failure modes and candidate threshold/weight adjustments are documented for follow-up work
- [x] #4 Validation output explicitly states that v1 is heuristic inference rather than observed intake truth
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review the generated v1 matches and choose a small spot-check set with known or strongly expected regional crude relationships.
2. Compare the top-ranked matches against technical fit and regional plausibility for each selected refinery, noting both successes and weak points.
3. Write a validation document summarizing the spot-check set, expected relationships, results, failure modes, and candidate calibration follow-ups, while explicitly framing v1 as heuristic inference.
4. Update the backlog task with notes/final summary and mark it done if the validation output is complete.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Reviewed generated `refinery_crude_matches_v1.csv`, `refinery_crude_scores_v1.csv`, and country sourcing outputs to choose a targeted spot-check set spanning North Sea, Atlantic-import, Gulf hydroskimming, Gulf condensate-splitter, and Gulf coking cases.
- Created validation document `doc-2` at `backlog/docs/validation/doc-2 - V1-refinery-to-crude-matching-spot-check-validation.md`.
- Spot checks covered Mongstad, Pembroke, Rotterdam I, Mina Al Fahal, Abu Dhabi II, Ras Tanura, and Sohar I.
- Documented both plausible behavior and failure modes, especially missing/weak Oman and UAE sourcing priors, underweighted geography in Gulf cases, and candidate-universe gaps for Saudi/Kuwaiti/UAE grades.
- Validation document explicitly states that v1 remains heuristic inference rather than observed intake truth.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed the v1 targeted spot-check validation pass and documented it in `doc-2`. The review found strong behavior for North Sea cases, acceptable behavior for some Atlantic import systems, and clear Gulf failure modes tied to weak country priors, underweighted geography, and candidate-universe gaps. The document also states explicitly that v1 is heuristic inference, not observed refinery intake truth.
<!-- SECTION:FINAL_SUMMARY:END -->
