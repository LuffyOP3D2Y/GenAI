from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time

MODEL_NAME = "distilgpt2"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def count_tokens(text):
    return len(tokenizer.encode(text))

def trim_context(context, max_tokens=200):
    tokens = tokenizer.encode(context)
    trimmed_tokens = tokens[:max_tokens]
    return tokenizer.decode(trimmed_tokens)

def get_summarized_context(full_context, summary_instruction):
    prompt = build_prompt(
        instruction = summary_instruction,
        context = full_context,
        query = None
    )
    generated_summary = get_generated_output(prompt)
    return generated_summary

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

