# Bezier Grau 4
from math import factorial
from sys import stderr
import pygame
from colors import *
from helper import render_text
from controlpoint import ControlPoint
from bspline import BSpline
from typing import List, Tuple


class Bezier:
    param = 0.0005

    def __init__(self, degree: int = -1, control_points: List[ControlPoint] = []):
        if degree <= 0:
            raise ValueError('degree has to be bigger than 0')
        self.degree = degree
        self.control_points: List[ControlPoint] = control_points
        self.curve_points: List[Tuple[int, int]] = []
        self.changed_state: bool = True
        self.moving_index: int = -1

    def inc_degree(self):
        self.changed_state = True
        self.degree += 1

    def dec_degree(self):
        self.changed_state = True
        if self.degree >= 2:
            self.degree -= 1

    def can_draw(self) -> bool:
        return self.get_nCP() == self.degree + 1

    def get_nCP(self) -> int:
        return len(self.control_points)

    def try_moving(self, x: int, y: int):
        for cp in self.control_points:
            if cp.is_bellow(x, y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.set_moving(cp)
                break

    def try_removing(self, x: int, y: int):
        for cp in self.control_points:
            if cp.is_bellow(x, y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.remove_control_point(cp)
                break

    def set_moving(self, control_point: ControlPoint):
        self.moving_index = self.control_points.index(control_point)

    def set_not_moving(self):
        self.moving_index = -1

    def is_moving(self) -> bool:
        return self.moving_index != -1

    def move_control_point_if_set(self, coord: Tuple[int, int]):
        if self.is_moving():
            if coord != self.control_points[self.moving_index].get_pos():
                self.changed_state = True
                self.control_points[self.moving_index].set_pos(*coord)
            else:
                self.changed_state = False

    def clear_control_points(self):
        self.changed_state = True
        self.control_points = []

    def add_control_point(self, x: int, y: int, color: Tuple[int, int, int]):
        if self.get_nCP() == self.degree + 1:
            return
        self.changed_state = True
        self.control_points.append(ControlPoint(
            x, y, self.get_nCP(), color, True))

    def remove_control_point(self, control_point: ControlPoint):
        self.changed_state = True
        self.control_points.remove(control_point)
        self.__update_control_points_indexes()

    def __update_control_points_indexes(self):
        for index, cp in enumerate(self.control_points):
            cp.id = index

    def draw_connecting_lines(self, screen: pygame.Surface):
        for i in range(len(self.control_points) - 1):
            pygame.draw.line(
                screen, black, self.control_points[i].get_pos(), self.control_points[i+1].get_pos(), width=2)

    def draw_control_points(self, screen: pygame.Surface):
        for p in self.control_points:
            if p.x > screen.get_size()[0]:
                p.x = screen.get_size()[0] - 10
            if p.y > screen.get_size()[1]:
                p.y = screen.get_size()[1] - 10
            p.draw(screen)

    def draw_curve(self, screen: pygame.Surface, font: pygame.font.Font, color: Tuple[int, int, int]):
        if not self.changed_state:
            self.__draw_cached_curve(screen, color)
        elif self.can_draw():
            self.changed_state = False
            self.curve_points.clear()
            i = 0.0
            while i <= 1.0:
                self.__calculate_point(i, screen, color)
                i += Bezier.param
            self.__draw_cached_curve(screen, color)
        else:
            render_text(f'{self.degree - self.get_nCP() + 1} more points needed!',
                        (screen.get_size()[0] // 4 + screen.get_size()[0] // 2, 40), screen, font, black)

    def __draw_cached_curve(self, screen: pygame.Surface, color: Tuple[int, int, int]):
        pygame.draw.lines(screen, color, False, self.curve_points, 4)

    def __calculate_point(self, u: float, screen: pygame.Surface, color: Tuple[int, int, int]):
        sumX = 0
        sumY = 0
        for i in range(self.get_nCP()):
            sumX += (factorial(self.degree) /
                     (factorial(i) * factorial(self.degree - i))) * \
                pow(1-u, self.degree-i) * \
                pow(u, i) * \
                self.control_points[i].x
            sumY += (factorial(self.degree) /
                     (factorial(i) * factorial(self.degree - i))) * \
                pow(1-u, self.degree-i) * \
                pow(u, i) * \
                self.control_points[i].y

        self.curve_points.append((int(sumX), int(sumY)))

    def continuity_0(self, bspline: BSpline):
        if self.can_draw() and bspline.can_draw():
            self.changed_state = True
            last_cp_bspline = bspline.control_points[-1]
            first_cp_bezier = self.control_points[0]
            deltaX = last_cp_bspline.x - first_cp_bezier.x
            deltaY = last_cp_bspline.y - first_cp_bezier.y
            for cp in self.control_points:
                cp.set_pos(cp.x + deltaX, cp.y + deltaY)

    def continuity_1(self, bspline: BSpline):
        self.continuity_0(bspline)
        seclast_cp_bsline = bspline.control_points[-2]
        first_cp_bezier = self.control_points[0]
        deltaX = seclast_cp_bsline.x - first_cp_bezier.x
        deltaY = seclast_cp_bsline.y - first_cp_bezier.y
        self.control_points[1].set_pos(
            first_cp_bezier.x - deltaX,
            first_cp_bezier.y - deltaY
        )

    def continuity_2(self, bspline: BSpline):
        self.continuity_1(bspline)
