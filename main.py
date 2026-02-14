import sys
import pygame
from rain import Raindrop, WIDTH, HEIGHT
from env import draw_scene

# Setting up window using pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
FPS = 60

# Slider configuration (bottom of the window)
SLIDER_X = 150
SLIDER_Y = HEIGHT - 40
SLIDER_WIDTH = 400
SLIDER_HEIGHT = 8
SLIDER_HANDLE_RADIUS = 10

intensity = 0.5  # initial rain intensity [0.0, 1.0]
dragging_slider = False

# Rain spawning container
raindrops = []
spawn_timer = 0.0

# Spawn interval limits (in seconds)
MAX_INTERVAL = 0.25  # almost no rain
MIN_INTERVAL = 0.01  # very heavy rain


def intensity_to_spawn_interval(value: float) -> float:
    """Map slider intensity [0,1] to spawn interval (smaller = more drops)."""
    value = max(0.0, min(1.0, value))
    return MAX_INTERVAL - value * (MAX_INTERVAL - MIN_INTERVAL)


def draw_slider(surface, value: float):
    """Draw a simple horizontal slider and label for rain intensity."""
    # Track
    track_rect = pygame.Rect(SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT)
    pygame.draw.rect(surface, (200, 200, 200), track_rect)

    # Handle position based on current value
    value = max(0.0, min(1.0, value))
    handle_x = SLIDER_X + int(value * SLIDER_WIDTH)
    handle_y = SLIDER_Y + SLIDER_HEIGHT // 2
    pygame.draw.circle(surface, (255, 255, 255), (handle_x, handle_y), SLIDER_HANDLE_RADIUS)
    pygame.draw.circle(surface, (50, 50, 50), (handle_x, handle_y), SLIDER_HANDLE_RADIUS, 2)

    # Label
    font = pygame.font.SysFont(None, 24)
    text = font.render("Rain intensity", True, (255, 255, 255))
    surface.blit(text, (SLIDER_X, SLIDER_Y - 25))


while running:

    dt = clock.tick(FPS) / 1000.0

    # Closing the Window Function & slider interaction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Check if click is on/near the slider track area
            if SLIDER_X <= mx <= SLIDER_X + SLIDER_WIDTH and SLIDER_Y - 15 <= my <= SLIDER_Y + 25:
                dragging_slider = True
                # Update intensity immediately on click
                intensity = (mx - SLIDER_X) / SLIDER_WIDTH
                intensity = max(0.0, min(1.0, intensity))
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False
        elif event.type == pygame.MOUSEMOTION and dragging_slider:
            mx, my = event.pos
            intensity = (mx - SLIDER_X) / SLIDER_WIDTH
            intensity = max(0.0, min(1.0, intensity))

    # Compute current spawn interval from intensity
    spawn_interval = intensity_to_spawn_interval(intensity)

    # Updating the rain
    spawn_timer += dt
    while spawn_timer >= spawn_interval:
        raindrops.append(Raindrop())
        spawn_timer -= spawn_interval

    # For rain to fall
    for drop in raindrops:
        drop.update()

    # Remove raindrop that ends
    raindrops = [d for d in raindrops if not d.off_screen()]

    # Drawing static environment with raindrops (background depends on intensity)
    draw_scene(screen, WIDTH, HEIGHT, intensity)

    # Multiple raindrops
    for drop in raindrops:
        drop.draw(screen)

    # Draw UI slider on top
    draw_slider(screen, intensity)

    # Flips the display screen
    pygame.display.flip()

pygame.quit()
sys.exit()