import re
import ast
import json

def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)
    
def make_input(inputs: dict) -> str:
    """challenges data를 받아서 llm input prompt로 변환"""

    train_datas: list = inputs["train"]

    if len(inputs["test"]) > 1:
        # test input이 1개 이상인 경우 에러 호출
        raise ValueError("test has more than 2 matrix inputs")
    
    test_data = inputs["test"][0]
    
    # TODO
    # prompt engineering
    
    train_data = train_datas[0]
    train_input = train_data["input"]
    train_output = train_data["output"]

    test_input = test_data["input"]

    prompt = (
        "predict the test output\n"
        "<example>\n"
        f"Input:\n{train_input}\noutput:\n{train_output}\n"
        "</example>\n"
        f"test input:\n{test_input}\ntest output:"
    )
    
    return prompt

def parse_llm_arc_output(text: str) -> str:
    m = re.search(r"\[\[\s*.*?\s*\]\]", text)
    if not m:
        return [[0, 0], [0, 0]]
    try:
        return ast.literal_eval(m.group(0))
    except(ValueError, SyntaxError):
        return [[0, 0], [0, 0]]
    

def parse_llm_custom_output(text: str) -> str | None:
    m = re.search(r"\[\s*.*?\s*\]", text)
    if not m:
        return None
    try:
        return ast.literal_eval(m.group(0))
    except(ValueError, SyntaxError):
        return None
    

if __name__ == "__main__":
    text = "text [1, 3, 5, 33, 5 ,'aa'  ] hi"
    print(parse_llm_custom_output(text))