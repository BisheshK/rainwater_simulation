import sys
import pygame
from rain import Raindrop, WIDTH, HEIGHT
from env import draw_scene

#Setting up window using pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True
FPS=60

#rain spawing container
raindrops=[]
spawn_timer = 0.0
spawn_interval = 0.05

while running:

    dt = clock.tick(FPS) / 1000.0

    #Closing the Window Function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    #updating the rain
    spawn_timer += dt
    while spawn_timer >= spawn_interval:
        raindrops.append(Raindrop())
        spawn_timer -= spawn_interval

    #for rain to fall
    for drop in raindrops:
        drop.update()

    # remove raindrop that ends
    raindrops = [d for d in raindrops if not d.off_screen()]

    #drawing static environment with raindrops 
    draw_scene(screen,WIDTH,HEIGHT)

    #multiple raindrops
    for drop in raindrops:
        drop.draw(screen)
    
    #flips the display screen
    pygame.display.flip()

pygame.quit()
sys.exit()