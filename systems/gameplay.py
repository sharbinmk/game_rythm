# gameplay.py
import pygame
import os
from config import *
from notes import *
from judge import *
from chartloader import *
from assets import *
from gameplayui import *
import abilities

ESC_HOLD_LIMIT = 1000


def load_song_settings(selected_song):
    settings_path = os.path.join("charts", selected_song, "settings.py")

    settings = {
        "NOTE_SOUND": True,
        "NOTE_SPEED": NOTE_SPEED,
        "LEAD_IN": 2250,
        "SCORE_BOOST": 1.0,
        "MISS_SCORE": 0.0,
        "DUAL_SCORE": 0.85

    }

    if os.path.exists(settings_path):
        song_settings = {}

        with open(settings_path, "r") as f:
            exec(f.read(), song_settings)

        settings["NOTE_SOUND"] = song_settings.get("NOTE_SOUND", settings["NOTE_SOUND"])
        settings["NOTE_SPEED"] = song_settings.get("NOTE_SPEED", settings["NOTE_SPEED"])
        settings["LEAD_IN"] = song_settings.get("LEAD_IN", settings["LEAD_IN"])
        settings["SCORE_BOOST"] = song_settings.get("SCORE_BOOST", settings["SCORE_BOOST"])
        settings["MISS_SCORE"] = song_settings.get("MISS_SCORE", settings["MISS_SCORE"])
        settings["DUAL_SCORE"] = song_settings.get("DUAL_SCORE", settings["DUAL_SCORE"])

    return settings


def gameplay(screen, selected_song, speed_mult=1.0, time_limit=None):
    clock = pygame.time.Clock()

    # Reset ability charges each run
    abilities.ability_charges = 20

    # Reset all UI state
    judgements.clear()
    sparkles.clear()
    hit_particles.clear()

    accuracy = 100.0
    esc_held = False
    esc_hold_start = 0
    total_score = 0
    total_notes = 0
    force_fail = False

    # Load song-specific settings
    song_settings = load_song_settings(selected_song)

    note_sound_on = song_settings["NOTE_SOUND"]
    effective_speed = song_settings["NOTE_SPEED"] * speed_mult
    lead_in_value = song_settings["LEAD_IN"]
    score_boost = song_settings["SCORE_BOOST"]
    miss_score = song_settings["MISS_SCORE"]
    dual_score = song_settings["DUAL_SCORE"]

    # Count-in
    countin_sound.play()
    countin_start = pygame.time.get_ticks()
    countin_dur = int(countin_sound.get_length() * 1000)

    while pygame.time.get_ticks() - countin_start < countin_dur:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        _draw_gameplay_frame(screen, [], 100.0, 0, {"scale": 1.0, "t": 0})
        pygame.display.flip()
        clock.tick(60)

    # Load chart
    chart_path = os.path.join("charts", selected_song)
    chart = Chart(chart_path)
    chart_notes = chart.notes
    spawn_index = 0

    pygame.mixer.music.load(chart.track)
    pygame.mixer.music.play()

    notes = []
    combo = 0
    combo_anim = {"scale": 1.0, "t": 0}
    running = True
    game_start = pygame.time.get_ticks()

    # Main loop
    while running:
        dt = clock.tick(60)

        # Optional time limit. Story mode uses this. Freeplay does not.
        if time_limit is not None:
            if pygame.time.get_ticks() - game_start >= time_limit:
                running = False

        # Hold ESC to stop and show current result
        if esc_held:
            if pygame.time.get_ticks() - esc_hold_start >= ESC_HOLD_LIMIT:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                force_fail = True
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_held = True
                    esc_hold_start = pygame.time.get_ticks()

                # Top lane: A S D
                if event.key in (pygame.K_a, pygame.K_s, pygame.K_d):
                    result = hit_note(notes, "top")
                    if result:
                        combo, total_notes, total_score, accuracy = _process_hit(
                            result, notes, combo, total_notes, total_score, accuracy,
                            combo_anim, TOP_HIT_POS, note_sound_on, score_boost
                        
                        )

                # Bottom lane: J K L
                if event.key in (pygame.K_j, pygame.K_k, pygame.K_l):
                    result = hit_note(notes, "bottom")
                    if result:
                        combo, total_notes, total_score, accuracy = _process_hit(
                            result, notes, combo, total_notes, total_score, accuracy,
                            combo_anim, BOTTOM_HIT_POS, note_sound_on, score_boost
                        )

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    esc_held = False

        # Spawn notes
        current_time = pygame.mixer.music.get_pos()
        lead_in = lead_in_value

        while spawn_index < len(chart_notes) and current_time >= chart_notes[spawn_index]["time"] - lead_in:
            nt = chart_notes[spawn_index]["type"]

            if nt == "top":
                notes.append(Note("top", upper_note_img, speed=effective_speed))
            elif nt == "bottom":
                notes.append(Note("bottom", lower_note_img, speed=effective_speed))
            elif nt == "dual":
                notes.append(Note("mid", dual_note_img, speed=effective_speed, note_type="dual"))

            spawn_index += 1

        # Update notes
        new_notes = []

        for note in notes:
            note.update()

            if note.x <= MISS_X:
                set_judgement_ui("MISS")
                combo = 0
                total_notes += 1
                total_score += miss_score
                accuracy = (total_score / total_notes) * 100 if total_notes else 100.0
                continue

            if note.note_type == "dual" and note.hit_top and note.hit_bottom and not getattr(note, "dual_scored", False):
                if note_sound_on:
                    note_clap_sound.play()

                combo += 1
                total_notes += 1
                total_score += dual_score
                accuracy = (total_score / total_notes) * 100

                trigger_combo_pop(combo_anim)
                trigger_character_hit()
                spawn_hit_particles(DUAL_HIT_POS)

                note.dual_scored = True
                continue

            new_notes.append(note)

        notes = new_notes

        # Update UI state
        update_judgements()
        update_combo_border(combo)
        update_sparkles()
        update_character()
        _tick_combo_anim(combo_anim)

        # Draw
        # End gameplay when the chart is finished
        if spawn_index >= len(chart_notes) and len(notes) == 0:
            running = False

        # Also stop if the actual song ends
        if not pygame.mixer.music.get_busy():
            running = False

        pygame.mixer.music.fadeout(400)
        return 0.0 if force_fail else accuracy

    pygame.mixer.music.fadeout(400)
    return 0.0 if force_fail else accuracy


def _process_hit(result, notes, combo, total_notes, total_score, accuracy, combo_anim, hit_pos, note_sound_on, score_boost):
    judgement, note_obj, acc = result
    judgement, acc, _ = abilities.ability(judgement, acc)

    if note_obj and note_obj.note_type == "dual":
        note_obj.hit_top = True if hit_pos == TOP_HIT_POS else note_obj.hit_top
        note_obj.hit_bottom = True if hit_pos == BOTTOM_HIT_POS else note_obj.hit_bottom
        return combo, total_notes, total_score, accuracy

    set_judgement_ui(judgement)

    if judgement == "MISS":
        combo = 0
        total_notes += 1
    else:
        if note_sound_on:
            note_clap_sound.play()

        combo += 1
        total_notes += 1
        total_score += min(acc * score_boost, 1.0)

        trigger_combo_pop(combo_anim)
        trigger_character_hit()
        spawn_hit_particles(hit_pos)

    accuracy = (total_score / total_notes) * 100 if total_notes else 100.0
    return combo, total_notes, total_score, accuracy


def _tick_combo_anim(combo_anim):
    if combo_anim["scale"] > 1.0:
        combo_anim["t"] += 0.12
        combo_anim["scale"] = max(1.0, combo_anim["scale"] - combo_anim["t"] * 0.08)


def _draw_gameplay_frame(screen, notes, accuracy, combo, combo_anim):
    draw_BG(screen, TOP_COLOR, BOT_COLOR)
    draw_combo_border(screen)

    screen.blit(bgdeco5, BG5DECO_POS)
    screen.blit(bgdeco1, BG1DECO_POS)
    screen.blit(bgdeco2, BG2DECO_POS)
    screen.blit(bgdeco3, BG3DECO_POS)

    screen.blit(play_area, PLAY_AREA_POS)
    screen.blit(ability_count, ABILITY_COUNT_POS)
    screen.blit(skip_btn, SKIP_BTN_POS)
    screen.blit(accuracy_area, ACCURACY_POS)
    screen.blit(character_placeholder, CHARACTER_PLACEHOLDER_POS)
    draw_character(screen)
    screen.blit(note_area, NOTE_AREA_POS)
    screen.blit(play_area_deco, PLAY_AREA_DECO_POS)
    screen.blit(judgement_img, JUDGEMENT_POS)

    draw_judgements(screen)

    # Accuracy text
    acc_text = acc_font.render(f"{accuracy:.2f}", True, (139, 147, 179))
    screen.blit(acc_text, acc_text.get_rect(center=(1120 + 159 // 2, 27 + 62 // 2)))

    # Ability charges
    ab_text = abil_font.render(str(abilities.ability_charges), True, (139, 147, 179))
    screen.blit(ab_text, ab_text.get_rect(center=(
        ABILITY_COUNT_POS[0] + ability_count.get_width() // 2,
        ABILITY_COUNT_POS[1] + ability_count.get_height() // 2
    )))

    draw_combo(screen, combo, combo_anim)
    draw_sparkles(screen)
    update_hit_particles()
    draw_hit_particles(screen)

    # Notes clipped to play area
    if notes:
        mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))

        for note in notes:
            note.draw(mask)

        screen.set_clip(PLAY_AREA_RECT)
        screen.blit(mask, (0, 0))
        screen.set_clip(None)