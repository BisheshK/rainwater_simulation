import sys
import pygame
from rain import Raindrop, WIDTH, HEIGHT
from env import draw_scene

# Setting up window to run pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
FPS = 60

def load_img(name, size):
        return pygame.transform.scale(pygame.image.load(f"assets/{name}.png").convert_alpha(), size)
# Image Path
IMG_GROUND = load_img("ground",     (1000, 200))
IMG_HOUSE  = load_img("house",      (250, 220))  
IMG_ROOF   = load_img("roof",       (270, 50))    
IMG_GUTTER = load_img("gutter",     (270, 7))     
IMG_TANK   = load_img("water_tank", (90, 150))    
IMG_PIPE   = load_img("pipe",       (50, 6))     
IMG_FIELD  = load_img("field",      (260, 140))   
IMG_PLANT  = load_img("plant",      (28, 28))


# Contrl Module 
UI_MARGIN_X = WIDTH - 420
UI_MARGIN_Y = 20

# Slider configuration (Now Top-Left)
SLIDER_WIDTH = 250
SLIDER_HEIGHT = 10 # Thicker track
SLIDER_HANDLE_RADIUS = 12 # Larger handle
SLIDER_X = UI_MARGIN_X + 130
SLIDER_Y = UI_MARGIN_Y + 50

# Button (Switch) configuration
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 25
BUTTON_X = UI_MARGIN_X + 130
BUTTON_Y = SLIDER_Y + 45

# Colors from the mockup
BG_COLOR_UI = (200, 240, 245)  # Light cyan background
ACCENT_COLOR = (52, 190, 235)  # Bright blue for handles/switches
TRACK_COLOR = (215, 215, 215)   # Light grey

watering_active = False

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


def draw_control_panel(surface):
    # Reduced panel size to 400x150
    panel_rect = pygame.Rect(UI_MARGIN_X, UI_MARGIN_Y, 400, 150)
    pygame.draw.rect(surface, BG_COLOR_UI, panel_rect, border_radius=25)
    pygame.draw.rect(surface, (0, 0, 0), panel_rect, 2, border_radius=25) 

    # Smaller title font
    font_title = pygame.font.SysFont("Arial", 22, bold=True)
    title_text = font_title.render("CONTROL MODULE", True, (0, 0, 0))
    surface.blit(title_text, (panel_rect.centerx - title_text.get_width()//2, UI_MARGIN_Y + 15))

def draw_slider(surface, value: float):
    # Smaller label font
    font = pygame.font.SysFont("Arial", 16, bold=True)
    text = font.render("RAIN INTENSITY:", True, (0, 0, 0))
    surface.blit(text, (SLIDER_X - 120, SLIDER_Y - 3))

    track_rect = pygame.Rect(SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT)
    pygame.draw.rect(surface, TRACK_COLOR, track_rect, border_radius=SLIDER_HEIGHT//2)

    value = max(0.0, min(1.0, value))
    handle_x = SLIDER_X + int(value * SLIDER_WIDTH)
    handle_y = SLIDER_Y + SLIDER_HEIGHT // 2
    pygame.draw.circle(surface, ACCENT_COLOR, (handle_x, handle_y), SLIDER_HANDLE_RADIUS)

def draw_button(surface, active):
    font = pygame.font.SysFont("Arial", 16, bold=True)
    text = font.render("WATER:", True, (0, 0, 0))
    surface.blit(text, (BUTTON_X - 120, BUTTON_Y + 3))

    button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(surface, TRACK_COLOR, button_rect, border_radius=BUTTON_HEIGHT//2)

    # Smaller toggle circle
    circle_radius = 15
    circle_x = BUTTON_X + (BUTTON_WIDTH - circle_radius) if active else BUTTON_X + circle_radius
    pygame.draw.circle(surface, ACCENT_COLOR, (circle_x, BUTTON_Y + BUTTON_HEIGHT//2), circle_radius)

    return button_rect


intensity = 0.5 
dragging_slider = False
spawn_interval = intensity_to_spawn_interval(intensity) # Initial interval

assets = {
    'ground': IMG_GROUND, 'house': IMG_HOUSE, 'roof': IMG_ROOF,
    'gutter': IMG_GUTTER, 'tank': IMG_TANK,   'pipe': IMG_PIPE,
    'field':  IMG_FIELD,  'plant': IMG_PLANT
}

while running:

    dt = clock.tick(FPS) / 1000.0

    # Closing the Window Function & slider interaction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Slider check
            if SLIDER_X <= mx <= SLIDER_X + SLIDER_WIDTH and SLIDER_Y - 15 <= my <= SLIDER_Y + 15:
                dragging_slider = True
            # Button check
            button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            if button_rect.collidepoint(mx, my):
                watering_active = not watering_active
        
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False
        
        elif event.type == pygame.MOUSEMOTION and dragging_slider:
            mx, my = event.pos
            intensity = (mx - SLIDER_X) / SLIDER_WIDTH
            intensity = max(0.0, min(1.0, intensity))

    # Compute current spawn interval from intensity
        spawn_interval = intensity_to_spawn_interval(intensity)

    # Only spawn rain if intensity is greater than 0
    if intensity > 0:
        spawn_timer += dt
        while spawn_timer >= spawn_interval:
            raindrops.append(Raindrop())
            spawn_timer -= spawn_interval
    else:
        spawn_timer = 0

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

    # Drawing static environment with raindrops
    draw_scene(screen, WIDTH, HEIGHT, intensity, watering_active, assets)
    
    for drop in raindrops:
        drop.draw(screen)

    # Multiple raindrops
    for drop in raindrops:
        drop.draw(screen)

    # Draw the Background Panel
    draw_control_panel(screen)

    # Draw UI components inside it
    draw_slider(screen, intensity)
    draw_button(screen, watering_active)

    pygame.display.flip()

    # Flips the display screen
    pygame.display.flip()

pygame.quit()
sys.exit()