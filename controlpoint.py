import pygame
from colors import *
from typing import Tuple


class ControlPoint:
    def __init__(self, x: int, y: int, id: int, color: Tuple[int, int, int], display_id_under=False):
        self.x = x
        self.y = y
        self.id = id
        self.inner_circle = None
        self.outter_circle = None
        self.color = color
        self.display_id_under = display_id_under
        self.font = pygame.font.Font('freesansbold.ttf', 16)

    def get_pos(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_bellow(self, x: int, y: int):
        return self.outter_circle.collidepoint(x, y)

    def draw(self, screen: pygame.Surface):
        text = self.font.render(f'P{self.id}', True, self.color)
        textRect = text.get_rect()
        if self.display_id_under:
            textRect.center = (self.x, self.y + 20)
        else:
            textRect.center = (self.x, self.y - 15)
        screen.blit(text, textRect)

        self.outter_circle = pygame.draw.circle(
            screen, self.color, (self.x, self.y), 10)
        self.inner_circle = pygame.draw.circle(
            screen, grey, (self.x, self.y), 9)
