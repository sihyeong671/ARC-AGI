import os
import random
import json


# 2차원 인식 평가 데이터 셋 생성 스크립트
# 인덱스는 항상 0부터 시작

# v1. 0과 1로 이루어진 일반적인 행렬에서 1의 위치 찾기
# v2. 0 ~ 9의 랜덤한 숫자로 이루어진 행렬 + 찾아야할 숫자가 여러개
# v3. 0, 1로 이루어진 행렬에서 1의 좌표 이동

# 등등
# target number가 두개 있는 열 or 행
# 열 or 행 swap

# TODO
# v4
# v5

DATA_DIR = "dataset/"
os.makedirs(DATA_DIR, exist_ok=True)

def gen_data_v1():
    """input으로 행렬을 주고 특정 숫자의 좌표가 어디있는지 출력
    0과 1로 이루어진 일반적인 행렬
    """
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

    with open("dataset_v1.json", "w") as f:
        json.dump(dataset, f, indent=2)


def gen_data_v2():
    """input으로 행렬을 주고 특정 숫자의 좌표가 어디있는지 출력
    0 ~ 9 랜덤 숫자로 이루어진 행렬

    찾아야할 target number가 1 ~ 5개 랜덤으로 존재
    """
    num_samples = 100
    dataset = {"dataset": []}
    for _ in range(num_samples):
        rows = random.randint(3, 16)
        cols = random.randint(3, 16)

        target_num = random.randint(0, 9)
        random_num = [i for i in range(10)]
        random_num.remove(target_num)
        
        target_position = set()

        for _ in range(1, 6):
            target_position.add((random.randint(0, rows-1), random.randint(0, cols-1)))

        matrix = []
        for r in range(rows):
            str_col = ""
            for c in range(cols):
                if (r, c) in target_position:
                    str_col += str(target_num)
                else:
                    str_col += str(random.choice(random_num))
            matrix.append(str_col)

        dataset["dataset"].append({
            "matrix": matrix,
            "target_num": target_num,
            "coordinates": list(target_position)
        })

        with open("dataset_v2.json", "w") as f:
            json.dump(dataset, f, indent=2)

gen_data_v1()
gen_data_v2()

def generate_eval_data():
    # 모든 데이터 묶어서 하나의 json파일로 생성
    pass