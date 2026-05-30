# freeplay.py

import pygame
import os
from assets import *
from config import *
from gameplayui import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_sound(path, vol=0.4):
    try:
        s = pygame.mixer.Sound(os.path.join(BASE_DIR, path))
        s.set_volume(vol)
        return s
    except:
        return None

def load_pointer():
    try:
        return pygame.image.load(os.path.join(BASE_DIR, "Assets/ui/Pointer.png")).convert_alpha()
    except:
        return None

def freeplay(screen):
    clock = pygame.time.Clock()
    running = True
    sparkle_timer = 0

    click_sound = load_sound("music/Menu Selection Click.wav", 0.4)
    hover_sound = load_sound("music/Hovering.mp3", 0.25)
    pointer_img = load_pointer()

    # Centered card positions
    card1_pos = (350, 250)   # Normal / Fraq
    card2_pos = (665, 250)   # Hard / Levitating

    card_w = FreeplayWIPlevel.get_width()
    card_h = FreeplayWIPlevel.get_height()

    card1_rect = pygame.Rect(card1_pos[0], card1_pos[1], card_w, card_h)
    card2_rect = pygame.Rect(card2_pos[0], card2_pos[1], card_w, card_h)

    cards = [
        {
            "rect": card1_rect,
            "image": FreeplayWIPlevel,
            "song": "Fraq",
        },
        {
            "rect": card2_rect,
            "image": FreeplayHardlevel,
            "song": "hard_chapter3_song",
        }
    ]

    selected_index = 0
    last_selected = -1

    back_rect = pygame.Rect(35, 35, 180, 60)

    while running:
        sparkle_timer -= 1

        if sparkle_timer <= 0:
            spawn_border_sparkles()
            sparkle_timer = 10

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    if click_sound:
                        click_sound.play()
                    return False

                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(cards)

                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(cards)

                elif event.key == pygame.K_1:
                    if click_sound:
                        click_sound.play()
                    return "Fraq"

                elif event.key == pygame.K_2:
                    if click_sound:
                        click_sound.play()
                    return "hard_chapter3_song"

                elif event.key == pygame.K_RETURN:
                    if click_sound:
                        click_sound.play()
                    return cards[selected_index]["song"]

            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()

                for i, card in enumerate(cards):
                    if card["rect"].collidepoint(mx, my):
                        selected_index = i

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()

                    if back_rect.collidepoint(mx, my):
                        if click_sound:
                            click_sound.play()
                        return False

                    for card in cards:
                        if card["rect"].collidepoint(mx, my):
                            if click_sound:
                                click_sound.play()
                            return card["song"]

        if selected_index != last_selected:
            if hover_sound:
                hover_sound.play()
            last_selected = selected_index

        # Background
        draw_BG(screen, TOP_COLOR, BOT_COLOR)

        border = Combo100Border.copy()
        border.set_alpha(80)
        screen.blit(border, (0, 0))

        update_sparkles()
        draw_sparkles(screen)

        screen.blit(bgdeco1, BG1DECO_POS)
        screen.blit(bgdeco2, BG2DECO_POS)
        screen.blit(bgdeco3, BG3DECO_POS)
        screen.blit(bgdeco4, BG4DECO_POS)
        screen.blit(bgdeco5, BG5DECO_POS)

        # Bring back Dylan's top freeplay message
        screen.blit(FreeplayWIPtxt, FREE_PLAY_WIP_TXT)

        # Back button
        pygame.draw.rect(screen, (20, 24, 50), back_rect, border_radius=20)
        pygame.draw.rect(screen, (190, 195, 255), back_rect, width=2, border_radius=20)

        back_text = font.render("BACK", True, (245, 245, 255))
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

        # Draw cards
        for i, card in enumerate(cards):
            rect = card["rect"]

            if i == selected_index:
                scaled_img = pygame.transform.smoothscale(
                    card["image"],
                    (int(card_w * 1.04), int(card_h * 1.04))
                )
                draw_rect = scaled_img.get_rect(center=rect.center)
                screen.blit(scaled_img, draw_rect)

                # Pointer
                if pointer_img:
                    pointer = pygame.transform.smoothscale(pointer_img, (210, 120))

                    if i == 0:
                        # Normal/Fraq selected: flip pointer and put it on the left
                        pointer = pygame.transform.flip(pointer, True, False)
                        pointer_rect = pointer.get_rect(midright=(draw_rect.left + 25, draw_rect.centery))
                    else:
                        # Hard selected: normal pointer on the right
                        pointer_rect = pointer.get_rect(midleft=(draw_rect.right - 25, draw_rect.centery))

                    screen.blit(pointer, pointer_rect)

            else:
                screen.blit(card["image"], rect)

        pygame.display.flip()

    return False