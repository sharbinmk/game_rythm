# freeplay.py

import pygame
import os
import math
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


def menu_font(size, bold=False):
    try:
        return pygame.font.SysFont("georgia", size, bold=bold)
    except:
        return pygame.font.Font(None, size)


def freeplay(screen):
    clock = pygame.time.Clock()
    running = True
    sparkle_timer = 0

    click_sound = load_sound("music/Menu Selection Click.wav", 0.4)
    hover_sound = load_sound("music/Hovering.mp3", 0.25)
    pointer_img = load_pointer()

    button_font = menu_font(42, bold=True)

    # Centered card positions
    card1_pos = (350, 250)   # Normal / Fraq
    card2_pos = (665, 250)   # Hard / Levitating

    card_w = FreeplayWIPlevel.get_width()
    card_h = FreeplayWIPlevel.get_height()

    card1_rect = pygame.Rect(card1_pos[0], card1_pos[1], card_w, card_h)
    card2_rect = pygame.Rect(card2_pos[0], card2_pos[1], card_w, card_h)

    back_rect = pygame.Rect(WIDTH // 2 - 130, 635, 260, 70)

    # 0 = Normal, 1 = Hard, 2 = Back
    selected_index = 0
    last_selected = selected_index

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
                    if selected_index in (0, 1):
                        selected_index = 0
                    else:
                        selected_index = 0

                elif event.key == pygame.K_RIGHT:
                    if selected_index in (0, 1):
                        selected_index = 1
                    else:
                        selected_index = 1

                elif event.key == pygame.K_DOWN:
                    selected_index = 2

                elif event.key == pygame.K_UP:
                    selected_index = 0

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

                    if selected_index == 0:
                        return "Fraq"
                    elif selected_index == 1:
                        return "hard_chapter3_song"
                    elif selected_index == 2:
                        return False

            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()

                if card1_rect.collidepoint(mx, my):
                    selected_index = 0
                elif card2_rect.collidepoint(mx, my):
                    selected_index = 1
                elif back_rect.collidepoint(mx, my):
                    selected_index = 2

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()

                    if card1_rect.collidepoint(mx, my):
                        if click_sound:
                            click_sound.play()
                        return "Fraq"

                    if card2_rect.collidepoint(mx, my):
                        if click_sound:
                            click_sound.play()
                        return "hard_chapter3_song"

                    if back_rect.collidepoint(mx, my):
                        if click_sound:
                            click_sound.play()
                        return False

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

        # Bring back Dylan's top message image
        screen.blit(FreeplayWIPtxt, FREE_PLAY_WIP_TXT)

        # Back button like main menu
        back_selected = selected_index == 2
        back_scale = 1.05 if back_selected else 1.0

        bw = int(back_rect.width * back_scale)
        bh = int(back_rect.height * back_scale)
        draw_back_rect = pygame.Rect(0, 0, bw, bh)
        draw_back_rect.center = back_rect.center

        pygame.draw.rect(screen, (8, 11, 28), draw_back_rect, border_radius=24)
        pygame.draw.rect(screen, (24, 28, 55), draw_back_rect.inflate(-8, -8), border_radius=20)

        back_border = (255, 215, 100) if back_selected else (190, 195, 255)
        pygame.draw.rect(screen, back_border, draw_back_rect, width=2, border_radius=24)

        back_shadow = button_font.render("BACK", True, (30, 30, 60))
        screen.blit(back_shadow, back_shadow.get_rect(center=(draw_back_rect.centerx + 2, draw_back_rect.centery + 2)))

        back_text = button_font.render("BACK", True, (245, 245, 255))
        screen.blit(back_text, back_text.get_rect(center=draw_back_rect.center))

        # Draw cards
        cards = [
            (card1_rect, FreeplayWIPlevel),
            (card2_rect, FreeplayHardlevel),
        ]

        for i, (rect, image) in enumerate(cards):
            if i == selected_index:
                scaled_img = pygame.transform.smoothscale(
                    image,
                    (int(card_w * 1.04), int(card_h * 1.04))
                )
                draw_rect = scaled_img.get_rect(center=rect.center)
                screen.blit(scaled_img, draw_rect)
            else:
                draw_rect = rect
                screen.blit(image, draw_rect)

            # Pointer bounce
            if pointer_img and i == selected_index:
                bounce = int(math.sin(pygame.time.get_ticks() * 0.006) * 4)
                pointer = pygame.transform.smoothscale(pointer_img, (210, 120))

                if i == 0:
                    # Only Normal/Fraq flips from right to left
                    pointer = pygame.transform.flip(pointer, True, False)
                    pointer_rect = pointer.get_rect(
                        midright=(draw_rect.left + 25, draw_rect.centery + bounce)
                    )
                else:
                    # Hard keeps normal pointer
                    pointer_rect = pointer.get_rect(
                        midleft=(draw_rect.right - 25, draw_rect.centery + bounce)
                    )

                screen.blit(pointer, pointer_rect)

        # Pointer for back button
        # Pointer for bottom back button
        if pointer_img and selected_index == 2:
            bounce = int(math.sin(pygame.time.get_ticks() * 0.006) * 4)
            pointer = pygame.transform.smoothscale(pointer_img, (190, 110))
            pointer_rect = pointer.get_rect(
                midleft=(draw_back_rect.right - 15, draw_back_rect.centery + bounce)
            )
            screen.blit(pointer, pointer_rect)

        pygame.display.flip()

    return False