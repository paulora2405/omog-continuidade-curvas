import pygame
from colors import *
from controlpoint import ControlPoint
from bspline import BSpline

size = (1280, 720)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    print(screen.get_size())
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
            "OMOG Continuidade de Curvas - Paulo Albuquerque - FPS : {}".format(frameRate))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bspline.kOrder += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if bspline.kOrder > 2:
                        bspline.kOrder -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_left, m_middle, m_right = pygame.mouse.get_pressed()
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
                            x, y, cp_index))
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
                x, y = pygame.mouse.get_pos()
                bspline.control_points[moving_index].set_pos(x, y)

        bspline.draw_connecting_lines(screen)
        bspline.draw_control_points(screen)

        # draws text for less cp than order
        if bspline.get_nCP() < bspline.kOrder:
            text = font.render(
                f'Pick at least {bspline.kOrder - bspline.get_nCP()} more control points.',
                True,
                black)
            textRect = text.get_rect()
            textRect.centerx = screen.get_size()[0] // 2
            screen.blit(text, textRect)
        else:
            text = font.render(
                f'Degree {bspline.degree}; K Order {bspline.kOrder}; Control points {bspline.get_nCP()}.',
                True,
                black)
            textRect = text.get_rect()
            textRect.centerx = screen.get_size()[0] // 2
            screen.blit(text, textRect)
            bspline.draw_curve(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
