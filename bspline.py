# B-Spline Grau 6 (Não Uniforme)
from argparse import ArgumentError
import pygame
from colors import *
from controlpoint import ControlPoint


class BSpline:
    param = 1

    def __init__(self, order: int = -1, degree: int = -1, control_points: list[ControlPoint] = []):
        if degree == -1 and order == -1:
            raise ArgumentError('either order or degree is necessary')
        if degree != -1 and degree <= 0:
            raise ValueError('degree has to be bigger than 0')
        if order != -1 and order <= 1:
            raise ValueError('order has to be bigger than 1')
        self.degree: int = degree if degree != -1 else order - 1
        self.order: int = order if order != -1 else degree + 1
        self.control_points: list[ControlPoint] = control_points
        self.knotSequence: list[int] = []

    def update_control_points(self, control_points: list[ControlPoint]):
        self.control_points = control_points
        self.__updateKnotSequence()

    def add_control_point(self, control_point: ControlPoint):
        self.control_points.append(control_point)
        self.__updateKnotSequence()

    def remove_control_point(self, control_point: ControlPoint):
        self.control_points.remove(control_point)
        self.__updateKnotSequence()

    def draw_connecting_lines(self, screen: pygame.Surface):
        for i in range(len(self.control_points) - 1):
            pygame.draw.line(
                screen, black, self.control_points[i].get_pos(), self.control_points[i+1].get_pos(), width=2)

    def draw_control_points(self, screen: pygame.Surface):
        for p in self.control_points:
            p.draw(screen, red)

    def draw_curve(self, screen: pygame.Surface):
        if self.order >= len(self.control_points):
            i = 0.0
            while i <= 1:
                self.__draw_point(i, screen)
                i += BSpline.param

    def __draw_point(self, u: int, screen: pygame.Surface):
        conX = [0 * self.order]
        conY = [0 * self.order]
        delta_index: int = self.__find_delta_index(u)

        for i in range(self.order - 1):
            conX[i] = self.control_points[delta_index - 1].x
            conY[i] = self.control_points[delta_index - 1].y

        for r in range(self.order, 1, -1):
            i = delta_index
            for s in range(r - 1):
                omega = u - \
                    (self.knotSequence[i] / self.knotSequence[i + r - 1]) - \
                    self.knotSequence[i]
                conX[s] = omega * conX[s] + (1 - omega) * conX[s + 1]
                conY[s] = omega * conY[s] + (1 - omega) * conY[s + 1]
                i -= 1

        # calculations return normalized value [0,1]
        # coords in pygame are integers
        x = int(conX[0] * screen.get_size()[0])
        y = int(conY[0] * screen.get_size()[1])
        pygame.draw.circle(screen, purple, (x, y), 1)

    def __find_delta_index(self, u: int):
        j = 0
        m = len(self.control_points) - 1
        for i in range(m + self.order - 1):
            if u >= self.knotSequence[i] and u < self.knotSequence[i+1]:
                return i
            j += 1
        return -1

    def __updateKnotSequence(self):
        m = len(self.control_points) - 1
        total = m + self.order + 1
        knot_value = 0
        increment = 1 / (m - self.order + 2)
        self.knotSequence.clear()
        for i in range(total):
            if i < self.order:
                self.knotSequence.append(0)
            elif i >= self.order and i < total - self.order:
                knot_value += increment
                self.knotSequence.append(knot_value)
            elif i >= total - self.order:
                self.knotSequence.append(1)
