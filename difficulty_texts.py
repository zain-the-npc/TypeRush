import json

def load_texts():
    with open("data/sample_texts.json", "r") as f:
        return json.load(f)

def get_text_by_difficulty(level):
    texts = load_texts()
    from random import choice
    return choice(texts.get(level, []))
