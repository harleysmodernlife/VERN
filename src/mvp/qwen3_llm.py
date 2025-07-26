"""
Qwen3-0.6B LLM Wrapper for VERN

Handles loading, inference, and config for Qwen3-0.6B using Hugging Face Transformers.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-0.6B"

class Qwen3LLM:
    def __init__(self, device=None, enable_thinking=True):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.enable_thinking = enable_thinking
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype="auto",
            device_map="auto" if self.device == "cuda" else None
        ).to(self.device)
        self.history = []

    def generate(self, prompt, context=None, max_new_tokens=256):
        messages = self.history + [{"role": "user", "content": prompt}]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=self.enable_thinking
        )
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens
        )
        output_ids = generated_ids[0][len(inputs.input_ids[0]):].tolist()

        # Try to parse <think> block if present
        try:
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

        # Update history
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": content})

        return {
            "thinking": thinking_content,
            "content": content
        }

# Example usage (for testing)
if __name__ == "__main__":
    llm = Qwen3LLM(enable_thinking=True)
    result = llm.generate("Give me a short introduction to large language models.")
    print("Thinking:", result["thinking"])
    print("Content:", result["content"])
