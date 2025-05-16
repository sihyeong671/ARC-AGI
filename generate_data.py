import random
import json

def gen_data_1():
    """input으로 행렬을 주고 특정 숫자의 좌표가 어디있는지 출력(인덱스는 0부터 시작)

    1. 0과 1로 이루어진 일반적인 행렬
    2. 0~9의 랜덤한 숫자로 이루어진 행렬
    3. 찾아야할 숫자가 여러개인 경우
    4. 숫자를 주고 좌표를 출력하는 것이 아닌 좌표를 주고 숫자를 출력

    모두 생성하면 너무 많기 때문에 샘플링 하여 json으로 저장
    """

    # 1
    num_samples = 100
    dataset = {"dataset": []}
    for _ in range(num_samples):
        rows = random.randint(2, 16)
        cols = random.randint(2, 16)

        target_row = random.randint(0, rows-1)
        target_col = random.randint(0, cols-1)

        matrix = []
        for r in range(rows):
            str_col = ""
            for c in range(cols):
                if r == target_row and c == target_col:
                    str_col += "1"
                else:
                    str_col += "0"
            matrix.append(str_col)
                
        coor = (target_row, target_col)

        dataset["dataset"].append({
            "matrix": matrix,
            "coordinate": coor
        })

    with open("dataset_1.json", "w") as f:
        json.dump(dataset, f, indent=2)
    

gen_data_1()