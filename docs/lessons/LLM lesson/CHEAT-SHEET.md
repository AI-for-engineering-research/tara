# LLM Cheat Sheet

## Core model
- An LLM is a **next-token predictor**.
- It reads the current **token** sequence.
- It produces **logits** over possible next tokens.
- **Softmax** turns logits into probabilities.
- A **decoding strategy** picks the next token.
- The token is appended and the loop repeats.

## Tokens
- Models operate on **tokens**, not words.
- Tokenization affects:
  - context window usage
  - cost
  - generation behavior

## Representations
- Tokens become **embeddings**: learned vectors.
- **Positional information** is added so order matters.

## Attention
- **Attention** lets a token use other tokens in context.
- **Query**: what this token is looking for.
- **Key**: how another token is matched.
- **Value**: what information that token contributes.
- **Masking** decides which tokens are allowed.
- In **causal** generation, tokens can only attend to earlier tokens.
- **Multi-head attention** lets the model track different relevance patterns in parallel.

## Layers
Each transformer layer roughly does:
1. self-attention
2. per-token MLP / feed-forward computation
3. residual update

Residual idea:
- new representation = old representation + learned adjustment

## Training vs inference
- **Training**: weights change to improve next-token prediction.
- **Inference**: weights stay fixed; the model just runs the forward pass.
- In chat, the model usually uses **context adaptation**, not live training.

## Sampling
- **Greedy**: pick highest-probability token.
- **Sampling**: choose from the distribution.
- **Lower temperature**: more concentrated, more predictable.
- **Higher temperature**: flatter, more varied.

## Hallucinations
- Hallucinations are usually **plausible but false continuations**.
- The model is optimized for likely continuation, not guaranteed truth.
- Weak or ambiguous context increases hallucination risk.

## Grounding
Grounding gives the model external evidence:
- documents
- tools
- databases
- source passages

Grounding helps because it constrains next-token prediction with real context.

## Practical levers
If output is bad, improve one or more of:
- **context**: clearer prompt, examples, grounding, structure
- **selection**: temperature / decoding strategy
- **verification**: tests, source checks, tools, human review

## Practical defaults
- If accuracy matters: ground + lower temperature + verify.
- If output is vague: add constraints and format.
- If output is inconsistent: make prompt explicit and reduce temperature.
- If output is too rigid: loosen constraints or raise temperature slightly.
