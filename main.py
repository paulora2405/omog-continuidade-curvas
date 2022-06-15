import pygame
from colors import *
from controlpoint import ControlPoint

size = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(size)
print(screen.get_size())
clock = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 26)
control_points: list[ControlPoint] = []
index = 0
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_left, m_middle, m_right = pygame.mouse.get_pressed()
            if m_left:
                x, y = pygame.mouse.get_pos()
                found = False
                for cp in control_points:
                    if cp.is_bellow(x, y):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        moving_index = control_points.index(cp)
                        found = True
                if not found:
                    control_points.append(ControlPoint(
                        x, y, index))
                    index += 1
            elif m_right:
                x, y = pygame.mouse.get_pos()
                for cp in control_points:
                    if cp.is_bellow(x, y):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        control_points.remove(cp)

        elif event.type == pygame.MOUSEBUTTONUP:
            moving_index = -1
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if moving_index != -1:
            x, y = pygame.mouse.get_pos()
            control_points[moving_index].set_pos(x, y)

    # draws lines connecting control points
    for i in range(len(control_points) - 1):
        pygame.draw.line(
            screen, black, control_points[i].get_pos(), control_points[i+1].get_pos(), width=2)
    # draws control points
    for p in control_points:
        p.draw(screen, red)
    # draws text for less than 4 cp
    if len(control_points) < 4:
        text = font.render(
            f'You need at least 4 control points, {4 - len(control_points)} to go.', True, black)
        textRect = text.get_rect()
        textRect.centerx = screen.get_size()[0] // 2
        screen.blit(text, textRect)

    pygame.display.update()

pygame.quit()
