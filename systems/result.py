# result.py
import pygame
from assets import *
from config import *
from gameplayui import *

def get_rank(acc):
    if acc >= 99:   return SSSrank, SSS_RANK_POS
    elif acc >= 95: return SSrank,  SS_RANK_POS
    elif acc >= 90: return Srank,   S_RANK_POS
    elif acc >= 80: return Arank,   A_RANK_POS
    elif acc >= 70: return Brank,   B_RANK_POS
    else:           return Crank,   C_RANK_POS

def result_screen(screen, accuracy):
    clock       = pygame.time.Clock()
    rank_img, rank_pos = get_rank(accuracy)
    blink       = 0
    running     = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return True
                if event.key == pygame.K_ESCAPE:
                    return True

        draw_BG(screen, TOP_COLOR, BOT_COLOR)
        screen.blit(bgdeco1, BG1DECO_POS)
        screen.blit(bgdeco2, BG2DECO_POS)
        screen.blit(bgdeco3, BG3DECO_POS)
        screen.blit(bgdeco4, BG4DECO_POS)
        screen.blit(bgdeco5, BG5DECO_POS)

        screen.blit(ResultBg,      RESULT_BG_POS)
        screen.blit(ResultBgDeco,  RESULT_BG_DECO_POS)
        screen.blit(AccuracyResultArea, ACCURACY_RESULT_AREA_POS)
        screen.blit(AccuracyTxt,   ACCURACY_TXT_POS)
        screen.blit(ResultArea,    RESULT_AREA_POS)
        screen.blit(ResultTxt,     RESULT_TXT_POS)
        screen.blit(ResultExitBtn, RESULT_EXT_BTN_POS)

        acc_text = acc_result_font.render(f"{accuracy:.2f}%", True, (255, 255, 255))
        screen.blit(acc_text, acc_text.get_rect(center=(
            ACCURACY_RESULT_AREA_POS[0] + AccuracyResultArea.get_width()  // 2,
            ACCURACY_RESULT_AREA_POS[1] + AccuracyResultArea.get_height() // 2
        )))

        screen.blit(rank_img, rank_pos)

        # Blinking prompt
        blink = (blink + 1) % 80
        if blink < 50:
            try:
                prompt_font = pygame.font.SysFont("georgia", 22)
                screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT - 36)))
            except:
                pass

        pygame.display.flip()
        clock.tick(60)

    return True
