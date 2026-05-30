# main.py
import pygame


# When compile, please merge properly
pygame.init()
screen = pygame.display.set_mode((1333,750))

from gameplay import gameplay
from result import result_screen
from freeplay import freeplay

running = True

while running:

    selected_song = freeplay(screen)
    if selected_song is False:
        break

    accuracy = gameplay(screen, selected_song)

    result_action = result_screen(screen, accuracy)

pygame.quit()