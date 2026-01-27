# scene.py
import pygame

def draw_scene(surface, width, height):
    # Colors
    SKY_COLOR = (20, 20, 40)      # will later change with intensity
    GROUND_COLOR = (40, 80, 40)
    HOUSE_COLOR = (180, 160, 140)
    ROOF_COLOR = (140, 70, 40)
    GUTTER_COLOR = (120, 120, 130)
    PIPE_COLOR = (120, 120, 130)
    TANK_FRONT = (60, 100, 160)
    TANK_SIDE = (40, 70, 120)

    surface.fill(SKY_COLOR)

    # Ground strip
    ground_rect = pygame.Rect(0, height - 175, width, 200)
    pygame.draw.rect(surface, GROUND_COLOR, ground_rect)

    # House body
    house_rect = pygame.Rect(150, 320, 200, 180)  # x, y, w, h
    pygame.draw.rect(surface, HOUSE_COLOR, house_rect)

    # Roof as trapezoid (pseudo-3D)
    # front edge slightly lower, back edge slightly higher
    roof_front_left = (140, 320)
    roof_front_right = (360, 320)
    roof_back_left = (160, 280)
    roof_back_right = (340, 280)
    roof_points = [roof_back_left, roof_back_right, roof_front_right, roof_front_left]
    pygame.draw.polygon(surface, ROOF_COLOR, roof_points)

    # Gutter (front edge of roof)
    gutter_rect = pygame.Rect(140, 320, 230, 7)
    pygame.draw.rect(surface, GUTTER_COLOR, gutter_rect)

    # Down pipe
    pipe_rect = pygame.Rect(355, 320, 10, 135)
    pygame.draw.rect(surface, PIPE_COLOR, pipe_rect)

    # Connection pipe
    pipe_rect = pygame.Rect(355, 450, 70, 7)
    pygame.draw.rect(surface, PIPE_COLOR, pipe_rect)

    # Tank front
    tank_front_rect = pygame.Rect(410, 320, 80, 140)
    pygame.draw.rect(surface, TANK_FRONT, tank_front_rect)
