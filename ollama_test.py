import os
import json
import ollama
from tqdm import tqdm

from src.utils import parse_llm_custom_output

OUTPUT_DIR = "output/"
SYSTEM_PROMPT = """Find 1 in the matrix of the following strings and output its coordinates
The index starts at zero.

The output must be list of coordinates format like [row, col].

"""

MODEL_NAME = "qwen3:0.6b"


wrong_predictions = []
correct_cnt = 0

with open("dataset/dataset_v1.json", "r") as f:
    data = json.load(f)

dataset = data["dataset"]

for idx, task in enumerate(tqdm(dataset)):

    matrix_prompt = "Input:\n"
    matrix = [list(map(int, s)) for s in task["matrix"]]
    matrix_prompt += f"{matrix}"
    prompt = matrix_prompt + "Output:"
    
    
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        think=True,
        options={
            "num_ctx": 3000
        }
    )

    predicted_output = response["message"]["content"]
    # print(predicted_output)
    
    output_list = predicted_output.split("</think>")
    # print(output_list)
    think, output = output_list[0], output_list[-1]

    pred = parse_llm_custom_output(output)
    answer = task["coordinate"]
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/output.txt", "a", encoding="utf-8") as f:
        f.write(f"""-----{idx}-----
{matrix_prompt}  
                
{think}
</think>

Predict: {pred}
Answer: {answer}

""")
    
    if str(answer) == pred:
        correct_cnt += 1
        print("Correct!")

print(correct_cnt)

