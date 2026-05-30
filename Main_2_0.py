# Main_2_0.py  —  Moon Rhythm  (Story overhaul)

#Hello
import pygame
import random
import math
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "systems"))

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1333, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Rhythm")
clock = pygame.time.Clock()

from gameplay import gameplay
from result import result_screen
from freeplay import freeplay

# ─── Audio ───────────────────────────────────────────────────────────────────
def _load_sound(path, vol=0.4):
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(vol)
        return s
    except:
        return None

click_sound = _load_sound("music/Menu Selection Click.wav", 0.4)
hover_sound = _load_sound("music/Hovering.mp3", 0.25)

try:
    pygame.mixer.music.load("music/Background_Music.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)
except:
    pass

# ─── Fonts ────────────────────────────────────────────────────────────────────
def _font(size, bold=False):
    try:
        name = "georgia"
        return pygame.font.SysFont(name, size, bold=bold)
    except:
        return pygame.font.Font(None, size)

title_font   = _font(52, bold=True)
page_font    = _font(44, bold=True)
button_font  = _font(38, bold=True)
small_font   = _font(22)
story_font   = _font(26)
tiny_font    = _font(18)

# ─── Colours ──────────────────────────────────────────────────────────────────
WHITE    = (245, 245, 255)
LAVENDER = (185, 190, 255)
GOLD     = (255, 215, 100)
DARK     = (12,  15,  32)
PANEL    = (10,  14,  35, 180)
TEAL     = (100, 220, 200)
PINK     = (255, 160, 200)

# ─── Background ───────────────────────────────────────────────────────────────
try:
    bg_raw = pygame.image.load("Assets/ui/Main_Menu.png").convert()
    bg = pygame.transform.scale(bg_raw, (WIDTH, HEIGHT))
except:
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(DARK)

try:
    pointer_img = pygame.image.load("Assets/ui/Pointer.png").convert_alpha()
except:
    pointer_img = None

# ─── Stars ────────────────────────────────────────────────────────────────────
class Star:
    def __init__(self):
        self.reset(random.randint(0, WIDTH))

    def reset(self, x=None):
        self.x = x if x is not None else WIDTH + 10
        self.y = random.uniform(0, HEIGHT)
        self.size = random.choice([1, 1, 1, 2, 2, 3])
        self.speed = random.uniform(0.1, 0.45)
        self.twinkle = random.uniform(0, math.pi * 2)
        self.twinkle_speed = random.uniform(0.02, 0.06)
        self.base_alpha = random.randint(140, 255)

    def update(self):
        self.x -= self.speed
        self.twinkle += self.twinkle_speed
        if self.x < -10:
            self.reset()

    def draw(self, surf):
        alpha = int(self.base_alpha * (0.6 + 0.4 * math.sin(self.twinkle)))
        col = (
            min(255, WHITE[0]),
            min(255, int(WHITE[1] * (alpha / 255))),
            min(255, int(WHITE[2] * (alpha / 255))),
        )
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.size)

stars = [Star() for _ in range(160)]

def draw_stars():
    for s in stars:
        s.update()
        s.draw(screen)

# ─── Smooth gradient BG ───────────────────────────────────────────────────────
_grad_surf = pygame.Surface((WIDTH, HEIGHT))
for _y in range(HEIGHT):
    _t = _y / HEIGHT
    _r = int(0x0c * (1 - _t) + 0x03 * _t)
    _g = int(0x0e * (1 - _t) + 0x06 * _t)
    _b = int(0x24 * (1 - _t) + 0x10 * _t)
    pygame.draw.line(_grad_surf, (_r, _g, _b), (0, _y), (WIDTH, _y))

def draw_bg_layer():
    screen.blit(bg, (0, 0))
    screen.blit(_grad_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# ─── Floating orbs ────────────────────────────────────────────────────────────
class Orb:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.r = random.randint(40, 100)
        self.alpha = random.randint(8, 22)
        self.phase = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.005, 0.015)
        self.col = random.choice([LAVENDER, TEAL, PINK, GOLD])
        self.drift_x = random.uniform(-0.15, 0.15)
        self.drift_y = random.uniform(-0.08, 0.08)

    def update(self):
        self.phase += self.speed
        self.x += self.drift_x + math.sin(self.phase) * 0.3
        self.y += self.drift_y + math.cos(self.phase * 0.7) * 0.2
        if self.x < -120: self.x = WIDTH + 120
        if self.x > WIDTH + 120: self.x = -120
        if self.y < -120: self.y = HEIGHT + 120
        if self.y > HEIGHT + 120: self.y = -120

    def draw(self, surf):
        s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.col, self.alpha), (self.r, self.r), self.r)
        surf.blit(s, (int(self.x - self.r), int(self.y - self.r)))

orbs = [Orb() for _ in range(12)]

def draw_orbs():
    for o in orbs:
        o.update()
        o.draw(screen)

# ─── Helper: draw translucent panel ──────────────────────────────────────────
def draw_panel(x, y, w, h, alpha=180, border_col=LAVENDER, radius=22):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (8, 11, 28, alpha), s.get_rect(), border_radius=radius)
    pygame.draw.rect(s, (*border_col, 140), s.get_rect(), width=2, border_radius=radius)
    screen.blit(s, (x, y))

def draw_text_shadow(font, text, color, pos, shadow_col=(0,0,0), offset=2):
    sx, sy = pos
    shadow = font.render(text, True, shadow_col)
    screen.blit(shadow, (sx + offset, sy + offset))
    surf = font.render(text, True, color)
    screen.blit(surf, (sx, sy))
    return surf.get_rect(topleft=pos)

# ─── Story data ───────────────────────────────────────────────────────────────
# Three chapters, each with an intro + outro cutscene
STORY_CHAPTERS = [
    {
        "id": 1,
        "title": "Chapter 1: The First Note",
        "subtitle": "Every journey begins with a single sound.",
        "chart": "Fraq",
        "speed_mult": 1.0,
        "density": 1.0,
        "pass_acc": 60.0,
        "intro": [
            "Ino grew up in a small coastal town where the wind sang through the reeds at dusk.",
            "One evening, an old musician passed through and played a melody so beautiful",
            "that Ino wept without knowing why.",
            "",
            "That night, Ino made a decision:",
            "\"I will travel the world. I will become a musician.\"",
            "",
            "The road ahead is long. But every legend starts somewhere.",
            "Press ENTER to begin your first performance.",
        ],
        "outro_pass": [
            "The crowd fell silent after the last note faded.",
            "Then — applause. Scattered at first, then thunderous.",
            "",
            "Ino bowed, heart racing. It was rough, but it was real.",
            "\"You have potential,\" whispered an elder in the crowd.",
            "\"Keep going.\"",
        ],
        "outro_fail": [
            "The notes scattered like startled birds.",
            "Ino stumbled, lost the rhythm, and the music collapsed.",
            "",
            "A gentle voice spoke from the crowd:",
            "\"Even the greatest musicians fell first. Try again.\"",
        ],
    },
    {
        "id": 2,
        "title": "Chapter 2: The Mountain Stage",
        "subtitle": "The higher you climb, the colder the air.",
        "chart": "Fraq",
        "speed_mult": 1.2,
        "density": 1.0,
        "pass_acc": 70.0,
        "intro": [
            "Months have passed. Ino's fingers have grown callused,",
            "and the melodies come easier now.",
            "",
            "Word spread of a festival high in the mountain village of Kelara.",
            "Musicians from three kingdoms compete there for the Silver Reed —",
            "an instrument said to amplify the soul of its player.",
            "",
            "Ino arrives at dusk, watching rivals who have trained for years.",
            "Doubt creeps in. But so does determination.",
            "",
            "The stage is yours. Press ENTER.",
        ],
        "outro_pass": [
            "Ino's performance cut through the mountain air like a clear bell.",
            "The Silver Reed judges exchanged glances.",
            "",
            "\"This one,\" said the eldest judge, \"plays not just notes —",
            "but feeling.\"",
            "",
            "Ino did not win the Reed. But earned something rarer:",
            "an invitation to the Grand Conservatory of the Eastern Coast.",
        ],
        "outro_fail": [
            "The mountain wind was merciless, drowning out the hesitation in Ino's playing.",
            "The judges shook their heads.",
            "",
            "A rival musician placed a hand on Ino's shoulder.",
            "\"The mountain does not care about ambition. Only precision.\"",
            "\"Come back when you are ready.\"",
        ],
    },
    {
        "id": 3,
        "title": "Chapter 3: The Concert Hall of Stars",
        "subtitle": "Excellence is not a destination. It is a way of moving.",
        "chart": "Fraq",
        "speed_mult": 1.45,
        "density": 1.0,
        "pass_acc": 80.0,
        "intro": [
            "The Grand Conservatory stands on a cliff above the ocean.",
            "Its concert hall has hosted the greatest musicians of three generations.",
            "",
            "Tonight, Ino performs for the first time on its legendary stage.",
            "The audience includes scholars, kings, and wanderers alike.",
            "All of them here for one thing: music that moves the stars.",
            "",
            "Ino stands in the wings, breathing slowly.",
            "This is what the journey was for.",
            "",
            "Every note. Every stumble. Every dawn practice.",
            "It all leads here.",
            "",
            "Play with everything you have. Press ENTER.",
        ],
        "outro_pass": [
            "The final chord rang out and hung in the air like a held breath.",
            "",
            "Then silence.",
            "Then the entire hall rose to its feet.",
            "",
            "The Conservatory's Grandmaster approached Ino afterward.",
            "\"I have heard ten thousand musicians in this hall,\"",
            "\"and I have never seen someone play like they were healing something.\"",
            "",
            "Ino smiled — not in triumph, but in recognition.",
            "This was not the end of the journey.",
            "This was the beginning of what the journey was for.",
            "",
            "~ Fin ~",
        ],
        "outro_fail": [
            "The hall was patient. The music was not.",
            "",
            "Ino left the stage quietly, walking to the ocean's edge.",
            "The waves were indifferent. The stars, distant.",
            "",
            "But the music was still there — inside, waiting.",
            "\"Excellence is not a destination,\" Ino remembered.",
            "\"It is a way of moving.\"",
            "",
            "Tomorrow, practice begins again.",
        ],
    },
]

# ─── State machine ────────────────────────────────────────────────────────────
MAIN          = "main"
STORY_SELECT  = "story_select"
CUTSCENE      = "cutscene"
LOADING       = "loading"
RESULT_STORY  = "result_story"

state               = MAIN
selected_chapter    = None   # index 0-2
cutscene_lines      = []
cutscene_is_outro   = False
cutscene_pass       = False
last_accuracy       = 0.0
loading_start       = 0
selected_index      = 0
last_mouse          = pygame.mouse.get_pos()
running             = True
chapters_cleared    = [False, False, False]  # track which chapters passed

# ─── Cutscene renderer ────────────────────────────────────────────────────────
_cs_line_index  = 0
_cs_line_timer  = 0
_cs_char_timer  = 0.0
_cs_chars_shown = 0
_cs_all_shown   = False
_cs_blink       = 0

def start_cutscene(lines, is_outro=False, passed=False):
    global cutscene_lines, cutscene_is_outro, cutscene_pass
    global _cs_line_index, _cs_line_timer, _cs_char_timer
    global _cs_chars_shown, _cs_all_shown, _cs_blink
    cutscene_lines   = lines
    cutscene_is_outro = is_outro
    cutscene_pass    = passed
    _cs_line_index   = 0
    _cs_line_timer   = 0
    _cs_char_timer   = 0.0
    _cs_chars_shown  = 0
    _cs_all_shown    = False
    _cs_blink        = 0

def update_cutscene_chars(dt):
    global _cs_chars_shown, _cs_char_timer, _cs_all_shown
    if _cs_all_shown:
        return
    full = "\n".join(cutscene_lines)
    _cs_char_timer += dt * 40   # chars per second
    _cs_chars_shown = min(int(_cs_char_timer), len(full))
    if _cs_chars_shown >= len(full):
        _cs_all_shown = True

def draw_cutscene():
    global _cs_blink
    draw_bg_layer()
    draw_orbs()
    draw_stars()

    chap = STORY_CHAPTERS[selected_chapter] if selected_chapter is not None else None

    # Title bar
    if chap:
        title_str = chap["title"] if not cutscene_is_outro else ("✓ " if cutscene_pass else "✗ ") + chap["title"]
        col = GOLD if (cutscene_is_outro and cutscene_pass) else (PINK if (cutscene_is_outro and not cutscene_pass) else LAVENDER)
        draw_panel(WIDTH//2 - 420, 40, 840, 72, alpha=200, border_col=col)
        t = title_font.render(title_str, True, col)
        screen.blit(t, t.get_rect(center=(WIDTH//2, 76)))

    # Text box
    box_x, box_y, box_w, box_h = 140, 135, WIDTH - 280, HEIGHT - 220
    draw_panel(box_x, box_y, box_w, box_h, alpha=210, border_col=LAVENDER, radius=18)

    # Build visible text from typewriter effect
    full = "\n".join(cutscene_lines)
    visible = full[:_cs_chars_shown] if not _cs_all_shown else full
    lines_visible = visible.split("\n")

    y_off = box_y + 28
    for ln in lines_visible:
        if ln.strip() == "":
            y_off += 18
            continue
        col_ln = GOLD if ln.startswith("~") else WHITE
        surf = story_font.render(ln, True, col_ln)
        screen.blit(surf, (box_x + 32, y_off))
        y_off += 36

    # Prompt
    _cs_blink = (_cs_blink + 1) % 90
    if _cs_all_shown and _cs_blink < 55:
        prompt = "[ENTER] Continue" if not cutscene_is_outro else "[ENTER] Continue  |  [ESC] Chapter Select"
        p_surf = small_font.render(prompt, True, LAVENDER)
        screen.blit(p_surf, p_surf.get_rect(center=(WIDTH//2, HEIGHT - 52)))

def handle_cutscene_input(event):
    global state, _cs_char_timer, _cs_chars_shown, _cs_all_shown
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if not _cs_all_shown:
                # Skip to end
                _cs_char_timer = 99999
                _cs_chars_shown = 99999
                _cs_all_shown = True
            else:
                # Advance
                if cutscene_is_outro:
                    state = STORY_SELECT
                    selected_index_reset()
                else:
                    # Start loading
                    begin_loading()
        if event.key == pygame.K_ESCAPE and cutscene_is_outro:
            state = STORY_SELECT
            selected_index_reset()

# ─── Loading screen ───────────────────────────────────────────────────────────
def begin_loading():
    global state, loading_start
    state = LOADING
    loading_start = pygame.time.get_ticks()

def draw_loading():
    draw_bg_layer()
    draw_orbs()
    draw_stars()

    chap = STORY_CHAPTERS[selected_chapter]
    draw_panel(WIDTH//2 - 280, 290, 560, 170, alpha=210)

    t = page_font.render("LOADING", True, WHITE)
    screen.blit(t, t.get_rect(center=(WIDTH//2, 340)))

    sub = small_font.render(chap["subtitle"], True, LAVENDER)
    screen.blit(sub, sub.get_rect(center=(WIDTH//2, 385)))

    elapsed = pygame.time.get_ticks() - loading_start
    prog = min(elapsed / 1800, 1.0)
    bar_x = WIDTH//2 - 220
    bar_y = 415
    pygame.draw.rect(screen, (20,22,45), (bar_x, bar_y, 440, 18), border_radius=9)
    pygame.draw.rect(screen, LAVENDER, (bar_x, bar_y, int(440 * prog), 18), border_radius=9)
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, 440, 18), width=2, border_radius=9)

# ─── Buttons ──────────────────────────────────────────────────────────────────
class MenuButton:
    def __init__(self, text, x, y, w, h, action, sub=""):
        self.text = text
        self.sub  = sub
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.scale  = 1.0
        self._was_hovered = False

    def draw(self, surface, selected=False):
        hovered = selected
        if hovered and not self._was_hovered and hover_sound:
            hover_sound.play()
        self._was_hovered = hovered

        target = 1.03 if hovered else 1.0
        self.scale += (target - self.scale) * 0.16

        w = int(self.rect.width  * self.scale)
        h = int(self.rect.height * self.scale)
        rect = pygame.Rect(0, 0, w, h)
        rect.center = self.rect.center

        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (8, 11, 28, 220), s.get_rect(), border_radius=28)
        pygame.draw.rect(s, (24, 28, 55, 190), s.get_rect().inflate(-10, -10), border_radius=24)
        border_col = GOLD if hovered else LAVENDER
        pygame.draw.rect(s, border_col, s.get_rect(), width=2, border_radius=28)
        surface.blit(s, rect)

        # Shadow + main text
        shadow = button_font.render(self.text, True, (30, 30, 60))
        surface.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2 - (10 if self.sub else 0))))
        main = button_font.render(self.text, True, WHITE)
        surface.blit(main, main.get_rect(center=(rect.centerx, rect.centery - (10 if self.sub else 0))))

        if self.sub:
            sub_s = tiny_font.render(self.sub, True, LAVENDER)
            surface.blit(sub_s, sub_s.get_rect(center=(rect.centerx, rect.centery + 16)))

        # Pointer
        if hovered and pointer_img:
            fy = int(math.sin(pygame.time.get_ticks() * 0.006) * 4)
            ptr = pygame.transform.smoothscale(pointer_img, (280, 160))
            pr = ptr.get_rect(midleft=(rect.right - 40, rect.centery + fy))
            surface.blit(ptr, pr)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(pygame.mouse.get_pos())
        )

# ─── Chapter card ─────────────────────────────────────────────────────────────
class ChapterButton:
    def __init__(self, chap_idx, x, y, w, h):
        self.idx   = chap_idx
        self.chap  = STORY_CHAPTERS[chap_idx]
        self.rect  = pygame.Rect(x, y, w, h)
        self.scale = 1.0
        self._was  = False

    def draw(self, surface, selected=False):
        if selected and not self._was and hover_sound:
            hover_sound.play()
        self._was = selected

        target = 1.035 if selected else 1.0
        self.scale += (target - self.scale) * 0.16

        w = int(self.rect.width  * self.scale)
        h = int(self.rect.height * self.scale)
        r = pygame.Rect(0, 0, w, h)
        r.center = self.rect.center

        cleared = chapters_cleared[self.idx]
        locked  = self.idx > 0 and not chapters_cleared[self.idx - 1]

        s = pygame.Surface((w, h), pygame.SRCALPHA)
        base_col = (8, 11, 28, 230)
        pygame.draw.rect(s, base_col, s.get_rect(), border_radius=20)

        if cleared:
            border = GOLD
        elif locked:
            border = (60, 60, 90)
        elif selected:
            border = WHITE
        else:
            border = LAVENDER
        pygame.draw.rect(s, border, s.get_rect(), width=2, border_radius=20)

        surface.blit(s, r)

        # Chapter number badge
        num_col = GOLD if cleared else (LAVENDER if not locked else (80, 80, 110))
        num = page_font.render(str(self.chap["id"]), True, num_col)
        surface.blit(num, (r.x + 22, r.y + 14))

        # Title
        col = (180, 180, 180) if locked else WHITE
        t = small_font.render(self.chap["title"], True, col)
        surface.blit(t, (r.x + 18, r.y + 64))

        # Subtitle
        st = tiny_font.render(self.chap["subtitle"], True, LAVENDER if not locked else (70, 70, 100))
        surface.blit(st, (r.x + 18, r.y + 92))

        # Pass accuracy requirement
        req = tiny_font.render(f"Pass: {self.chap['pass_acc']:.0f}%  |  Speed: ×{self.chap['speed_mult']}", True,
                               TEAL if not locked else (60, 60, 90))
        surface.blit(req, (r.x + 18, r.y + 116))

        # Lock / cleared badge
        if locked:
            lk = small_font.render("🔒 LOCKED", True, (100, 100, 130))
            surface.blit(lk, lk.get_rect(midright=(r.right - 16, r.centery)))
        elif cleared:
            lk = small_font.render("★ CLEARED", True, GOLD)
            surface.blit(lk, lk.get_rect(midright=(r.right - 16, r.centery)))

        # Pointer
        if selected and pointer_img:
            fy = int(math.sin(pygame.time.get_ticks() * 0.006) * 4)
            ptr = pygame.transform.smoothscale(pointer_img, (240, 137))
            pr = ptr.get_rect(midleft=(r.right - 30, r.centery + fy))
            surface.blit(ptr, pr)

    def clicked(self, ev):
        return (
            ev.type == pygame.MOUSEBUTTONDOWN
            and ev.button == 1
            and self.rect.collidepoint(pygame.mouse.get_pos())
        )

# ─── Main menu buttons ────────────────────────────────────────────────────────
BW, BH = 520, 85
CX = WIDTH // 2 - BW // 2

def _select_chapter(idx):
    global selected_chapter, state
    chap = STORY_CHAPTERS[idx]
    locked = idx > 0 and not chapters_cleared[idx - 1]
    if locked:
        return
    selected_chapter = idx
    state = CUTSCENE
    start_cutscene(chap["intro"], is_outro=False)

def _open_story():
    global state, selected_index
    state = STORY_SELECT
    selected_index = 0

def _open_freeplay():
    selected_song = freeplay(screen)

    if selected_song:
        pygame.mixer.music.stop()
        acc = gameplay(screen, selected_song)
        result_screen(screen, acc)

        try:
            pygame.mixer.music.load("music/Background_Music.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
        except:
            pass

def _quit():
    global running
    running = False

main_buttons = [
    MenuButton("STORY MODE", CX, 290, BW, BH, _open_story,   sub="Ino's Journey"),
    MenuButton("FREEPLAY",   CX, 410, BW, BH, _open_freeplay, sub="Play any song"),
    MenuButton("QUIT",        CX, 530, BW, BH, _quit),
]

chapter_buttons = [
    ChapterButton(0, WIDTH//2 - 560, 190, 520, 155),
    ChapterButton(1, WIDTH//2 - 560, 370, 520, 155),
    ChapterButton(2, WIDTH//2 - 560, 550, 520, 155),
]

back_btn = MenuButton("BACK", 35, 48, 180, 62, lambda: _go_main())

def _go_main():
    global state, selected_index
    state = MAIN
    selected_index = 0

def selected_index_reset():
    global selected_index
    selected_index = 0

# ─── Draw helpers ─────────────────────────────────────────────────────────────
def draw_version():
    v = tiny_font.render("Moon Rhythm  ·  Ino's Journey  ·  v2.0", True, (80, 80, 110))
    screen.blit(v, (30, HEIGHT - 30))

def draw_title_panel():
    draw_panel(60, 50, 500, 120, alpha=200, border_col=LAVENDER)
    draw_text_shadow(title_font, "MOON RHYTHM", WHITE, (80, 62))
    sub = small_font.render("A rhythm journey across the world", True, LAVENDER)
    screen.blit(sub, (80, 122))
    pygame.draw.line(screen, LAVENDER, (80, 148), (520, 148), 1)

def draw_page_title(title_text, sub_text, col=WHITE):
    draw_panel(WIDTH//2 - 310, 30, 620, 100, alpha=210, border_col=col)
    t = page_font.render(title_text, True, col)
    screen.blit(t, t.get_rect(center=(WIDTH//2, 62)))
    s = small_font.render(sub_text, True, LAVENDER)
    screen.blit(s, s.get_rect(center=(WIDTH//2, 102)))

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""

    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current.strip())
            current = word + " "

    if current:
        lines.append(current.strip())

    return lines

# ─── Story select: right panel showing chapter story preview ──────────────────
def draw_story_panel():
    if 0 <= selected_index < 3:
        chap = STORY_CHAPTERS[selected_index]
        locked = selected_index > 0 and not chapters_cleared[selected_index - 1]
        px, py, pw, ph = WIDTH//2 + 190, 185, 460, 520
        draw_panel(px, py, pw, ph, alpha=200, border_col=GOLD if chapters_cleared[selected_index] else LAVENDER, radius=16)

        screen.blit(small_font.render(chap["title"], True, GOLD), (px + 20, py + 18))
        pygame.draw.line(screen, LAVENDER, (px + 20, py + 48), (px + pw - 20, py + 48), 1)

        if locked:
            lk = page_font.render("LOCKED", True, (80, 80, 120))
            screen.blit(lk, lk.get_rect(center=(px + pw//2, py + ph//2)))
            hint = small_font.render("Complete the previous chapter first.", True, (80, 80, 120))
            screen.blit(hint, hint.get_rect(center=(px + pw//2, py + ph//2 + 44)))
        else:
            preview_lines = chap["intro"][:4]
            y_off = py + 62

            for ln in preview_lines:
                if ln == "":
                    y_off += 14
                    continue

                wrapped = wrap_text(ln, tiny_font, pw - 40)

                for line in wrapped:
                    surf = tiny_font.render(line, True, (160, 165, 210))
                    screen.blit(surf, (px + 20, y_off))
                    y_off += 24

            # Requirements
            y_off = py + ph - 120
            pygame.draw.line(screen, (40, 44, 80), (px + 20, y_off), (px + pw - 20, y_off), 1)
            y_off += 12
            screen.blit(small_font.render(f"Pass accuracy:  {chap['pass_acc']:.0f}%", True, TEAL),    (px + 20, y_off))
            screen.blit(small_font.render(f"Note speed:     ×{chap['speed_mult']}",    True, TEAL),    (px + 20, y_off + 30))
            screen.blit(tiny_font.render("Controls: A/S/D top", True, LAVENDER), (px + 20, y_off + 62))
            screen.blit(tiny_font.render("J/K/L bottom", True, LAVENDER), (px + 20, y_off + 86))

            enter_hint = tiny_font.render("[ENTER] or click to play", True, WHITE)
            screen.blit(enter_hint, enter_hint.get_rect(center=(px + pw//2, py + ph + 22)))

# ─── Screens ──────────────────────────────────────────────────────────────────
def draw_main_menu():
    draw_bg_layer()
    draw_orbs()
    draw_stars()
    draw_title_panel()
    for i, btn in enumerate(main_buttons):
        btn.draw(screen, i == selected_index)
    draw_version()

def draw_story_select():
    draw_bg_layer()
    draw_orbs()
    draw_stars()
    draw_page_title("STORY MODE", "Ino's Journey  —  Choose a Chapter", GOLD)
    for i, btn in enumerate(chapter_buttons):
        btn.draw(screen, i == selected_index)
    back_btn.draw(screen, selected_index == 3)
    draw_story_panel()
    draw_version()

# ─── Active buttons by state ──────────────────────────────────────────────────
def active_buttons():
    if state == MAIN:
        return main_buttons
    if state == STORY_SELECT:
        return list(chapter_buttons) + [back_btn]
    return []

def handle_button_action(btn):
    if click_sound:
        click_sound.play()
    if hasattr(btn, "action"):
        btn.action()
    elif hasattr(btn, "idx"):
        _select_chapter(btn.idx)

# ─── Post-gameplay: result → cutscene ────────────────────────────────────────
def after_gameplay(accuracy):
    global last_accuracy, state
    last_accuracy = accuracy
    chap = STORY_CHAPTERS[selected_chapter]
    passed = accuracy >= chap["pass_acc"]
    if passed:
        chapters_cleared[selected_chapter] = True
    lines = chap["outro_pass"] if passed else chap["outro_fail"]
    state = CUTSCENE
    start_cutscene(lines, is_outro=True, passed=passed)

    # restore menu music
    try:
        pygame.mixer.music.load("music/Background_Music.mp3")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
    except:
        pass

# ─── Main loop ────────────────────────────────────────────────────────────────
dt = 0.0

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # ── Cutscene input
        if state == CUTSCENE:
            handle_cutscene_input(event)
            continue

        # ── Keyboard nav
        btns = active_buttons()
        if event.type == pygame.KEYDOWN and btns:
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(btns)
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(btns)
            elif event.key == pygame.K_RETURN:
                handle_button_action(btns[selected_index])
            elif event.key == pygame.K_ESCAPE:
                if state == STORY_SELECT:
                    _go_main()

        # ── Mouse clicks
        for btn in active_buttons():
            if btn.clicked(event):
                handle_button_action(btn)

    # ── Mouse hover
    if state != CUTSCENE:
        mx, my = pygame.mouse.get_pos()
        if (mx, my) != last_mouse:
            last_mouse = (mx, my)
            for i, btn in enumerate(active_buttons()):
                if btn.rect.collidepoint(mx, my):
                    selected_index = i

    # ── Draw
    if state == MAIN:
        draw_main_menu()
    elif state == STORY_SELECT:
        draw_story_select()
    elif state == CUTSCENE:
        update_cutscene_chars(dt)
        draw_cutscene()
    elif state == LOADING:
        draw_loading()
        if pygame.time.get_ticks() - loading_start > 1800:
            # Launch gameplay
            chap = STORY_CHAPTERS[selected_chapter]
            pygame.mixer.music.stop()
            acc = gameplay(screen, chap["chart"], speed_mult=chap["speed_mult"])
            after_gameplay(acc)

    pygame.display.flip()
    dt = clock.tick(60) / 1000.0

pygame.quit()
