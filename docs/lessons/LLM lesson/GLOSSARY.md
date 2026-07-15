# LLM Glossary

## Attention
Mechanism that lets a token use information from other allowed tokens in the sequence.

## Causal mask
Rule in GPT-style generation that prevents a token from attending to later tokens.

## Context
The current token sequence the model conditions on.

## Context adaptation
Temporary behavior change caused by the current prompt or conversation, without changing weights.

## Context window
Maximum amount of token context the model can use at once.

## Decoding
The method used to choose a token from the model's probability distribution.

## Embedding
A learned vector representation of a token.

## Feed-forward block / MLP
Per-token computation applied after attention inside a transformer layer.

## Grounding
Supplying external evidence so the model answers from specific source material, not weights alone.

## Hallucination
A plausible-sounding but false or unsupported continuation.

## Inference
Using fixed weights to compute outputs.

## Key
Part of attention used to determine whether a token matches another token's query.

## Logit
A raw score for a candidate next token before probabilities are computed.

## Multi-head attention
Using several attention heads in parallel so the model can track different kinds of relevance at once.

## Next-token prediction
The core training and generation objective: predict what token should come next.

## Positional information
Signals added so the model knows token order.

## Probability distribution
The model's assigned probabilities over candidate next tokens.

## Query
Part of attention representing what a token is looking for in context.

## Residual connection
A skip path that adds the earlier representation back to a block's output.

## Sampling
Choosing a token stochastically from the probability distribution.

## Self-attention
Attention among tokens in the same sequence.

## Softmax
Function that turns logits into probabilities that sum to 1.

## Temperature
A decoding control that makes the probability distribution sharper or flatter.

## Token
A text chunk used by the model's tokenizer; not necessarily a whole word.

## Tokenizer
The system that splits text into tokens and maps them to IDs.

## Training
The process of updating weights to improve prediction.

## Transformer layer
A repeated block containing attention, MLP computation, and residual structure.

## Value
Part of attention representing the information a token contributes if attended to.

## Weights
The learned parameters of the model.
