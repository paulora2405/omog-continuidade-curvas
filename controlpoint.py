import pygame
from colors import *

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 16)


class ControlPoint:
    def __init__(self, x: int, y: int, id: int):
        self.x = x
        self.y = y
        self.id = id
        self.inner_circle = None
        self.outter_circle = None

    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_bellow(self, x: int, y: int):
        return self.outter_circle.collidepoint(x, y)

    def draw(self, screen: pygame.Surface, color):
        text = font.render(f'P{self.id}', True, color)
        textRect = text.get_rect()
        if self.y < 20:
            textRect.center = (self.x, self.y + 20)
        else:
            textRect.center = (self.x, self.y - 15)

        screen.blit(text, textRect)
        self.outter_circle = pygame.draw.circle(
            screen, color, (self.x, self.y), 10)
        self.inner_circle = pygame.draw.circle(
            screen, grey, (self.x, self.y), 9)
