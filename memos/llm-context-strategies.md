# Context Strategies for LLM Systems

### Trimming, Summarization, and Retrieval (RAG)

## 1. Executive Summary

This memo analyzes three context-management strategies for Large
Language Model (LLM) systems operating over policy documents with
internal contradictions:

- **Strategy A: Context Trimming**

- **Strategy B: Context Summarization**

- **Strategy C: Retrieval-Augmented Generation (RAG)**

The goal is not to optimize answer quality, but to understand **how
different context strategies shift system risk, confidence, and
observability** under realistic failure conditions.

The central finding is that context strategies do not merely affect
*what* a model answers --- they materially change *how* failures
manifest:

- Trimming reduces hallucination surface area but increases ambiguous or
  silent failure.

- Summarization introduces cascading risk when weak summaries become the
  sole grounding source.

- RAG improves apparent grounding but creates the most dangerous failure
  mode: **confident, policy-like answers based on incorrect or
  irrelevant context**.

These tradeoffs are structural and persist regardless of model scale.

## 2. Common System Setup

All strategies were evaluated under a fixed system contract to isolate
the effect of context handling:

### 2.1 Prompt Contract (Fixed)

All prompts followed a deterministic scaffold:

- **Instruction** (authoritative scope)

- **Context** (optional, untrusted)

- **Question**

- **Terminal directive:**\
  *"Answer carefully and only within the instruction scope."*

This contract makes context strategy the primary independent variable.

### 2.2 Test Document Characteristics

The policy document intentionally contained:

- Partial coverage of enforcement rules

- Legal boilerplate

- Internal ambiguities and contradictions

This mirrors real enterprise policy surfaces rather than idealized
documentation.

## 3. Strategy A --- Context Trimming

### 3.1 Description

A contiguous subset of the policy document (e.g., billing and payment
sections) was selected and passed directly to the model. Truncation
boundaries were intentionally imperfect to stress attention and
grounding limits.

### 3.2 Observed Behaviour

Across runs, the model frequently produced:

- Repetition of instruction fragments or terminal directives

- Short, degenerate continuations resembling refusal but lacking an
  explicit abstention signal

- Occasional early termination (empty output)

### 3.3 Strategic Insight

Context trimming reduces exposure to irrelevant or contradictory
information, but when grounding is insufficient the model does not
reliably abstain. Instead, it often **echoes the prompt or collapses
into low-information output**.

### 3.4 System Implication

Trimming alone does not guarantee safe failure. Without explicit
abstention logic, it replaces hallucination with **opacity**, which is
difficult to detect and automate against in production systems.

## 4. Strategy B --- Context Summarization

### 4.1 Description

The full policy document was first summarized by the model. The
resulting summary was then used as the sole context for answering
downstream questions.

### 4.2 Observed Behaviour

Observed outcomes included:

- Empty or near-empty generations (early EOS)

- Noisy summaries leaking prompt scaffolding

- Downstream answers weakly aligned with original policy semantics

### 4.3 Strategic Insight

When the same model is used for both summarization and answering, errors
compound. A weak summary collapses the model's continuation space,
making silence, repetition, or low-entropy outputs the most likely
result.

### 4.4 System Implication

Summarization introduces a **single point of semantic failure**. If the
summary is wrong or lossy, downstream answers inherit that error with
reduced observability. This strategy is only viable when summarization
quality is demonstrably strong and independently validated.

## 5. Strategy C --- Retrieval-Augmented Generation (RAG)

### 5.1 Description

A deliberately naive retriever split the policy into chunks and ranked
them using token overlap scoring. Both **top-k (most relevant)** and
**bottom-k (least relevant)** chunks were injected into the prompt to
expose contrastive failure modes.

### 5.2 Observed Behaviour --- Relevant Retrieval

When relevant but incomplete chunks were retrieved:

- Outputs sounded policy-compliant and confident

- Answers closely mirrored retrieved text with minimal synthesis

- Some degeneration appeared at sequence boundaries

### 5.3 Observed Behaviour --- Irrelevant Retrieval

When irrelevant chunks were retrieved:

- Outputs often entered repetition loops or echoed the question

- Tone remained confident despite lack of support

- Failures appeared "formal" rather than obviously incorrect

### 5.4 Strategic Insight

RAG shifts failure from **ignorance to overconfidence**. The model
treats retrieved text as authoritative continuation. When retrieval
quality degrades, hallucination becomes structured, fluent, and
difficult to detect.

### 5.5 System Implication

RAG systems are only as safe as their retrieval layer. Without strong
retrieval quality, reranking, and abstention enforcement, RAG produces
failures that are more dangerous than base-model hallucination.

## 6. Synthesis: Comparative Tradeoffs

Across all strategies, failures were systematic rather than random. The
table below summarizes the observed tradeoffs:

  --------------------------------------------------------------------------------
  **Dimension**              **Trimming**   **Summarization**   **RAG**
  -------------------------- -------------- ------------------- ------------------
  Hallucination risk         Low            Medium              High (if retrieval
                                                                weak)

  Confidence of failure      Low            Low--Medium         High

  Observability              Medium         Low                 Low

  Latency                    Low            Medium              High

  Suitability for            Moderate       Moderate            High (with
  policy/compliance                                             controls)

  Debuggability              High           Medium              Low

  Dependency on upstream     Low            Medium              Very High
  quality                                                       
  --------------------------------------------------------------------------------

**Key pattern:**\
As systems move from trimming → summarization → RAG, they trade reduced
hallucination probability for **increased confidence in failure and
reduced observability**.

## 7. Strategic Recommendations

- Prefer **explicit abstention contracts** regardless of context
  strategy.

- Treat all context --- retrieved or summarized --- as potentially
  adversarial.

- Use RAG only with:

  - Strong retrievers and rerankers

  - Aggressive context hygiene

  - Post-generation validation

- Preserve raw prompts, retrieved chunks, and outputs as first-class
  operational artefacts.

A system that occasionally refuses to answer is safer and more auditable
than one that confidently fabricates.

## 8. Model Choice and Limitations

All experiments were conducted using **DistilGPT-2**, a lightweight,
non-instruction-tuned causal language model with known limitations:

- Susceptibility to repetition and degeneration

- Weak instruction adherence

- No native abstention behavior

This choice was intentional. Primitive models surface failure modes
earlier and more clearly, removing the illusion of robustness created by
larger, instruction-tuned systems. While output quality will improve
with stronger models, the **structural failure patterns documented here
are expected to persist unless explicitly addressed at the system
level**.
