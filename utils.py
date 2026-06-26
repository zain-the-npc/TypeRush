import time

def calculate_accuracy(original, typed):
    if not original:
        return 0
    # Compare full length of original — missing/extra characters count as mistakes
    correct = sum(
        1 for i in range(len(original))
        if i < len(typed) and original[i] == typed[i]
    )
    return round((correct / len(original)) * 100, 2)

def count_mistakes(original, typed):
    # Any position where typed is wrong or missing counts as a mistake
    mistakes = sum(
        1 for i in range(len(original))
        if i >= len(typed) or original[i] != typed[i]
    )
    return mistakes

def calculate_wpm(typed_text, start_time, end_time):
    if start_time is None or end_time is None:
        return 0
    words = len(typed_text) / 5
    minutes = (end_time - start_time) / 60
    return round(words / minutes, 2) if minutes > 0 else 0

def highlight_mistakes(original, typed):
    highlighted = ""
    for i in range(len(original)):
        o = original[i]
        t = typed[i] if i < len(typed) else ""
        if o == t:
            highlighted += f"<span style='color:white'>{o}</span>"
        else:
            highlighted += f"<span style='color:red'>{o}</span>"
    return highlighted