from argparse import ArgumentError
import pygame
import sys
from colors import *
from controlpoint import ControlPoint
from bspline import BSpline


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
    run = True

    while run:
        screen.fill(white)
        clock.tick(fps)
        frameRate = int(clock.get_fps())
        pygame.display.set_caption(
            f'Curve Continuity - Paulo Albuquerque - {frameRate} FPS')

        run = event_handling(bspline)

        bspline.move_control_point(pygame.mouse.get_pos())

        text = font.render(
            f'Degree {bspline.degree}      K Order {bspline.kOrder}      Control points {bspline.get_nCP()}',
            True,
            black)
        textRect = text.get_rect()
        textRect.centerx = screen.get_size()[0] // 2
        screen.blit(text, textRect)

        # draws connecting lines firts so they are further back
        bspline.draw_connecting_lines(screen)
        if bspline.can_draw():
            # draws the curve
            bspline.draw_curve(screen, blue)
        else:
            # draws text for less cp than order
            text = font.render(
                f'Pick at least {bspline.kOrder - bspline.get_nCP()} more control points!',
                True,
                black)
            textRect = text.get_rect()
            textRect.center = (screen.get_size()[0] // 2, 40)
            screen.blit(text, textRect)
        # draws the control points last so they are at above everything else
        bspline.draw_control_points(screen)

        pygame.display.update()

    pygame.quit()


def event_handling(bspline: BSpline) -> bool:
    run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_d:
                bspline.inc_order()
            elif event.key == pygame.K_a:
                bspline.dec_order()
            elif event.key == pygame.K_s:
                bspline.clear_control_points()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_left, _, m_right = pygame.mouse.get_pressed()
            if m_left:
                x, y = pygame.mouse.get_pos()
                found = False
                for cp in bspline.control_points:
                    if cp.is_bellow(x, y):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        bspline.set_moving(cp)
                        found = True
                        break
                if not found:
                    bspline.add_control_point(x, y, red)
            elif m_right:
                x, y = pygame.mouse.get_pos()
                for cp in bspline.control_points:
                    if cp.is_bellow(x, y):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        bspline.remove_control_point(cp)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            bspline.set_not_moving()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    return run


if __name__ == "__main__":
    main()
