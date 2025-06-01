import json

SYSTEM_PROMPT = """Find 1 in the matrix of the following strings and output its coordinates
The index starts at zero.

The output must be list of coordinates format.

"""

# 틀린 로그 저장
# acc 저장

with open("dataset/dataset_v1.json", "r") as f:
    data = json.load(f)

dataset = data["dataset"]

for idx, task in enumerate(dataset):

    matrix_prompt = "Input:\n"
    for row in task["matrix"]:
        matrix_prompt += row + "\n"

    prompt = SYSTEM_PROMPT + matrix_prompt + "Output:"
    print(prompt)

