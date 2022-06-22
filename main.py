from argparse import ArgumentError
import pygame
import sys
from colors import *
from bspline import BSpline
from bezier import Bezier
from typing import Tuple


def main():
    if len(sys.argv) == 1:
        size = (1280, 720)
    elif len(sys.argv) == 3:
        size = (int(sys.argv[1]), int(sys.argv[2]))
    else:
        raise ArgumentError(
            argument=None, message='either pass WIDTH HEIGHT or no arguments')

    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('freesansbold.ttf', 26)
    bspline = BSpline(degree=6)
    bezier = Bezier(degree=4)
    run = True
    fcs = True  # First Curve Selected, for short

    while run:
        screen.fill(white)
        clock.tick(fps)
        frameRate = int(clock.get_fps())
        pygame.display.set_caption(
            f'Curve Continuity - Paulo Albuquerque - {frameRate} FPS')

        run, fcs = event_handling(
            bspline, bezier, fcs)

        render_text(f'B-Spline: Degree={bspline.degree} Points={bspline.get_nCP()}',
                    (screen.get_size()[0] // 4, 14), screen, font, red)
        render_text(f'Bezier: Degree={bezier.degree} Points={bezier.get_nCP()}',
                    (screen.get_size()[0] // 4 + screen.get_size()[0] // 2, 14), screen, font, blue)
        render_text(f'{"<-" if fcs else ""} Selected {"->" if not fcs else ""}',
                    (screen.get_size()[0] // 2, 14), screen, font, red if fcs else blue)
        render_text('Space key switches', (screen.get_size()
                    [0] // 2, 40), screen, font, black)

        bspline.draw_connecting_lines(screen)
        bezier.draw_connecting_lines(screen)
        if bspline.can_draw():
            bspline.draw_curve(screen, red)
        else:
            render_text(f'{bspline.kOrder - bspline.get_nCP()} more points needed!',
                        (screen.get_size()[0] // 4, 40), screen, font, black)
        if bezier.can_draw():
            bezier.draw_curve(screen, blue)
        else:
            render_text(f'{bezier.degree - bezier.get_nCP() + 1} more points needed!',
                        (screen.get_size()[0] // 4 + screen.get_size()[0] // 2, 40), screen, font, black)
        bspline.draw_control_points(screen)
        bezier.draw_control_points(screen)

        pygame.display.update()

    pygame.quit()


def event_handling(bspline: BSpline, bezier: Bezier, first_curve_selected) -> Tuple[bool, bool]:
    run = True
    fcs = first_curve_selected
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                fcs = not fcs
            elif event.key == pygame.K_d:
                if fcs:
                    bspline.inc_order()
                else:
                    bezier.inc_degree()
            elif event.key == pygame.K_a:
                if fcs:
                    bspline.dec_order()
                else:
                    bezier.dec_degree()
            elif event.key == pygame.K_s:
                bspline.clear_control_points()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_left, _, m_right = pygame.mouse.get_pressed()
            if m_left:
                bspline.try_moving(x, y)
                bezier.try_moving(x, y)
                if not bspline.is_moving() and not bezier.is_moving():
                    if fcs:
                        bspline.add_control_point(x, y, red)
                    else:
                        bezier.add_control_point(x, y, blue)
            elif m_right:
                bspline.try_removing(x, y)
                bezier.try_removing(x, y)

        elif event.type == pygame.MOUSEBUTTONUP:
            bspline.set_not_moving()
            bezier.set_not_moving()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    bspline.move_control_point_if_set((x, y))
    bezier.move_control_point_if_set((x, y))

    return run, fcs


def render_text(text: str, pos: Tuple[int, int], screen: pygame.Surface, font: pygame.font.Font, color: Tuple[int, int, int]):
    textRender = font.render(text, True, color)
    textRect = textRender.get_rect()
    textRect.center = pos
    screen.blit(textRender, textRect)


if __name__ == "__main__":
    main()
