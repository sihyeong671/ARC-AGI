import json
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

arc_colors = ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
              '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']

cmap = ListedColormap(arc_colors)
norm = BoundaryNorm(range(11), cmap.N)

@st.cache_resource
def load_json(json_path: str):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data

def plot_one(ax, mat, title: str):
    ax.imshow(mat, cmap=cmap, norm=norm)
    ax.set_title(title, fontsize=8)
    ax.axis("off")

st.title("Title")

selected_data = st.selectbox(
    "데이터 선택",
    ["train", "eval", "test"]
)

if selected_data == "train":
    challenges_data = load_json("data/arc-agi_training_challenges.json")
    solutions_data = load_json("data/arc-agi_training_solutions.json")
elif selected_data == "eval":
    challenges_data = load_json("data/arc-agi_evaluation_challenges.json")
    solutions_data = load_json("data/arc-agi_evaluation_solutions.json")
elif selected_data == "test":
    challenges_data = load_json("data/arc-agi_test_challenges.json")
    solutions_data = None

id_list = list(challenges_data.keys())

task_id = st.selectbox(
    "Select ID",
    id_list
)

task = challenges_data[task_id]

train = task["train"]
test = task["test"]
total_length = len(train) + (1 if test else 0)

if solutions_data is not None:
    solution = solutions_data[task_id][0]

fig, axs = plt.subplots(2, total_length, figsize=(2 * total_length, 4))
axs = np.atleast_2d(axs)

fig.suptitle(f"Task: {task_id}", fontsize=8)


for idx, pair in enumerate(train):
    plot_one(axs[0, idx], pair['input'], f"Train {idx} Input")
    plot_one(axs[1, idx], pair['output'], f"Train {idx} Output")

if test:
    plot_one(axs[0, len(train)], test[0]['input'], "Test Input")
    if solutions_data is not None:
        plot_one(axs[1, len(train)], solution, "Test Output")

st.pyplot(fig)