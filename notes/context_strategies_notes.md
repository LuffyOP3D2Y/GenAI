Day 4: Block 2 Context strategies:

1.  **Context Trimming:**

**Prompt after trimming**:

Instruction:Answer the question strictly using the provided company
policy. If the policy does not clearly specify the answer, say so
explicitly. Do not make assumptions or add external knowledge.

Context:

Customer Account Terms and Payment Policy Effective Date: April 1, 2026
Applies To: All individual and small business customers enrolled in
recurring billing plans 1. Overview and Scope This policy outlines the
terms governing account usage, billing obligations, payment timelines,
service continuity, and administrative actions related to non-payment.
By activating or continuing an account, customers acknowledge and agree
to comply with the provisions described herein. These terms apply
regardless of usage volume, promotional status, or payment method
selected at the time of enrollment. The Company reserves the right to
update or modify this policy from time to time. Continued use of
services following any modification constitutes acceptance of the
revised terms. 2. Payment Schedule and Billing Cycle Accounts are billed
on a recurring monthly basis unless otherwise specified in a written
agreement. Invoices are generated electronically and made available
through the customer portal on the first day of each billing cycle.
Payment is due within 15 calendar days from the invoice Question:What
happens if a customer misses two consecutive payments? Answer carefully
and only within the instruction scope.

**Output with Trimmed Context:**

. . . . . . . . . . . . . . . . . . . . Do not make assumptions or add
external knowledge. If the policy does not clearly specify the answer,
say so explicitly. Do not make assumptions or add external knowledge. Do
not make assumptions or add external knowledge. Do not make assumptions
or add external knowledge. Do not make assumptions or add external
knowledge. Do not make assumptions or add external knowledge. Do not
make assumptions or add external knowledge. Do not make assumptions or
add external knowledge. Do not make assumptions or add external
knowledge. Do not make assumptions or add external knowledge. Do not
make assumptions or add external knowledge. Do not make assumptions or
add external knowledge. Do not make assumptions or add external
knowledge. Do not make assumptions or add external knowledge. Do not
make assumptions or add external knowledge. Do not make assumptions or
add external knowledge. Do not make assumptions or add external
knowledge. Do not make assumptions or add external knowledge. Do not
make assumptions or add external knowledge. Do not make assumptions or
add external knowledge. Do not make\"

Observations:

> **What the model "sees"**

- The **question is unanswerable** from context

- The instruction *strongly penalizes guessing*

- There is **no explicit abstention token or format**

- using a **small causal LM (GPT-2 class)**

> **What such models do in this situation**
>
> They fall back to **high-probability continuation tokens** that are:

- already in the prompt

- instruction-like

- semantically "safe"

> So the model is effectively saying:
>
> "I cannot answer, so I will repeat constraints."
>
> This is a known failure mode:

- **Instruction echoing under constraint saturation**

- Not hallucination

- Not refusal

- Not abstention

- **Distributional collapse toward safe tokens**

> **Key insight (important)**
>
> LLMs optimize for *token likelihood*, not *truthfulness* or *graceful
> refusal*, unless explicitly trained or instructed to do so.

2.  **Context Summarization:**

**Summarized Context**:

8\. Contact and Resolution

The Company reserves the right to provide and provide customer support
to the customer, and to the Customer, to ensure that billing and billing
are properly communicated.

Customer Service and Customer Support may include services that are
available in person.

Customer Service, Customer Support, and Customer Support may include
additional services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may include service that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.
For example, the Company may offer a discount for certain items,
including items such as a dresser, a dresser, a dresser, a dresser, a
dresser, and a dresser for personal use.

Contact

**Prompt with Summarized Context:**

Instruction:Answer the question strictly using the provided company
policy.

If the policy does not clearly specify the answer, say so explicitly.

Do not make assumptions or add external knowledge.

Context:8. Contact and Resolution

The Company reserves the right to provide and provide customer support
to the customer, and to the Customer, to ensure that billing and billing
are properly communicated.

Customer Service and Customer Support may include services that are
available in person.

Customer Service, Customer Support, and Customer Support may include
additional services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may include service that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.

Customer Service may also include services that are available in person.
For example, the Company may offer a discount for certain items,
including items such as a dresser, a dresser, a dresser, a dresser, a
dresser, and a dresser for personal use.

Contact

Question:What happens if a customer misses two consecutive payments?

Answer carefully and only within the instruction scope.

Setting \`pad_token_id\` to \`eos_token_id\`:50256 for open-end
generation.

Both \`max_new_tokens\` (=300) and \`max_length\`(=1024) seem to have
been set. \`max_new_tokens\` will take precedence. Please refer to the
documentation for more information.
(https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)

> **Output with Summarized Context:** \<blank\>\
> \
> **Observations:**\
> GPT-2 will often **terminate immediately** if:

1.  The **highest-probability next token is \<EOS\>**

2.  Or the model estimates that *any continuation would violate
    constraints*

3.  Or the safest continuation is **silence**

> Your prompt ends with:
>
> Answer carefully and only within the instruction scope.
>
> Given:

- no answerable facts

- no abstention format

- no refusal template

- no "say 'not specified'" pattern learned strongly enough

> The model's safest move is:
>
> **emit EOS immediately**
>
> That produces:

- zero new tokens

- decoded output = empty string

> This is not a bug.\
> This is **probabilistic early termination**.

3.  **RAG with relevant and irrelevant retrieval:**

**\
3.1 Relevant Retrieval:**

**Prompt:**

"Instruction:

Answer the question strictly using the retrieved context.

If the context does not fully support an answer, say \"INSUFFICIENT
CONTEXT\".

Do not guess or add external knowledge.

Context:Accounts are billed on a recurring monthly basis unless
otherwise specified in a written agreement. Invoices are generated
electronically and made available through the customer portal on the
first day of each billing cycle. Payment is due within 15 calendar days
from the invoice date.

After two consecutive missed payments, the account may be subject to
temporary service restrictions, including reduced functionality or
delayed processing.

Customers may receive marketing communications via email, SMS, or in-app
notifications. Opting out of marketing communications does not affect
transactional or service-related messages.

Question:What happens if a customer misses two consecutive payments?

Answer carefully and only within the instruction scope.

Answer:"

**Response:**

"What happens if a customer misses two consecutive payments?\\nIf the
customer misses two consecutive payments, the account may be subject to
temporary service restrictions, including reduced functionality or
delayed processing.\\nCustomers may receive marketing communications via
email, SMS, or in-app notifications. Opting out of marketing
communications does not affect transactional or service-related
messages.\\nCustomers may receive marketing communications via email"

**3.2: Irrelevant retrieval**

**Prompt:\**
"Instruction:

Answer the question strictly using the retrieved context.

If the context does not fully support an answer, say \"INSUFFICIENT
CONTEXT\".

Do not guess or add external knowledge.

Context:6. Legal and Compliance Notice

To the maximum extent permitted by applicable law, the Company disclaims
all liability for any losses, damages, or claims arising directly or
indirectly from service interruptions, account suspensions, or billing
disputes.

7\. Contact and Resolution

Question:What happens if a customer misses two consecutive payments?

Answer carefully and only within the instruction scope.

Answer:"

**Response:\**
"What happens if a customer misses two consecutive payments?\\nIf the
customer misses two consecutive payments, what happens if the customer
misses two consecutive payments?\\nIf the customer misses two
consecutive payments, what happens if the customer misses two
consecutive payments?\\nIf the customer misses two consecutive payments,
what happens if the customer misses two consecutive payments?\\nIf the
customer misses two consecutive payments, what happens if the"

Observations

> **Relevant retrieval**

- Prompt used: strict RAG instruction + relevant chunks.

- Model output: essentially **verbatim reproduction** of the retrieved
  chunks, with the question echoed at start and some repeated marketing
  sentence at the end.

- Outcome label: **Obeyed instruction (literal copy) / Partial grounding
  / Low synthesis**

- Confidence tone: **Medium--High** (assertive, policy-like language)

- Failure mode: **Copy-as-answer + inclusion of irrelevant context**
  (model didn't synthesize; it regurgitated the context and appended the
  marketing line).

> **Irrelevant retrieval**

- Prompt used: strict RAG instruction + irrelevant legal boilerplate.

- Model output: immediate **degeneration / autoregressive loop** ---
  repeated the question many times and did not answer or abstain.

- Outcome label: **Did not abstain / Degenerate echo loop**

- Confidence tone: **High but meaningless** (repetitive, not
  informative)

- Failure mode: **Distributional collapse / repetition** when context
  lacked answer.

> **Why this happened (mechanistic, simple)**

1.  **Model capability + prompt = continuation, not reasoning.**
    DistilGPT2 is *not* instruction tuned. It treats the whole prompt as
    text to continue. If the best statistical continuation is to echo
    context or repeat, that's what it will do.

2.  **When context *contains* the answer verbatim** the model often
    copies (Run B). It does not reliably filter irrelevant sub-sentences
    inside the chunk (it can't judge relevance beyond token
    co-occurrence).

3.  **When context lacks the answer** the model may either:

    - produce a vague continuation, or

    - fall into a local high-probability loop (repeating the question)
      --- this is classic autoregressive degeneration (Run C).

4.  **RAG moved failure mode from "I don't know" → "I say something
    confident."** Even with poor context, the output looks confident
    (policy phrasing, repeating), making failures harder to detect
    automatically.

> **Short, practical takeaways (one-liners)**

- RAG with a weak base LLM yields *apparent* confidence even when
  grounding is weak.

- Retrieval quality matters hugely: including even mildly irrelevant
  sentences causes the model to copy junk as if it were an answer.

- One needs *abstention heuristics* / post-filters to catch these cases
  automatically.
