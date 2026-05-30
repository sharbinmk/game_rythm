# freeplay.py

# For future stuff - I won't be limiting this thing to assignment only.
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
                elif event.key == pygame.K_1:
                    selected_song = "Fraq"
                    return selected_song

        # Background
        draw_BG(screen, TOP_COLOR, BOT_COLOR)

        # bruh too lazy to make a new border with less alpha.
        border = Combo100Border.copy()
        border.set_alpha(80)
        screen.blit(border, (0,0))
        update_sparkles()
        draw_sparkles(screen)
        screen.blit(bgdeco1, BG1DECO_POS)
        screen.blit(bgdeco2, BG2DECO_POS)
        screen.blit(bgdeco3, BG3DECO_POS)
        screen.blit(bgdeco4, BG4DECO_POS)
        screen.blit(bgdeco5, BG5DECO_POS)
        screen.blit(FreeplaySelectWIP, FREE_PLAY_SELECT_POS)

        screen.blit(FreeplayWIPtxt, FREE_PLAY_WIP_TXT)
        screen.blit(FreeplayWIPlevel, FREE_PLAY_WIP_LEVEL)

        # Exit Btn
        screen.blit(FreeplayExitBtn, FREE_PLAY_EXIT_BTN)

        pygame.display.flip()

    return True