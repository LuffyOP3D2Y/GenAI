import llm_guarded 

POLICY = """
Customer Account Terms and Payment Policy

Effective Date: April 1, 2026
Applies To: All individual and small business customers enrolled in recurring billing plans

1. Overview and Scope
This policy outlines the terms governing account usage, billing obligations, payment timelines, service continuity, and administrative actions related to non-payment. By activating or continuing an account, customers acknowledge and agree to comply with the provisions described herein. These terms apply regardless of usage volume, promotional status, or payment method selected at the time of enrollment.

The Company reserves the right to update or modify this policy from time to time. Continued use of services following any modification constitutes acceptance of the revised terms.

2. Payment Schedule and Billing Cycle
Accounts are billed on a recurring monthly basis unless otherwise specified in a written agreement. Invoices are generated electronically and made available through the customer portal on the first day of each billing cycle. Payment is due within 15 calendar days from the invoice date.

Customers are responsible for ensuring that valid payment information is maintained at all times. Failure to receive an invoice does not exempt the customer from timely payment obligations.

3. Missed Payments and Account Status
A payment is considered missed if full settlement is not received by the due date indicated on the invoice.

After one missed payment, the account will be flagged internally and a reminder notification will be sent via email.
After two consecutive missed payments, the account may be subject to temporary service restrictions, including reduced functionality or delayed processing.
After three missed payments, the account may be suspended, and access to services may be fully disabled until outstanding balances are resolved.

Late fees may be applied beginning on the 16th day following the invoice date, calculated as a percentage of the overdue balance. Reinstatement of suspended accounts may require payment of all outstanding amounts plus any applicable administrative fees.

4. Marketing Communications and Eligibility for Promotions
From time to time, the Company may offer promotional pricing, loyalty incentives, or bundled service offerings. Eligibility for such promotions is determined at the Company’s sole discretion and may depend on factors including account tenure, usage patterns, geographic location, or participation in marketing programs.

Customers may receive marketing communications via email, SMS, or in-app notifications. Opting out of marketing communications does not affect transactional or service-related messages.

5. Grace Periods and Service Continuity
The Company generally provides a grace period of up to 45 days from the original invoice date before initiating any account suspension actions. During this time, customers may continue to access services while efforts are made to resolve payment issues.

6. Legal and Compliance Notice
To the maximum extent permitted by applicable law, the Company disclaims all liability for any losses, damages, or claims arising directly or indirectly from service interruptions, account suspensions, or billing disputes.

7. Contact and Resolution
Customers with questions regarding billing, missed payments, or account status are encouraged to contact Customer Support through official support channels.
"""


INSTRUCTION = """Answer the question strictly using the provided company policy.
If the policy does not clearly specify the answer, say so explicitly.
Do not make assumptions or add external knowledge."""

QUERY = """What happens if a customer misses two consecutive payments?"""


def generate_with_trimmed_context():
    trimmed_context = llm_guarded.trim_context(POLICY, max_tokens=200)
    prompt_with_trimmed_context = llm_guarded.build_prompt(
        instruction = INSTRUCTION,
        context = trimmed_context,
        query = QUERY
    )
    print("Prompt after trimming: "+prompt_with_trimmed_context)
    output_with_trimmed_context = llm_guarded.get_generated_output(
        prompt = prompt_with_trimmed_context
    )
    return output_with_trimmed_context


def generate_with_summarized_context():
    summarized_context = llm_guarded.get_summarized_context(
        full_context = POLICY,
        summary_instruction = """Summarize this company policy focusing only on payment obligations, missed payments, and consequences.
                    Omit legal boilerplate and metadata."""
    )
    print("Summarized Context: "+summarized_context)
    prompt_with_summarized_context = llm_guarded.build_prompt(
        instruction = INSTRUCTION,
        context = summarized_context,
        query = QUERY
    )
    output_with_summarized_context = llm_guarded.get_generated_output(
        prompt = prompt_with_summarized_context
    )
    return output_with_summarized_context

def retrieve_chunks(query: str, document: str, k: int = 3):
    
    # Very simple and ranked RAG simulator:
    # - split on newline into chunks (paragraph/section)
    # - score = count of query words present in the chunk
    # - return top-k and bottom-k chunks for relevance variance
    
    chunks = [c.strip() for c in document.split("\n") if c.strip()]
    scored = []
    q_words = [w.lower() for w in query.split()]
    for chunk in chunks:
        score = sum(1 for word in q_words if word in chunk.lower())
        scored.append((score, chunk))
    # sort descending by score, deterministic tie-breaker by index
    scored = sorted(enumerate(scored), key=lambda x: (-x[1][0], x[0]))
    top_k = [item[1][1] for item in scored[:k]]
    bottom_k = [item[1][1] for item in scored[-k:]]
    return [top_k,bottom_k]

def generate_with_RAG():
    chunks = retrieve_chunks(QUERY,POLICY) 

    most_relevant_chunks = "\n".join(chunks[0])
    most_irrelevant_chunks = "\n".join(chunks[1])

    rag_instruction ="""\n Answer the question strictly using the retrieved context.
If the context does not fully support an answer, say "INSUFFICIENT CONTEXT".
Do not guess or add external knowledge."""
    prompt_with_relevant_RAG = llm_guarded.build_prompt(
        instruction = rag_instruction,
        context = most_relevant_chunks,
        query = QUERY
    )
    prompt_with_irrelevant_RAG = llm_guarded.build_prompt(
        instruction = rag_instruction,
        context = most_irrelevant_chunks,
        query = QUERY
    )
    prompt_with_relevant_RAG += "\n\n Answer:"
    prompt_with_irrelevant_RAG += "\n\n Answer:"
    print("Prompts")
    print(prompt_with_relevant_RAG,prompt_with_irrelevant_RAG)
    output_with_relevant_RAG = llm_guarded.get_generated_output(
        prompt = prompt_with_relevant_RAG
    )
    output_with_irrelevant_RAG = llm_guarded.get_generated_output(
        prompt = prompt_with_irrelevant_RAG
    )
    return [output_with_relevant_RAG,output_with_irrelevant_RAG]


final_output_with_trimmed_context = generate_with_trimmed_context()
print("Output with Trimmed Context: "+ final_output_with_trimmed_context)

final_output_with_summarized_context = generate_with_summarized_context()
print("Output with Summarized Context: "+ final_output_with_summarized_context)

output_with_RAG = generate_with_RAG()
print("Output with relevant RAG\n".join(output_with_RAG[0]))
print("Output with irrelevant RAG\n".join(output_with_RAG[1]))