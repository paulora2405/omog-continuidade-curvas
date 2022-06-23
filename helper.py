import pygame
from colors import *
from typing import Tuple


def render_hotkeys(screen: pygame.Surface):
    font_size = 14
    font = pygame.font.Font('freesansbold.ttf', font_size)
    hotkeys = [
        'Space - Switch Curve',
        'Mouse Left - Add or move CP',
        'Mouse Right - Remove CP',
        'C - Increase Continuity',
        'S - Clear CPs',
        'A - Decrease Degree',
        'D - Increase Degree',
    ]
    hotkeys.reverse()
    for i, hotkey in enumerate(hotkeys):
        render_text(hotkey, (0, screen.get_size()
                             [1] - i * font_size), screen, font, black, center=False)


def render_text(text: str, pos: Tuple[int, int], screen: pygame.Surface, font: pygame.font.Font, color: Tuple[int, int, int], center=True):
    textRender = font.render(text, True, color)
    textRect = textRender.get_rect()
    if center:
        textRect.center = pos
    else:
        textRect.bottomleft = pos
    screen.blit(textRender, textRect)
