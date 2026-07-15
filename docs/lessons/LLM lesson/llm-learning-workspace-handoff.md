# Handoff: LLM learning workspace

## Purpose of next session
Continue the interactive teaching sequence on how LLMs work, with the next lesson focused on self-attention internals: queries, keys, and values.

## What happened
- Created a new teaching workspace for LLM learning at `llm-learning-workspace/`.
- Set mission to: understand transformers deeply and use LLMs effectively, starting from only basic prior knowledge.
- Created initial workspace files:
  - `llm-learning-workspace/MISSION.md`
  - `llm-learning-workspace/RESOURCES.md`
  - `llm-learning-workspace/NOTES.md`
- Created first lesson/reference artifacts:
  - `llm-learning-workspace/lessons/0001-an-llm-is-a-next-token-machine.html`
  - `llm-learning-workspace/reference/0001-llm-core-loop.html`
- Taught interactively in-chat beyond the HTML lesson sequence.

## Learning established
See learning records:
- `llm-learning-workspace/learning-records/0001-mission-and-basic-starting-point.md`
- `llm-learning-workspace/learning-records/0002-can-explain-next-token-prediction-and-why-prompting-works.md`
- `llm-learning-workspace/learning-records/0003-can-distinguish-training-vs-inference-and-understands-tokens.md`
- `llm-learning-workspace/learning-records/0004-understands-positional-information-and-attention-as-relevance.md`

In plain terms, the learner can now:
- Explain LLM generation as repeated next-token prediction over current context.
- Distinguish why prompting works from why sampling causes output variation.
- Explain that next-token distributions are computed at inference time from current context using learned weights.
- Distinguish training on large text corpora from inference.
- Explain what tokens are and why tokens matter more than words for cost/context/generation.
- Explain embeddings as learned vector representations, not mere labels.
- Explain why positional information is needed in transformers.
- Explain attention as a relevance-weighting mechanism over context.
- Explain that contextual information helps disambiguate token meaning.

## Open teaching thread
The learner asked:
- “lesson 5. and how many more lessons do you think we should do?”
- After Lesson 0005, they asked to pause and export the conversation.

Recommended next lesson:
- Lesson 0006: self-attention — queries, keys, and values.

Suggested roadmap already discussed:
- 0006 self-attention: queries, keys, values
- 0007 multi-head attention
- 0008 layers and residual structure
- 0009 training vs inference in more detail
- 0010 logits, softmax, sampling, temperature
- 0011 hallucinations
- 0012 practical LLM use from the mechanism-level model

## Gaps / follow-up work
- `llm-learning-workspace/RESOURCES.md` is still mostly empty. Future formal lessons should be grounded in curated high-trust sources.
- Interactive teaching progressed faster than the saved HTML lessons; only lesson 0001/reference 0001 exist as files so far.
- If continuing the teaching workspace formally, create:
  - lesson 0002+ HTML files
  - matching reference docs
  - possibly learning records for future demonstrated understanding

## User preferences / constraints
From workspace notes and conversation:
- Wants deep understanding of transformers.
- Also wants practical ability to use LLMs effectively.
- Starts from basic prior knowledge.
- Interactive teaching style is working well.
- Short incremental lessons with checks are appropriate.

## Suggested skills
- `teach` — continue the stateful teaching workflow in `llm-learning-workspace/`
- `handoff` — if another export/update is needed later

## Export location
This handoff file is now stored at:
- `docs/lessons/LLM lesson/llm-learning-workspace-handoff.md`
