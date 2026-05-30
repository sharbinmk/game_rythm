# gameplayui.py
import pytweening
import pygame
import random
import math
from assets import *

FADE_IN_END = 0.25
HOLD_END    = 0.65

sparkles      = []
hit_particles = []
judgements    = []

combo_border_alpha_50  = 0
combo_border_alpha_100 = 0
sparkle_timer = 0

# ── Pre-bake gradient surface so draw_BG is O(1) not O(HEIGHT) ───────────────
_grad_cache = {}

def _get_grad_surf(width, height, top_color, bot_color):
    key = (width, height, top_color, bot_color)
    if key not in _grad_cache:
        surf = pygame.Surface((width, height))
        for y in range(height):
            t = y / height
            r = int(top_color[0] * (1 - t) + bot_color[0] * t)
            g = int(top_color[1] * (1 - t) + bot_color[1] * t)
            b = int(top_color[2] * (1 - t) + bot_color[2] * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (width, y))
        _grad_cache[key] = surf
    return _grad_cache[key]

def draw_BG(surface, top_color, bottom_color):
    surf = _get_grad_surf(surface.get_width(), surface.get_height(), top_color, bottom_color)
    surface.blit(surf, (0, 0))

# ── Tweening ─────────────────────────────────────────────────────────────────
def get_tween(progress):
    return pytweening.easeOutQuad(progress)

# ── Judgement display ─────────────────────────────────────────────────────────
def set_judgement_ui(result):
    if result in ("GOOD EARLY", "GOOD LATE"):
        img = goodjudge_img;        pos = (120, 340)
    elif result in ("GREAT EARLY", "GREAT LATE"):
        img = greatjudge_img;       pos = (126, 341)
    elif result in ("PERFECT EARLY", "PERFECT LATE"):
        img = perfectjudge_img;     pos = (104, 339)
    elif result == "CRITICAL":
        img = critperfectjudge_img; pos = (75,  318)
    elif result == "MISS":
        img = missjudge_img;        pos = (126, 341)
    else:
        return

    judgements.append({
        "img":      img,
        "base_pos": pos,
        "start_y":  pos[1] + 40,
        "target_y": pos[1],
        "t": 0
    })

def update_judgements():
    keep = []
    for j in judgements:
        j["t"] += 0.055
        t = min(j["t"], 1.0)
        progress = min(t / FADE_IN_END, 1.0)
        ease = get_tween(progress)
        y = j["start_y"] + (j["target_y"] - j["start_y"]) * ease

        if t < FADE_IN_END:
            alpha = int(255 * (t / FADE_IN_END))
        elif t < HOLD_END:
            alpha = 255
        else:
            fade_t = (t - HOLD_END) / (1.0 - HOLD_END)
            alpha = int(255 * (1.0 - fade_t))

        img = j["img"].copy()
        img.set_alpha(alpha)
        j["draw_img"]   = img
        j["render_pos"] = (j["base_pos"][0], y)
        if t < 1.0:
            keep.append(j)
    judgements.clear()
    judgements.extend(keep)

def draw_judgements(screen):
    for j in judgements:
        screen.blit(j["draw_img"], j["render_pos"])

# ── Combo pop ─────────────────────────────────────────────────────────────────
def trigger_combo_pop(combo_anim):
    combo_anim["scale"] = 1.22
    combo_anim["t"]     = 0

def render_combo(combo):
    if combo >= 100:
        return Combo100, c_font.render(str(combo), True, (255, 215, 100))
    elif combo >= 50:
        return Combo50, c_font.render(str(combo), True, (255, 255, 255))
    elif combo >= 5:
        return None, c_font.render(str(combo), True, (255, 255, 255))
    else:
        return None, None

def draw_combo(screen, combo, combo_anim):
    image, text = render_combo(combo)
    scale = combo_anim["scale"]

    if image:
        iw, ih = image.get_size()
        scaled = pygame.transform.smoothscale(image, (int(iw * scale), int(ih * scale)))
        screen.blit(scaled, scaled.get_rect(center=COMBO_POS))

    if text:
        tw, th = text.get_size()
        scaled = pygame.transform.smoothscale(text, (int(tw * scale), int(th * scale)))
        screen.blit(scaled, scaled.get_rect(center=COMBO_TEXT_POS))

# ── Combo border ──────────────────────────────────────────────────────────────
def update_combo_border(combo):
    global combo_border_alpha_50, combo_border_alpha_100, sparkle_timer
    spd = 10
    if sparkle_timer > 0:
        sparkle_timer -= 1

    if 50 <= combo < 100:
        combo_border_alpha_50 = min(100, combo_border_alpha_50 + spd)
    else:
        combo_border_alpha_50 = max(0, combo_border_alpha_50 - spd)
        if combo < 10:
            sparkles.clear()

    if combo >= 100:
        combo_border_alpha_100 = min(100, combo_border_alpha_100 + spd)
        if sparkle_timer == 0:
            spawn_border_sparkles()
            sparkle_timer = 10
    else:
        combo_border_alpha_100 = max(0, combo_border_alpha_100 - spd)
        if combo < 15:
            sparkles.clear()

def draw_combo_border(screen):
    if combo_border_alpha_50 > 0:
        b = Combo50Border.copy()
        b.set_alpha(combo_border_alpha_50)
        screen.blit(b, (0, 0))
    if combo_border_alpha_100 > 0:
        b = Combo100Border.copy()
        b.set_alpha(combo_border_alpha_100)
        screen.blit(b, (0, 0))

# ── Sparkles ──────────────────────────────────────────────────────────────────
class SparkleParticle:
    def __init__(self, x, y, direction):
        self.x = x + random.randint(-50, 50)
        self.y = y
        self.size      = random.randint(16, 32)
        self.speed     = random.uniform(1.2, 2.8)
        self.life      = 60
        self.base_alpha = random.randint(70, 90)
        self.alpha     = self.base_alpha
        self.direction = direction

    def update(self):
        self.y += self.speed if self.direction == "down" else -self.speed
        self.life  -= 1
        self.alpha  = int(self.base_alpha * (self.life / 60))

    def draw(self, screen):
        img = pygame.transform.smoothscale(Sparkle.copy(), (int(self.size), int(self.size)))
        img.set_alpha(self.alpha)
        screen.blit(img, (self.x, self.y))

def spawn_border_sparkles():
    for _ in range(5):
        sparkles.append(SparkleParticle(random.randint(0, WIDTH), 10, "down"))
    for _ in range(5):
        sparkles.append(SparkleParticle(random.randint(0, WIDTH), HEIGHT - 10, "up"))

def update_sparkles():
    i = 0
    while i < len(sparkles):
        sparkles[i].update()
        if sparkles[i].life <= 0:
            sparkles.pop(i)
        else:
            i += 1

def draw_sparkles(screen):
    for s in sparkles:
        s.draw(screen)

# ── Hit particles ─────────────────────────────────────────────────────────────
class HitParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle      = random.uniform(0, math.pi * 2)
        speed      = random.uniform(1.8, 5.5)
        self.vx    = math.cos(angle) * speed
        self.vy    = math.sin(angle) * speed
        self.size  = random.randint(24, 38)
        self.life  = 22
        self.alpha = 255

    def update(self):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.18   # light gravity
        self.life -= 1
        self.alpha = int(255 * (self.life / 22))
        self.size *= 0.95

    def draw(self, screen):
        if self.size < 1:
            return
        img = pygame.transform.smoothscale(Sparkle.copy(), (int(self.size), int(self.size)))
        img.set_alpha(self.alpha)
        screen.blit(img, (self.x, self.y))

def spawn_hit_particles(pos, amount=16):
    for _ in range(amount):
        hit_particles.append(HitParticle(pos[0], pos[1]))

def update_hit_particles():
    i = 0
    while i < len(hit_particles):
        hit_particles[i].update()
        if hit_particles[i].life <= 0:
            hit_particles.pop(i)
        else:
            i += 1

def draw_hit_particles(screen):
    for p in hit_particles:
        p.draw(screen)

# ── Character animation ───────────────────────────────────────────────────────
# The character sits inside / over the CharacterPlaceholder box at (84, 183), 200×200
# We scale both poses to fit neatly in that zone and draw them centered on it.

CHAR_CENTER_X = 84 + 100   # placeholder center x
CHAR_BOTTOM_Y = 183 + 210  # sit character just above/at bottom of box

_char_hit_timer  = 0        # frames remaining in hit pose
_CHAR_HIT_FRAMES = 18       # how long the hit pose holds

# Pre-scaled pose surfaces — built lazily on first call so pygame is ready
_char_idle_surf = None
_char_hit_surf  = None
_char_scale_h   = 190       # target height (fits inside placeholder)

def _get_char_surfs():
    global _char_idle_surf, _char_hit_surf
    if _char_idle_surf is None:
        from assets import ino_idle, ino_hit
        def _scale(img, target_h):
            w, h = img.get_size()
            scale = target_h / h
            return pygame.transform.smoothscale(img, (int(w * scale), target_h))
        _char_idle_surf = _scale(ino_idle, _char_scale_h)
        _char_hit_surf  = _scale(ino_hit,  _char_scale_h)
    return _char_idle_surf, _char_hit_surf

def trigger_character_hit():
    global _char_hit_timer
    _char_hit_timer = _CHAR_HIT_FRAMES

def update_character():
    global _char_hit_timer
    if _char_hit_timer > 0:
        _char_hit_timer -= 1

def draw_character(screen):
    idle, hit = _get_char_surfs()
    # Subtle idle bob
    bob = int(math.sin(pygame.time.get_ticks() * 0.003) * 3)

    if _char_hit_timer > 0:
        # Hit pose: slight upward pop
        pop = int(pytweening.easeOutQuad(min(_char_hit_timer / _CHAR_HIT_FRAMES, 1.0)) * 8)
        surf = hit
        y_offset = -pop
    else:
        surf = idle
        y_offset = bob

    rect = surf.get_rect(midbottom=(CHAR_CENTER_X, CHAR_BOTTOM_Y + y_offset))
    screen.blit(surf, rect)
