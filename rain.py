import pygame
import random

WIDTH, HEIGHT = 1000,600

class Raindrop:
    def __init__(rain):
        rain.x=random.randint(0,WIDTH)
        rain.y=0
        rain.vy=random.uniform(4,8)
        rain.length = random.randint(8,14)
        rain.color = (150,180,225)
    
    def update(rain):
        rain.y += rain.vy

    def off_screen(rain):
        return rain.y > HEIGHT
    
    def draw(rain, surface):
        initial_pos = (int(rain.x),int(rain.y))
        end_pos = (int(rain.x),int(rain.y + rain.length))
        pygame.draw.line(surface, rain.color, initial_pos, end_pos,1)
