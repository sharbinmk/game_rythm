# judge.py
from config import *

def hit_note(notes, lane):
    accuracy_impact = 0
    candidates = []

    for note in notes:
        if note.note_type != "dual" and note.lane != lane:
            continue

        note_center = note.x + note.image.get_width() // 2
        diff = note_center - PERFECT_X
        abs_diff = abs(diff)

        if abs_diff <= GOOD_WINDOW:
            candidates.append((note, diff, abs_diff))

    # Ghost tap
    if not candidates:
        return None

    note, diff, abs_diff = min(candidates, key=lambda x: x[2])

    # STEP 4: judge it
    if abs_diff <= CRITICAL_WINDOW:
        judgement = "CRITICAL"

    elif abs_diff <= PERFECT_WINDOW:
        judgement = "PERFECT LATE" if diff < 0 else "PERFECT EARLY"

    elif abs_diff <= GREAT_WINDOW:
        judgement = "GREAT LATE" if diff < 0 else "GREAT EARLY"

    else:
        judgement = "GOOD LATE" if diff < 0 else "GOOD EARLY"

    if judgement in ("CRITICAL", "PERFECT EARLY", "PERFECT LATE"):
        accuracy_impact = 1.0

    elif judgement in ("GREAT EARLY", "GREAT LATE"):
        accuracy_impact = 0.7

    elif judgement in ("GOOD EARLY", "GOOD LATE"):
        accuracy_impact = 0.4

    elif judgement == "MISS":
        accuracy_impact = 0.0

    if note.note_type == "dual":
        return judgement, note, accuracy_impact

    notes.remove(note)
    return judgement, None, accuracy_impact
