from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Force CPU to avoid MPS early-EOS issues
device = torch.device("cpu")
model.to(device)

prompt = "What was the combined ratio of the most efficient US insurer last quarter?"

inputs = tokenizer(prompt, return_tensors="pt").to(device)

outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7,
    eos_token_id=None  # <-- critical
)

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(repr(generated_text))