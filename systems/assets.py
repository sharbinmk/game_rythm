# assets.py
import pygame
import os
from config import *

pygame.mixer.init()
pygame.font.init()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def p(path):
    return os.path.join(BASE_DIR, path)


# Playarea and Result UI
play_area = pygame.image.load(p("Assets/PlayArea.png"))
character_placeholder = pygame.image.load(p("Assets/CharacterPlaceholder.png"))
judgement_img = pygame.image.load(p("Assets/Judgement.png"))
note_area = pygame.image.load(p("Assets/NoteArea.png"))
skip_btn = pygame.image.load(p("Assets/SkipBtn.png"))
accuracy_area = pygame.image.load(p("Assets/Accuracybg.png"))
ability_count = pygame.image.load(p("Assets/AbilityCount.png"))

AccuracyResultArea = pygame.image.load(p("Assets/AccuracyResultArea.png"))
AccuracyTxt = pygame.image.load(p("Assets/AccuracyTxt.png"))
ResultArea = pygame.image.load(p("Assets/ResultArea.png"))
ResultTxt = pygame.image.load(p("Assets/ResultTxt.png"))
ResultBg = pygame.image.load(p("Assets/ResultBg.png"))
ResultBgDeco = pygame.image.load(p("Assets/ResultBgDeco.png"))
ResultExitBtn = pygame.image.load(p("Assets/ResultExitBtn.png"))

FreeplayWIPtxt = pygame.image.load(p("Assets/FreeplayWIPtxt.png"))
FreeplayWIPlevel = pygame.image.load(p("Assets/FreeplayWIPlevel.png"))
FreeplayExitBtn = pygame.image.load(p("Assets/FreeplayExitBtn.png"))
FreeplaySelectWIP = pygame.image.load(p("Assets/FreeplaySelectWIP.png"))

# Decos
bgdeco1 = pygame.image.load(p("Assets/bgdeco1.png"))
bgdeco2 = pygame.image.load(p("Assets/bgdeco2.png"))
bgdeco3 = pygame.image.load(p("Assets/bgdeco3.png"))
bgdeco4 = pygame.image.load(p("Assets/bgdeco4.png"))
bgdeco5 = pygame.image.load(p("Assets/bgdeco5.png"))
play_area_deco = pygame.image.load(p("Assets/PlayAreaDeco.png"))

# Notes
upper_note_img = pygame.image.load(p("Assets/UpperNote.png"))
lower_note_img = pygame.image.load(p("Assets/LowerNote.png"))
dual_note_img = pygame.image.load(p("Assets/DualNote.png"))

# Judgements
missjudge_img = pygame.image.load(p("Assets/missjudge.png"))
goodjudge_img = pygame.image.load(p("Assets/goodjudge.png"))
greatjudge_img = pygame.image.load(p("Assets/greatjudge.png"))
perfectjudge_img = pygame.image.load(p("Assets/perfectjudge.png"))
critperfectjudge_img = pygame.image.load(p("Assets/critperfectjudge.png"))

# Combo
Combo50 = pygame.image.load(p("Assets/Combo50.png"))
Combo100 = pygame.image.load(p("Assets/Combo100.png"))
Combo50Border = pygame.image.load(p("Assets/Combo50Border.png"))
Combo100Border = pygame.image.load(p("Assets/Combo100Border.png"))

# Results
SSSrank = pygame.image.load(p("Assets/SSS.png"))
SSrank = pygame.image.load(p("Assets/SS.png"))
Srank = pygame.image.load(p("Assets/S.png"))
Arank = pygame.image.load(p("Assets/A.png"))
Brank = pygame.image.load(p("Assets/B.png"))
Crank = pygame.image.load(p("Assets/C.png"))

# Audio
countin_sound = pygame.mixer.Sound(p("Assets/CountIn.wav"))
note_clap_sound = pygame.mixer.Sound(p("Assets/NoteClap.mp3"))
abil_sound = pygame.mixer.Sound(p("Assets/abil.mp3"))
music_path = p("charts/Fraq/track.mp3")

# Font
try:
    c_font = pygame.font.Font(p("Assets/印品鸿蒙体.ttf"), 64)
    font = pygame.font.Font(p("Assets/印品鸿蒙体.ttf"), 36)
    small_font = pygame.font.Font(p("Assets/印品鸿蒙体.ttf"), 24)
    acc_font = pygame.font.Font(p("Assets/印品鸿蒙体.ttf"), 40)
    acc_result_font = pygame.font.Font(p("Assets/印品鸿蒙体.ttf"), 60)
    abil_font = pygame.font.Font(p("Assets/印品鸿蒙体.ttf"), 30)
except FileNotFoundError:
    c_font = pygame.font.SysFont("arial", 64)
    font = pygame.font.SysFont("arial", 36)
    small_font = pygame.font.SysFont("arial", 24)
    acc_font = pygame.font.SysFont("arial", 40)
    acc_result_font = pygame.font.SysFont("arial", 60)
    abil_font = pygame.font.SysFont("arial", 30)

# Particle
Sparkle = pygame.image.load(p("Assets/sparkleparticle.png"))
