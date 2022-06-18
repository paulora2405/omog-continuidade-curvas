import pygame
from colors import *
from controlpoint import ControlPoint
from bspline import BSpline

size = (1280, 720)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('freesansbold.ttf', 26)
    bspline = BSpline(degree=6)
    cp_index = 0
    moving_index = -1
    run = True

    while run:
        screen.fill(white)
        clock.tick(fps)
        frameRate = int(clock.get_fps())
        pygame.display.set_caption(
            f'Curve Continuity - Paulo Albuquerque - {frameRate} FPS')

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
                            moving_index = bspline.control_points.index(cp)
                            found = True
                    if not found:
                        bspline.add_control_point(ControlPoint(
                            x, y, cp_index, red))
                        cp_index += 1
                elif m_right:
                    x, y = pygame.mouse.get_pos()
                    for cp in bspline.control_points:
                        if cp.is_bellow(x, y):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            bspline.remove_control_point(cp)

            elif event.type == pygame.MOUSEBUTTONUP:
                moving_index = -1
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if moving_index != -1:
                bspline.move_control_point(
                    moving_index, pygame.mouse.get_pos())

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


if __name__ == "__main__":
    main()
