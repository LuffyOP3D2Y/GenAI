# Day 2 -- Attention & System Design 

## Block 1 Goal: Understand why transformers replaced sequential models

### Question 1: What was the fundamental bottleneck of RNNs/LSTMs? RNNs and LSTMs were fundamentally bottlenecked by forced sequential computation. Because each token depended on the previous hidden state, tokens could not be processed in parallel and long-range dependencies degraded over distance. Scale alone could not overcome this architectural limitation.

### Question 2: Why was sequential processing a hard limit? Sequential processing constrained both information flow and training economics. Long-range dependencies had to be compressed into a single hidden state, making contextual reasoning over long sequences unreliable and inefficient.

### Question 3: What did attention make possible? Attention enabled every token to directly access relevant information from all other tokens in the sequence in parallel, without compressing context into a single representation.

## Block 2 Goal: Build intuition for Query, Key, Value and attention costs

### Question 1: What does a Query represent? A Query represents what information a token is looking for from the rest of the sequence to disambiguate its meaning in context.

### Question 2: What does a Key represent? A Key represents what information a token contains and how relevant that information is for satisfying another token's Query.

### Question 3: What does a Value represent? A Value represents the actual information that gets aggregated once relevance is established, updating a token's embedding to reflect contextual meaning.

### Question 4: Why is attention quadratic? Self-attention scales quadratically because every token must compare itself with every other token to compute relevance. Reducing these interactions necessarily trades off contextual fidelity.

Executive One-liner:\
Long context isn't free --- it's a quadratic tax on relevance.

## Block 3 Goal: Translate attention limits into real system architecture decisions

### Question 1: Why does RAG exist? RAG exists because attention and context windows are limited and expensive. Instead of expanding the model or context indefinitely, systems retrieve a small, relevant subset of external information and inject it into the prompt.

RAG exists because attention is scarce, not because models are dumb.

### Question 2: What failure modes does RAG introduce? RAG introduces data quality failures, retrieval relevance errors, over-retrieval that dilutes attention, privacy and security risks, and evaluation opacity due to embedding-based retrieval.

RAG doesn't remove hallucinations --- it replaces them with retrieval
errors.

### Question 3: Why do agent-based systems emerge naturally? Agent-based systems emerge because attention-based models cannot efficiently reason over large, multi-step tasks within a single context window. Decomposing tasks into specialized agents limits attention scope, reduces interference, and improves controllability and system reliability.

Agents exist because attention doesn't scale with ambition.

### Question 4: What common mistake do teams make when scaling LLM systems? Teams often treat LLMs as general-purpose decision-makers rather than probabilistic components optimized for narrow tasks. This leads to oversized prompts, diluted attention, and missing fallbacks, causing small errors to propagate into large system failures.

Most LLM failures at scale come from giving the model responsibility
instead of constraints.
