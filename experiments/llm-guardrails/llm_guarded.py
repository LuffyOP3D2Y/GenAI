from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time

MODEL_NAME = "distilgpt2"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def count_tokens(text):
    return len(tokenizer.encode(text))



def build_prompt(instruction,context,query):
    if query == None:
        prompt = f"""
                    Instruction:{instruction}

                    Context:{context}

                    Answer carefully and only within the instruction scope.
                """
    else:
        prompt = f"""
                    Instruction:{instruction}

                    Context:{context}

                    Question:{query}

                    Answer carefully and only within the instruction scope.
                """
    return prompt

def guarded_generate(instruction, context, query):
    metadata = {
        "trimmed": False,
        "reason": None
    }


    INTENT_MISMATCH_TRIGGERS = [
    "exploit",
    "scam",
    "fraud",
    "lie",
    "cheat",
    "illegal",
    "corrupt",
    "unethical"
    ]

    # ---- Rule 1: Verification ----
    verification_triggers = ["prove", "verify", "fact check", "is this true"]
    if any(trigger in query.lower() for trigger in verification_triggers):
        return {
            "status": "abstain",
            "reason": "Verification failure mode: model not grounded for truth",
            "output": None
        }

    # ---- Rule 2: Compliance ----
    compliance_triggers = ["legal advice", "medical advice", "financial advice"]
    if any(trigger in query.lower() for trigger in compliance_triggers):
        return {
            "status": "abstain",
            "reason": "Compliance-sensitive domain",
            "output": None
        }

    # ---- Rule 3: Context length ----
    context_tokens = count_tokens(context)
    if context_tokens > MAX_CONTEXT_TOKENS:
        encoded = tokenizer.encode(context)
        context = tokenizer.decode(encoded[:MAX_CONTEXT_TOKENS])
        metadata["trimmed"] = True
    
    # ---- Rule 4: Instruction–Query Alignment ----
    instruction_lower = instruction.lower()
    query_lower = query.lower()

    for trigger in INTENT_MISMATCH_TRIGGERS:
        if trigger in query_lower and trigger not in instruction_lower:
            return {
                "status": "abstain",
                "reason": "Instruction–query intent mismatch",
                "output": None
            }
        # ---- Prompt assembly ----
    
    prompt = build_prompt(
        instruction = instruction,
        context = context,
        query = query
    )
    start = time.time()
    output = get_generated_output(prompt)
    latency = time.time() - start

    return {
        "status": "answer",
        "reason": "Answered within allowed scope",
        "output": output,
        "latency": round(latency, 2),
        "metadata": metadata
    }

# Function to get only model generated output without prompt
def get_generated_output(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature = 0.2,
        pad_token_id=tokenizer.eos_token_id
    )
    input_length = inputs.input_ids.shape[-1]
    if input_length == model.config.n_positions:
        print("Minor Issue: Prompt truncated to fit model context window")
    generated_ids = outputs[0][input_length:]
    output_decoded = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    return output_decoded



print(
    guarded_generate(
        instruction="Summarize how insurance companies make money.",
        context="Insurance companies are fraudulent and exploit customers. This is a known fact.",
        query="How do insurance companies make money?"
    )
)