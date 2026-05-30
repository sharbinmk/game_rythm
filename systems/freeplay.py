# freeplay.py

import pygame
from assets import *
from config import *
from gameplayui import *

def freeplay(screen):
    clock = pygame.time.Clock()
    running = True
    sparkle_timer = 0

    # Centered card positions
    card1_pos = (330, 230)   # Fraq
    card2_pos = (690, 230)   # Chapter 3 Hard

    # Back button
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
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_1:
                    return "Fraq"

                if event.key == pygame.K_2:
                    return "hard_chapter3_song"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()

                    if back_rect.collidepoint(mx, my):
                        return False

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

        # Dylan's original freeplay background images
        screen.blit(FreeplaySelectWIP, FREE_PLAY_SELECT_POS)
        screen.blit(FreeplayWIPtxt, FREE_PLAY_WIP_TXT)

        # Back button top-left
        pygame.draw.rect(screen, (20, 24, 50), back_rect, border_radius=20)
        pygame.draw.rect(screen, (190, 195, 255), back_rect, width=2, border_radius=20)

        back_text = font.render("BACK", True, (245, 245, 255))
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

        # Title
        title = font.render("FREEPLAY", True, (230, 230, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 145)))

        # Left side hint
        left_hint = font.render("PRESS 1", True, (80, 90, 130))
        screen.blit(left_hint, left_hint.get_rect(center=(210, 345)))

        # Right side hint
        right_hint = font.render("PRESS 2", True, (80, 90, 130))
        screen.blit(right_hint, right_hint.get_rect(center=(1120, 345)))

        # Card 1 - Fraq
        card1 = FreeplayWIPlevel.copy()
        screen.blit(card1, card1_pos)

        fraq_press = small_font.render("Press 1", True, (230, 230, 255))
        fraq_song = small_font.render("Fraq", True, (255, 255, 255))
        fraq_mode = small_font.render("Normal", True, (200, 200, 255))

        screen.blit(fraq_press, fraq_press.get_rect(center=(card1_pos[0] + 175, card1_pos[1] + 310)))
        screen.blit(fraq_song, fraq_song.get_rect(center=(card1_pos[0] + 175, card1_pos[1] + 350)))
        screen.blit(fraq_mode, fraq_mode.get_rect(center=(card1_pos[0] + 175, card1_pos[1] + 385)))

        # Card 2 - Chapter 3 Hard
        card2 = FreeplayWIPlevel.copy()
        screen.blit(card2, card2_pos)

        hard_press = small_font.render("Press 2", True, (255, 230, 160))
        hard_song = small_font.render("Chapter 3", True, (255, 255, 255))
        hard_mode = small_font.render("Hard", True, (255, 220, 120))

        screen.blit(hard_press, hard_press.get_rect(center=(card2_pos[0] + 175, card2_pos[1] + 310)))
        screen.blit(hard_song, hard_song.get_rect(center=(card2_pos[0] + 175, card2_pos[1] + 350)))
        screen.blit(hard_mode, hard_mode.get_rect(center=(card2_pos[0] + 175, card2_pos[1] + 385)))

        pygame.display.flip()

    return False