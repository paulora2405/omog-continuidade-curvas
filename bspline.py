# B-Spline Grau 6 (Não Uniforme)
from argparse import ArgumentError
import pygame
from colors import *
from controlpoint import ControlPoint


class BSpline:
    param = 0.0005

    def __init__(self, kOrder: int = -1, degree: int = -1, control_points: list[ControlPoint] = []):
        if degree == -1 and kOrder == -1:
            raise ArgumentError('either order or degree is necessary')
        if degree != -1 and degree <= 0:
            raise ValueError('degree has to be bigger than 0')
        if kOrder != -1 and kOrder <= 1:
            raise ValueError('order has to be bigger than 1')
        self.degree: int = degree if degree != -1 else kOrder - 1
        self.kOrder: int = kOrder if kOrder != -1 else degree + 1
        self.control_points: list[ControlPoint] = control_points
        self.knotSequence: list[float] = []

    def inc_order(self):
        if self.kOrder < self.get_nCP():
            self.kOrder += 1
            self.degree = self.kOrder - 1

    def dec_order(self):
        if self.kOrder > 2:
            self.kOrder -= 1
            self.degree = self.kOrder - 1

    def get_nCP(self) -> int:
        return len(self.control_points)

    def clear_control_points(self):
        self.control_points = []
        self.__updateKnotVectors()

    def add_control_point(self, control_point: ControlPoint):
        self.control_points.append(control_point)
        self.__updateKnotVectors()

    def remove_control_point(self, control_point: ControlPoint):
        self.control_points.remove(control_point)
        self.__updateKnotVectors()

    def draw_connecting_lines(self, screen: pygame.Surface):
        for i in range(len(self.control_points) - 1):
            pygame.draw.line(
                screen, black, self.control_points[i].get_pos(), self.control_points[i+1].get_pos(), width=2)

    def draw_control_points(self, screen: pygame.Surface):
        for p in self.control_points:
            p.draw(screen, red)

    def draw_curve(self, screen: pygame.Surface, color: tuple[int, int, int]):
        self.__updateKnotVectors()
        if self.kOrder <= self.get_nCP():
            i = 0.0
            while i <= 1.0:
                self.__draw_point(i, screen, color)
                i += BSpline.param

    def __draw_point(self, u: int, screen: pygame.Surface, color: tuple[int, int, int]):
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
        pygame.draw.circle(screen, color, (x, y), 1)

    def __find_delta_index(self, u: int):
        m = self.get_nCP() - 1
        for i in range(m + self.kOrder - 1):
            if u >= self.knotSequence[i] and u < self.knotSequence[i+1]:
                return i
        raise ValueError('`u` not in interval t_i <= u < t_i+1')

    def __updateKnotVectors(self):
        self.knotSequence.clear()
        if self.get_nCP() - self.kOrder + 2 == 0:
            return

        n = float(self.get_nCP())
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
