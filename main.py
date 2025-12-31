import pygame

#Setting up window using pygame
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True

while running:

    #Closing the Window Function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.fill("white")

    #flips the display screen
    pygame.display.flip()

    #Seting FPS setting
    clock.tick(60)

pygame.quit()