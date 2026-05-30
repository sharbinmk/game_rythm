# assets.py
import pygame
import os
from config import *

# Resolve all paths relative to project root (one level up from systems/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def p(path):
    return os.path.join(BASE_DIR, path)

# Playarea and Result UI
play_area = pygame.image.load(p("Assets/PlayArea.png")).convert_alpha()
character_placeholder = pygame.image.load(p("Assets/CharacterPlaceholder.png")).convert_alpha()
judgement_img = pygame.image.load(p("Assets/Judgement.png")).convert_alpha()
note_area = pygame.image.load(p("Assets/NoteArea.png")).convert_alpha()
skip_btn = pygame.image.load(p("Assets/SkipBtn.png")).convert_alpha()
accuracy_area = pygame.image.load(p("Assets/Accuracybg.png")).convert_alpha()
ability_count = pygame.image.load(p("Assets/AbilityCount.png")).convert_alpha()

AccuracyResultArea = pygame.image.load(p("Assets/AccuracyResultArea.png")).convert_alpha()
AccuracyTxt = pygame.image.load(p("Assets/AccuracyTxt.png")).convert_alpha()
ResultArea = pygame.image.load(p("Assets/ResultArea.png")).convert_alpha()
ResultTxt = pygame.image.load(p("Assets/ResultTxt.png")).convert_alpha()
ResultBg = pygame.image.load(p("Assets/ResultBg.png")).convert_alpha()
ResultBgDeco = pygame.image.load(p("Assets/ResultBgDeco.png")).convert_alpha()
ResultExitBtn = pygame.image.load(p("Assets/ResultExitBtn.png")).convert_alpha()

FreeplayWIPtxt = pygame.image.load(p("Assets/FreeplayWIPtxt.png")).convert_alpha()
FreeplayWIPlevel = pygame.image.load(p("Assets/FreeplayWIPlevel.png")).convert_alpha()
FreeplayExitBtn = pygame.image.load(p("Assets/FreeplayExitBtn.png")).convert_alpha()
FreeplaySelectWIP = pygame.image.load(p("Assets/FreeplaySelectWIP.png")).convert_alpha()

# Decos
bgdeco1 = pygame.image.load(p("Assets/bgdeco1.png")).convert_alpha()
bgdeco2 = pygame.image.load(p("Assets/bgdeco2.png")).convert_alpha()
bgdeco3 = pygame.image.load(p("Assets/bgdeco3.png")).convert_alpha()
bgdeco4 = pygame.image.load(p("Assets/bgdeco4.png")).convert_alpha()
bgdeco5 = pygame.image.load(p("Assets/bgdeco5.png")).convert_alpha()
play_area_deco = pygame.image.load(p("Assets/PlayAreaDeco.png")).convert_alpha()

# Notes
upper_note_img = pygame.image.load(p("Assets/UpperNote.png")).convert_alpha()
lower_note_img = pygame.image.load(p("Assets/LowerNote.png")).convert_alpha()
dual_note_img = pygame.image.load(p("Assets/DualNote.png")).convert_alpha()

# Judgements
missjudge_img = pygame.image.load(p("Assets/missjudge.png")).convert_alpha()
goodjudge_img = pygame.image.load(p("Assets/goodjudge.png")).convert_alpha()
greatjudge_img = pygame.image.load(p("Assets/greatjudge.png")).convert_alpha()
perfectjudge_img = pygame.image.load(p("Assets/perfectjudge.png")).convert_alpha()
critperfectjudge_img = pygame.image.load(p("Assets/critperfectjudge.png")).convert_alpha()

# Combo
Combo50 = pygame.image.load(p("Assets/Combo50.png")).convert_alpha()
Combo100 = pygame.image.load(p("Assets/Combo100.png")).convert_alpha()
Combo50Border = pygame.image.load(p("Assets/Combo50Border.png")).convert_alpha()
Combo100Border = pygame.image.load(p("Assets/Combo100Border.png")).convert_alpha()

# Results
SSSrank = pygame.image.load(p("Assets/SSS.png")).convert_alpha()
SSrank = pygame.image.load(p("Assets/SS.png")).convert_alpha()
Srank = pygame.image.load(p("Assets/S.png")).convert_alpha()
Arank = pygame.image.load(p("Assets/A.png")).convert_alpha()
Brank = pygame.image.load(p("Assets/B.png")).convert_alpha()
Crank = pygame.image.load(p("Assets/C.png")).convert_alpha()

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
Sparkle = pygame.image.load(p("Assets/sparkleparticle.png")).convert_alpha()
