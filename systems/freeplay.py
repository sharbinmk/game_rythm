# freeplay.py

import pygame
from assets import *
from config import *
from gameplayui import *

def freeplay(screen):
    clock = pygame.time.Clock()
    running = True
    sparkle_timer = 0

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
                if event.key == pygame.K_SPACE:
                    return False

                if event.key == pygame.K_1:
                    return "Fraq"

                if event.key == pygame.K_2:
                    return "hard_chapter3_song"

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

        screen.blit(FreeplaySelectWIP, FREE_PLAY_SELECT_POS)

        # Simple difficulty text
        title = font.render("FREEPLAY", True, (230, 230, 255))
        normal = small_font.render("Press 1 - Normal", True, (200, 200, 255))
        hard = small_font.render("Press 2 - Hard", True, (255, 220, 120))
        back = small_font.render("Press Space - Back", True, (220, 220, 220))

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 170)))
        screen.blit(normal, normal.get_rect(center=(WIDTH // 2, 260)))
        screen.blit(hard, hard.get_rect(center=(WIDTH // 2, 310)))
        screen.blit(back, back.get_rect(center=(WIDTH // 2, 390)))

        screen.blit(FreeplayExitBtn, FREE_PLAY_EXIT_BTN)

        pygame.display.flip()

    return False