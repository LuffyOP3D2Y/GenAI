**LLM Guardrails Experiment**

**Purpose**

This experiment implements and evaluates a **guarded text-generation
pipeline** designed to constrain Large Language Model (LLM) behavior
under unsafe or ambiguous inputs.

The focus of this experiment is **code-level behavior**:

- How prompts are constructed

- How instructions and queries are separated

- How guardrails are applied before returning model output

- How abstention is surfaced programmatically

Interpretation of outputs, failure analysis, and system-level
implications are documented separately in the corresponding memo.

**Experiment Scope**

This experiment explores **instruction-bound generation** using a
lightweight LLM with explicit guardrail logic.

Key capabilities implemented:

- Instruction--query separation

- Deterministic prompt scaffolding

- Guarded generation with explicit abstention paths

- Minimal, inspectable control logic (no external frameworks)

The experiment intentionally avoids:

- Retrieval (RAG)

- Summarization

- Multi-agent orchestration

- Model fine-tuning

Those are handled in separate experiments.

**Code Structure**

**Primary File**

- llm_guarded.py

This file contains the full implementation of the guardrails and the
generation pipeline.

**High-Level Code Flow**

The execution flow is intentionally linear and easy to inspect:

1.  **Model and tokenizer initialization**

2.  **Prompt construction using a fixed scaffold**

3.  **Guarded generation**

4.  **Post-generation checks**

5.  **Structured output returned to caller**

Each step is explicit and isolated to make failure modes observable.

**Prompt Construction**

Prompts are constructed using a deterministic scaffold:

- **Instruction**\
  Defines the authoritative scope of what the model is allowed to do.

- **Context** (optional)\
  Treated as untrusted input.

- **Question**\
  User-provided query.

- **Terminal directive**

- Answer carefully and only within the instruction scope.

This scaffold is built programmatically to ensure consistency across
runs.

**Guarded Generation Logic**

The core function responsible for enforcing guardrails is:

- guarded_generate(\...)

This function:

- Receives a fully constructed prompt

- Executes model generation

- Applies guardrail checks on the output

- Decides whether to:

  - Return an answer

  - Abstain with a structured reason

The guardrails are applied **outside** the model itself and do not rely
on fine-tuning.

**Abstention Handling**

Abstention is treated as a **first-class system outcome**, not an error.

When guardrails trigger, the system returns:

- A structured abstention signal

- A reason code indicating why generation was suppressed

This design allows abstention to be:

- Machine-detectable

- Logged consistently

- Used in downstream control flows

**Running the Experiment**

Typical usage pattern:

1.  Define:

    - Instruction

    - Context (optional)

    - Query

2.  Build the prompt using the scaffold

3.  Call guarded_generate(\...)

4.  Inspect the returned structured output

No additional configuration or external services are required.

**Outputs**

The experiment produces:

- Console outputs for inspection

- Structured return objects indicating:

  - Answer vs abstention

  - Reason codes

Raw inputs and outputs used during experimentation are preserved
separately for traceability.

**Model Choice**

The experiment uses **DistilGPT-2** as the underlying model.

This choice is intentional for this experiment because:

- It makes failure modes more visible

- It avoids relying on instruction-tuned behavior

- It keeps the focus on **system design**, not model capability

Model limitations are discussed in the accompanying memo, not in this
README.

**Related Artifacts**

- **Memo**: Detailed analysis of observed behaviors and implications

- **Notes**: Raw prompts and verbatim model outputs

- **Context Strategies Experiment**: Separate experiment exploring
  trimming, summarization, and RAG

**What This Experiment Is (and Is Not)**

**This experiment is:**

- A demonstration of guardrails as system logic

- A minimal, inspectable control pipeline

- Focused on safety, scope control, and abstention

**This experiment is not:**

- A production-ready policy engine

- A benchmark of model intelligence

- A retrieval or agent framework
