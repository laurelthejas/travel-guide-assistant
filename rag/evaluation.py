"""
evaluation.py - a very simple evaluation setup.

1) Automatic check against a GOLDEN DATASET:
   score = share of expected keywords found in the answer
   score >= PASS_SCORE  -> thumbs up, otherwise thumbs down
2) HUMAN FEEDBACK: thumbs up/down + comment from the app, saved to feedback.csv
"""
import csv
import json
import time
from datetime import datetime

import pandas as pd

import config

PASS_SCORE = 0.5
FEEDBACK_COLUMNS = ["timestamp", "approach", "question", "answer", "rating", "comment"]


# ------------------------------------------------------------ golden dataset
def load_golden():
    return json.loads(config.GOLDEN_DATASET.read_text(encoding="utf-8"))


def keyword_score(answer, keywords):
    answer = answer.lower()
    found = [k for k in keywords if k.lower() in answer]
    return len(found) / len(keywords)


def run_evaluation(approaches, on_progress=None):
    """approaches = {"RAG": function(question) -> answer text, ...}"""
    golden = load_golden()
    rows, total, done = [], len(golden) * len(approaches), 0
    for item in golden:
        for name, ask in approaches.items():
            start = time.time()
            try:
                answer = ask(item["question"])
            except Exception as err:                       # keep going if one approach fails
                answer = f"ERROR: {err}"
            score = keyword_score(answer, item["keywords"])
            rows.append({"approach": name, "type": item["type"], "question": item["question"],
                         "answer": answer, "expected": item["expected_answer"],
                         "score": round(score, 2), "verdict": "👍" if score >= PASS_SCORE else "👎",
                         "seconds": round(time.time() - start, 1)})
            done += 1
            if on_progress:
                on_progress(done / total, f"{name}: {item['question']}")
    return pd.DataFrame(rows)


# ------------------------------------------------------------ human feedback
def save_feedback(approach, question, answer, rating, comment=""):
    new_file = not config.FEEDBACK_FILE.exists()
    with open(config.FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(FEEDBACK_COLUMNS)
        writer.writerow([datetime.now().isoformat(timespec="seconds"), approach, question, answer, rating, comment])


def load_feedback():
    if not config.FEEDBACK_FILE.exists():
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)
    return pd.read_csv(config.FEEDBACK_FILE)
