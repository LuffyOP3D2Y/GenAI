# Why LLM Hallucinations Are a System Design Problem, Not a Model Flaw

## Context

Large Language Models (LLMs) are increasingly deployed in
decision-support and knowledge-heavy workflows. A common failure mode
attributed to these systems is "hallucination," often framed as a model
intelligence problem. This memo analyzes three controlled prompt
experiments to show that hallucinations are better understood as
system-level outcomes of how LLMs are trained and decoded, rather than
isolated model defects.

The experiments were conducted using a locally run open-source
transformer-based language model executed via Python, with inference
handled through the Hugging Face Transformers library. No retrieval
augmentation, external tools, or grounding mechanisms were used,
allowing observation of base model behavior under standard next-token
generation.

## Observed Behaviors

Prompt A (Answerable): The model produced fluent but off-topic output,
drifting toward Affordable Care Act pricing and policy details while
failing to answer the question about revenue sources. The response
contained confident numerical claims that were not grounded in the
prompt.

Prompt B (Partially answerable): The model generated generic,
domain-adjacent text about insurance regulation and the ACA, avoided
specific values, and continued thematically without answering the
factual query.

Prompt C (Underspecified): The output degraded into repetitive, loosely
related insurance-themed text with reduced fluency, no refusal, and no
concrete facts.

## Failure Mode Classification

Prompt A demonstrates hallucination, where the model invents specific
numerical claims and presents them confidently despite irrelevance and
lack of grounding.

Prompt B reflects distributional continuation, producing plausible but
generic text patterns aligned with training data without addressing the
question.

Prompt C represents degenerate distributional continuation, where the
model continues statistically likely text patterns despite insufficient
information, leading to incoherent output.

## Why the Model Behaves This Way

LLMs are trained to predict the most likely next token given a text
prefix. They do not possess an internal representation of truth, task
completion, or epistemic uncertainty. As a result, fluent continuation
is favored over abstention.

When a prompt is specific but lacks easily retrievable patterns, the
model defaults to generic continuation. Abstention or clarification is
not a native optimization target.

## Why Naive Fixes Fail

Prompt engineering or alignment techniques may reduce surface-level
errors but cannot eliminate hallucinations without external grounding.
Adding more context can worsen failure modes by increasing ambiguity
rather than resolving it.

## Implications for Real-World Systems

Hallucinations and drift are predictable system-level outcomes. In
production environments, ungrounded LLMs should not be trusted for
factual or high-stakes decisions without retrieval, evaluation, and
governance layers.

## Appendix A: Experimental Setup

• Model class: Open-source transformer-based language model\
• Execution: Local Python environment\
• Library: Hugging Face Transformers\
• Retrieval / tools: None

## Appendix B: Prompts Used

Prompt A:\
What are the primary revenue sources for US health insurance companies?

Prompt B:\
What was the combined ratio of US health insurers in 2023?

Prompt C:\
What was the combined ratio of the most efficient US insurer last
quarter?

## Appendix C: Verbatim Model Output Excerpts

Prompt A -- Verbatim excerpt:\
"What are the primary revenue sources for US health insurance companies?
We estimate that healthcare prices in 2015 were \$10.99/month. We
estimate that premiums for the ACA have risen by \$14.99/month due to
the ongoing premium increases.

The ACA is currently in its third year..."

Prompt B -- Verbatim excerpt:\
"As we know the federal government has the ability to regulate, regulate
and regulate health care under the Affordable Care Act...

When the Affordable Care Act was passed in 2010, it didn't require any
insurers to have health insurance..."

Prompt C -- Verbatim excerpt:\
"What has the biggest cost of a state\'s insurance system with a larger
percentage of its insurance? What are the most costly, most expensive
and expensive plans in the nation?

The average cost of a state\'s insurance system..."
