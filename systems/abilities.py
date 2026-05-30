# abilities.py

# For future stuff - I won't be limiting this thing to assignment only.
from assets import *
ability_active = True
ability_charges = 20

def ability(judgement, acc):
    global ability_charges

    if ability_active and ability_charges > 0:

        if judgement in ("GREAT EARLY", "GREAT LATE"):

            judgement = "PERFECT EARLY"
            acc = 1.0
            ability_charges -= 1

            abil_sound.play()

            return judgement, acc, True

    return judgement, acc, False