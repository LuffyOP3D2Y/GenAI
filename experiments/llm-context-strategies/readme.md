**Context Strategies --- README**

**Purpose**

This folder contains an investigation of three context-management
strategies for LLM-based question answering over policy documents:
**Trimming**, **Summarization**, and **Retrieval-Augmented Generation
(RAG)**.

The objective is to surface **structural failure modes and operational
tradeoffs**---such as confidence, observability, and risk---rather than
to optimize for answer quality or benchmark models.

**What's included**

- context_strategies.py --- experiment harness (retriever, prompt
  builders, experiment runner).

- llm_builder.py --- model initialization and generation helpers
  (tokenizer, model load, prompt construction, trimming and
  summarization helpers).

- /notes/ (expected) --- raw inputs and verbatim outputs (prompts,
  retrieved chunks, model responses).

- /memos/ (expected) --- human-facing memos derived from experiments.

The code in this directory is intentionally minimal and diagnostic in
nature. It is designed for visibility and reasoning, not production
deployment.

**Quick overview of the experimental flow**

**1. Base run (baseline)**

The model is run with empty or minimal context to establish baseline
behavior for the same question.

**2. Strategy A --- Context Trimming**

A contiguous subset of the policy document (for example, a billing or
payment section) is passed as context.

Observed behaviors include instruction echoing, premature termination,
or refusal-like degeneration rather than structured abstention.

**3. Strategy B --- Summarization**

The policy document is summarized and the resulting summary is passed as
context.

This tests whether global abstraction improves grounding or instead
introduces new failure modes such as loss of critical details or empty
outputs due to early EOS behavior.

**4. Strategy C --- Retrieval-Augmented Generation (RAG)**

A deliberately naive retriever scores document chunks using token
overlap and returns:

- Top-k chunks (most relevant)

- Bottom-k chunks (least relevant)

Two RAG runs are performed per query:

- **RAG-Relevant**: using top-k chunks

- **RAG-Irrelevant**: using bottom-k chunks

This exposes how retrieval quality affects confidence, correctness, and
failure severity.

**Prompt scaffold (constant across strategies)**

All experiments use the same deterministic prompt structure:

Instruction: \<authoritative scope\>

Context: \<selected / summarized / retrieved chunks\>

Question: \<user query\>

Answer carefully and only within the instruction scope.

This scaffold ensures that differences in output are attributable to
context strategy rather than prompt phrasing.

**Key components in the codebase**

**retrieve_chunks(query, document, k)**

A simple chunk-based retriever using token overlap scoring. It is
intentionally transparent so that retrieved chunks can be inspected and
reasoned about.

**build_prompt(instruction, context, query)**

Constructs the fixed prompt scaffold shared across all strategies.

**get_generated_output(prompt)**

Invokes model generation and returns decoded output. Proper handling of
padding and EOS tokens is critical to avoid silent truncation.

**Summarization and trimming helpers**

Used to transform the same source document into different contextual
representations while keeping the question constant.

**Observed failure patterns**

Across multiple runs, several consistent patterns emerge:

- **Trimming** often reduces hallucination but increases silent failure
  modes such as repetition or instruction echoing.

- **Summarization** can remove essential details or terminate early,
  especially when performed by the same weak model used for downstream
  QA.

- **RAG with relevant chunks** often produces confident but shallow
  answers that mirror retrieved text without true synthesis.

- **RAG with irrelevant chunks** produces the most dangerous failures:
  fluent, authoritative, and completely unsupported answers.

These behaviors appear even when instructions are clear and identical
across runs.

**Why this experiment matters**

The results demonstrate that **context strategy selection directly
shifts failure modes**, not just accuracy:

- Trimming biases toward abstention-like behavior.

- Summarization trades completeness for coherence.

- RAG shifts failure from ignorance to overconfidence.

This has direct implications for AI systems in regulated or high-risk
domains, where confidence without grounding is often worse than refusal.

**Next steps (recommended)**

1.  Introduce explicit abstention detection and compare how often each
    strategy produces unsafe answers versus refusals.

2.  Replace naive retrieval with a ranked retriever and compare
    confidence inflation effects.

3.  Extend the experiment to instruction-tuned models and observe which
    failure modes persist.
