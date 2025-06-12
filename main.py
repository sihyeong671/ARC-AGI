import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.utils import load_json

class Qwen:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        self.history = []
        
    def generate(
        self,
        user_input: str,
        max_tokens: int = 512,
        enable_thinking: bool = True
    ):
        messages = self.history + [{"role": "user", "content": user_input}]
        text = self.tokenizer.apply_chat_template(
            messages,
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
        
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response})
        
        return thinking_content, response
        
        

def main():
    
    train_challenges_path = "data/arc-agi_training_challenges.json"
    train_solution_path = "data/arc-agi_training_solutions.json"
    
    train_challenges = load_json(train_challenges_path)
    train_solution = load_json(train_solution_path)
    
    # TODO
    # define cache_dir
    model_name = "Qwen/Qwen3-1.7B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="cuda"
    )
    qwen = Qwen(tokenizer, model)
    
    sample_challenge_id = list(train_challenges.keys())[0]
    challenge = train_challenges[sample_challenge_id]
    
    prompt = """You will be given a list of input-output pairs, labeld "Case 0", "Case 1", and so on. Each input and output is a grid of numbers representing a visual grid. There is a SINGLE rule that transforms each input grid to the corresponding grid.
The pattern may involve counting or sorting objects (e.g. sorting by size), comparing numbers (e.g. which shape or symbol appears the most?) Which is the largest object? Which objects are the same size?), or repeating a pattern for a fixed number of time.

There are other convepts that may be relevant.
- Lines, rectangular shapes
- Symmetries rotations, translations.
- Shape upscaling or downscaling, elastic distortations.
- Containing / being contained / being inside or outside of a perimeter.
- Drawing lines, connecting points, orthogonal projections.
- Copying, repeating objects.

You should treat cells with 0 as empty cells (backgrouds).

Please generate the Output grid that corresponds to the last given Input grid, using the transformation rule you induced from the previous input-output pairs.
"""
    
    for i, task in enumerate(challenge["train"]):
        prompt += f"Input {i+1}:\n"
        prompt += str(task["input"]) + "\n"
        prompt += f"Output {i+1}:\n"
        prompt += str(task["output"]) + "\n\n"
    
    prompt += "Now, predict the output for the following test input:\n"
    prompt += str(challenge["test"][0]["input"]) + "\n"
    prompt += "Output:\n"
    
    think, response = qwen.generate(prompt, max_tokens=30000)
    print("### THINK ###")
    print(think)

    print("### RESPONSE ###")
    print(response)

if __name__ == "__main__":
    main()
