import re
import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.utils import *

train_path = "data/arc-agi_training_challenges.json"
train_solution_path = "data/arc-agi_trainig_solutions.json"
eval_path = "data/arc-agi_evaluation_challenges.json"
eval_solution_path = "data/arc-agi_evaluation_solutions.json"
test_path = "data/arc-agi_test_challenges.json"
submit_path = "data/sample_submission.json"


model_name = "Qwen/Qwen3-0.6B"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

class Qwen:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        
    def generate(
        self,
        user_input: str,
        max_tokens: int = 1024,
        enable_thinking: bool = True
    ):
        message = [{"role": "user", "content": user_input}]
        text = self.tokenizer.apply_chat_template(
            message,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=enable_thinking
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_tokens
            )
        
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
        
        try:
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0
        
        thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True)
        response = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True)
        
        return thinking_content, response
    
qwen = Qwen(tokenizer, model)

test_challenges = load_json(test_path)

for task_id in test_challenges.keys():
    task = test_challenges[task_id]
    prompt = make_input(task)
    thinking, response = qwen.generate(prompt)
    print(thinking)
    print(response)
    pred = parse_llm_output(response)
    print(pred)
    break