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
        '0 - Continuity C0',
        '1 - Continuity C1',
        '2 - Continuity C2',
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


def render_continuity(continuity: int, screen: pygame.Surface, font: pygame.font.Font, center=True):
    pos = (screen.get_size()[0] // 2, 40)
    colors = [green, purple, violet]
    color = colors[continuity] if continuity != -1 else black
    geometric = False if continuity == 0 else True
    text = 'No Continuity' if continuity == - \
        1 else 'Continuity G' + str(continuity) if geometric else 'Continuity C' + str(continuity)
    textRender = font.render(text, True, color)
    textRect = textRender.get_rect()
    if center:
        textRect.center = pos
    else:
        textRect.bottomleft = pos
    screen.blit(textRender, textRect)
