# B-Spline Grau 6 (Não Uniforme)
from argparse import ArgumentError
from sys import stderr
import pygame
from colors import *
from controlpoint import ControlPoint
from typing import List, Tuple
from helper import render_text


class BSpline:
    param = 0.0005

    def __init__(self, kOrder: int = -1, degree: int = -1, control_points: List[ControlPoint] = []):
        if degree == -1 and kOrder == -1:
            raise ArgumentError(
                argument=None, message='either order or degree is necessary')
        if degree != -1 and kOrder != -1 and degree + 1 != kOrder:
            raise ValueError('order has to be equal to degree + 1')
        if degree != -1 and degree <= 0:
            raise ValueError('degree has to be bigger than 0')
        if kOrder != -1 and kOrder <= 1:
            raise ValueError('order has to be bigger than 1')
        self.degree: int = degree if degree != -1 else kOrder - 1
        self.kOrder: int = kOrder if kOrder != -1 else degree + 1
        self.control_points: List[ControlPoint] = control_points
        self.knotSequence: List[float] = []
        self.curve_points: List[Tuple[int, int]] = []
        self.changed_state: bool = True
        self.moving_index: int = -1

    def inc_order(self):
        self.changed_state = True
        self.kOrder += 1
        self.degree = self.kOrder - 1

    def dec_order(self):
        self.changed_state = True
        if self.kOrder > 2:
            self.kOrder -= 1
            self.degree = self.kOrder - 1

    def can_draw(self) -> bool:
        return self.kOrder <= self.get_nCP()

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
        self.changed_state = True
        self.control_points.append(ControlPoint(x, y, self.get_nCP(), color))

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
            p.draw(screen)

    def draw_curve(self, screen: pygame.Surface, font: pygame.font.Font, color: Tuple[int, int, int]):
        if not self.changed_state:
            self.__draw_cached_curve(screen, color)
        elif self.can_draw():
            self.changed_state = False
            self.__updateKnotVectors()
            # print(self.knotSequence)
            self.curve_points.clear()
            i = 0.0
            while i <= 1.0:
                self.__calculate_point(i, screen, color)
                i += BSpline.param
            self.__draw_cached_curve(screen, color)
        else:
            render_text(f'{self.kOrder - self.get_nCP()} more points needed!',
                        (screen.get_size()[0] // 4, 40), screen, font, black)

    def __draw_cached_curve(self, screen: pygame.Surface, color: Tuple[int, int, int]):
        pygame.draw.lines(screen, color, False, self.curve_points, 4)

    def __calculate_point(self, u: float, screen: pygame.Surface, color: Tuple[int, int, int]):
        coordX = [0.0 for _ in range(self.kOrder + 1)]
        coordY = [0.0 for _ in range(self.kOrder + 1)]
        delta_index: int = self.__find_delta_index(u)

        for i in range(self.kOrder):
            coordX[i] = self.control_points[delta_index - i].x / \
                screen.get_size()[0]
            coordY[i] = self.control_points[delta_index - i].y / \
                screen.get_size()[1]

        for r in range(self.kOrder, 1, -1):
            i = delta_index
            for s in range(r):
                omega = (u - self.knotSequence[i]) / \
                    (self.knotSequence[i + r - 1] -
                     self.knotSequence[i] + 0.0000000001)
                coordX[s] = omega * coordX[s] + (1 - omega) * coordX[s + 1]
                coordY[s] = omega * coordY[s] + (1 - omega) * coordY[s + 1]
                i -= 1

        # calculations return normalized value [0,1]
        # coords in pygame are integers
        x = int(screen.get_size()[0] * coordX[0])
        y = int(screen.get_size()[1] * coordY[0])
        self.curve_points.append((x, y))

    def __find_delta_index(self, u: float) -> int:
        m = self.get_nCP() - 1
        for i in range(m + self.kOrder - 1):
            if u >= self.knotSequence[i] and u < self.knotSequence[i+1]:
                return i
        raise ValueError('`u` not in interval t_i <= u < t_i+1')

    def __updateKnotVectors(self):
        self.knotSequence.clear()
        if self.get_nCP() - self.kOrder + 2 == 0:
            return

        m = float(self.get_nCP() - 1)
        knot_value = 0.0
        increment = 1.0 / (m - float(self.kOrder) + 2.0000000001)

        for i in range(self.get_nCP() + self.kOrder):
            if i < self.kOrder:
                self.knotSequence.append(0.0)
            elif i >= self.kOrder and i < self.get_nCP():
                knot_value += increment
                self.knotSequence.append(knot_value)
            elif i >= self.get_nCP():
                self.knotSequence.append(1.0)
