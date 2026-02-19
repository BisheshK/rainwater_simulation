import sys
import pygame

WIDTH, HEIGHT = 1000, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coordinate Grid (interval: 10)")
clock = pygame.time.Clock()
font_mid = pygame.font.SysFont("Arial", 11, bold=True)

GRID_INTERVAL = 10
MAJOR_EVERY   = 100
BG            = (30, 30, 30)
MINOR_COLOR   = (60, 60, 60)
MAJOR_COLOR   = (100, 100, 100)
LABEL_COLOR   = (200, 200, 200)
CURSOR_COLOR  = (255, 220, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(BG)

    # Vertical lines
    for x in range(0, WIDTH, GRID_INTERVAL):
        is_major = (x % MAJOR_EVERY == 0)
        pygame.draw.line(screen, MAJOR_COLOR if is_major else MINOR_COLOR, (x, 0), (x, HEIGHT), 1)
        if is_major and x > 0:
            screen.blit(font_mid.render(str(x), True, LABEL_COLOR), (x + 2, 2))

    # Horizontal lines
    for y in range(0, HEIGHT, GRID_INTERVAL):
        is_major = (y % MAJOR_EVERY == 0)
        pygame.draw.line(screen, MAJOR_COLOR if is_major else MINOR_COLOR, (0, y), (WIDTH, y), 1)
        if is_major and y > 0:
            screen.blit(font_mid.render(str(y), True, LABEL_COLOR), (2, y + 2))

    # Crosshair + coordinate label
    mx, my = pygame.mouse.get_pos()
    pygame.draw.line(screen, CURSOR_COLOR, (mx, 0), (mx, HEIGHT), 1)
    pygame.draw.line(screen, CURSOR_COLOR, (0, my), (WIDTH, my), 1)

    snapped_x = round(mx / GRID_INTERVAL) * GRID_INTERVAL
    snapped_y = round(my / GRID_INTERVAL) * GRID_INTERVAL
    coord_surf = font_mid.render(f"({snapped_x}, {snapped_y})", True, CURSOR_COLOR)

    lx = mx + 10 if mx + 10 + coord_surf.get_width() < WIDTH else mx - coord_surf.get_width() - 5
    ly = my + 10 if my + 10 + coord_surf.get_height() < HEIGHT else my - coord_surf.get_height() - 5
    screen.blit(coord_surf, (lx, ly))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
