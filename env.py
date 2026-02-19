# scene.py
import pygame

def draw_scene(surface, width, height, intensity, watering_active, imgs):
    intensity = max(0.0, min(1.0, intensity))

    CLEAR_SKY  = (135, 206, 235)
    STORMY_SKY = (20, 20, 40)

    def lerp(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    SKY_COLOR = lerp(CLEAR_SKY, STORMY_SKY, intensity)

    GROUND_COLOR = (40, 80, 40)
    HOUSE_COLOR  = (180, 160, 140)
    ROOF_COLOR   = (140, 70, 40)
    GUTTER_COLOR = (120, 120, 130)
    PIPE_COLOR   = (120, 120, 130)
    TANK_FRONT   = (60, 100, 160)
    GARDEN_SOIL  = (107, 75, 16)
    PLANT_COLOR  = (20, 150, 20)

    surface.fill(SKY_COLOR)

    # Ground strip
    ground_y = height - 200
    ground_rect = pygame.Rect(0, ground_y, width, 200)
    pygame.draw.rect(surface, GROUND_COLOR, ground_rect)

    # House body
    house_x, house_y = 100, 250
    house_w, house_h = 250, 220
    house_rect = pygame.Rect(house_x, house_y, house_w, house_h)
    pygame.draw.rect(surface, HOUSE_COLOR, house_rect)

    # Roof as trapezoid
    roof_front_left  = (house_x - 10,          house_y)
    roof_front_right = (house_x + house_w + 10, house_y)
    roof_back_left   = (house_x + 20,           house_y - 50)
    roof_back_right  = (house_x + house_w - 20, house_y - 50)
    roof_points = [roof_back_left, roof_back_right, roof_front_right, roof_front_left]
    pygame.draw.polygon(surface, ROOF_COLOR, roof_points)

    # Gutter
    gutter_rect = pygame.Rect(house_x - 10, house_y, house_w + 20, 7)
    pygame.draw.rect(surface, GUTTER_COLOR, gutter_rect)

    # Tank
    tank_x = house_x + house_w + 30   # = 380
    tank_y = 310
    tank_w, tank_h = 90, 150
    tank_front_rect = pygame.Rect(tank_x, tank_y, tank_w, tank_h)
    pygame.draw.rect(surface, TANK_FRONT, tank_front_rect)

    # Gutter-to-tank pipe
    gutter_right_x    = house_x + house_w + 10
    gutter_y          = house_y
    tank_top_center_x = tank_x + tank_w // 2
    drop_height       = 47
    pygame.draw.rect(surface, PIPE_COLOR, (gutter_right_x - 3, gutter_y, 6, drop_height))
    pygame.draw.rect(surface, PIPE_COLOR, (tank_top_center_x - 3, gutter_y + drop_height - 3, 6, 10))
    pygame.draw.rect(surface, PIPE_COLOR, (gutter_right_x - 3, gutter_y + drop_height - 3,
                                           tank_top_center_x - (gutter_right_x - 3), 6))

    # Field trapezoid
    field_w      = 260
    field_h      = 140
    field_offset = 40
    field_y      = ground_y - field_h + 150
    field_x      = tank_x + tank_w + 60   # = 510

    field_points = [
        (field_x,                field_y),           # top left
        (field_x + field_w,      field_y),           # top right
        (field_x + field_w - field_offset, field_y + field_h),  # bottom right
        (field_x - field_offset, field_y + field_h), # bottom left
    ]
    pygame.draw.polygon(surface, GARDEN_SOIL, field_points)
    pygame.draw.polygon(surface, (80, 110, 60), field_points, 2)

    field_top_left, field_top_right, field_bottom_right, field_bottom_left = field_points

    # Pipes along field edges
    PIPE_WIDTH = 6
    pygame.draw.line(surface, PIPE_COLOR, field_top_left,  field_bottom_left,  PIPE_WIDTH)
    pygame.draw.line(surface, PIPE_COLOR, field_top_right, field_bottom_right, PIPE_WIDTH)

    # Tank-to-field horizontal pipe
    tank_bottom_right = tank_x + tank_w
    pipe_height = tank_y + 140
    pygame.draw.rect(surface, PIPE_COLOR, (tank_bottom_right, pipe_height, 50, PIPE_WIDTH))

    # Water spray pipes across field
    PIPE_LINES  = 6
    spray_lines = []
    for i in range(PIPE_LINES):
        t  = i / (PIPE_LINES - 1)
        sy = int(field_top_left[1] + (field_bottom_left[1] - field_top_left[1]) * t)
        sx = int(field_top_left[0] + (field_bottom_left[0] - field_top_left[0]) * t)
        rx = int(field_top_right[0] + (field_bottom_right[0] - field_top_right[0]) * t)
        pygame.draw.line(surface, PIPE_COLOR, (sx, sy), (rx, sy), 3)
        spray_lines.append((sx, sy, rx))

    # Animated water jets
    if watering_active:
        current_time  = pygame.time.get_ticks()
        SPRAY_INTERVAL = 800
        JET_LENGTH     = 5
        JET_WIDTH      = 2
        JET_SPACING    = 30
        if (current_time // SPRAY_INTERVAL) % 2 == 0:
            for (sx, sy, rx) in spray_lines:
                for x in range(sx, rx, JET_SPACING):
                    pygame.draw.line(surface, (0, 200, 255), (x, sy), (x, sy - JET_LENGTH), JET_WIDTH)

    # Plants (X marks) inside trapezoid
    rows     = 5
    cols     = 5
    line_len = 7
    margin   = 15
    for row in range(rows):
        t_row   = (row + 0.5) / rows
        left_x  = field_top_left[0]  + (field_bottom_left[0]  - field_top_left[0])  * t_row
        left_y  = field_top_left[1]  + (field_bottom_left[1]  - field_top_left[1])  * t_row
        right_x = field_top_right[0] + (field_bottom_right[0] - field_top_right[0]) * t_row
        usable_left  = left_x  + margin
        usable_right = right_x - margin
        for col in range(cols):
            t_col = (col + 0.5) / cols
            px = usable_left + (usable_right - usable_left) * t_col
            py = left_y
            pygame.draw.line(surface, PLANT_COLOR, (px - line_len, py - line_len), (px + line_len, py + line_len), 2)
            pygame.draw.line(surface, PLANT_COLOR, (px - line_len, py + line_len), (px + line_len, py - line_len), 2)

    # ── Image overlays ───────────────────────────────────────────────────────

    # Ground
    if imgs.get('ground'):
        surface.blit(pygame.transform.scale(imgs['ground'], (width, 200)), (0, ground_y))

    # House  →  x=65, y=270, w=320, h=230
    HOUSE_IMG_X, HOUSE_IMG_Y = 65, 270
    HOUSE_IMG_W, HOUSE_IMG_H = 320, 230
    if imgs.get('house'):
        surface.blit(pygame.transform.scale(imgs['house'], (HOUSE_IMG_W, HOUSE_IMG_H)),
                     (HOUSE_IMG_X, HOUSE_IMG_Y))

    # Roof  →  x=55, y=170, w=360, h=110
    ROOF_IMG_X, ROOF_IMG_Y = 55, 170
    ROOF_IMG_W, ROOF_IMG_H = 360, 110
    if imgs.get('roof'):
        surface.blit(pygame.transform.scale(imgs['roof'], (ROOF_IMG_W, ROOF_IMG_H)),
                     (ROOF_IMG_X, ROOF_IMG_Y))

    # Gutter  →  x=65, y=270, w=320, h=12
    if imgs.get('gutter'):
        surface.blit(pygame.transform.scale(imgs['gutter'], (320, 12)), (65, 270))

    # Tank  →  x=400, y=320, w=95, h=170
    TANK_IMG_X, TANK_IMG_Y = 400, 320
    TANK_IMG_W, TANK_IMG_H = 95, 170
    if imgs.get('tank'):
        surface.blit(pygame.transform.scale(imgs['tank'], (TANK_IMG_W, TANK_IMG_H)),
                     (TANK_IMG_X, TANK_IMG_Y))

    # Tank-to-field pipe image
    tank_pipe_x = TANK_IMG_X + TANK_IMG_W
    tank_pipe_y = TANK_IMG_Y + TANK_IMG_H - 16
    tank_pipe_w = int(field_top_left[0]) - tank_pipe_x
    if imgs.get('pipe') and tank_pipe_w > 0:
        surface.blit(pygame.transform.scale(imgs['pipe'], (tank_pipe_w, 16)),
                     (tank_pipe_x, tank_pipe_y))

    # Field  →  bounding box of trapezoid
    if imgs.get('field'):
        xs   = [p[0] for p in field_points]
        ys   = [p[1] for p in field_points]
        bb_x = int(min(xs));  bb_y = int(min(ys))
        bb_w = int(max(xs) - min(xs));  bb_h = int(max(ys) - min(ys))
        surface.blit(pygame.transform.scale(imgs['field'], (bb_w, bb_h)), (bb_x, bb_y))

    # Plants image overlay (always shown, on top of field)
    if imgs.get('plant'):
        plant_size = 40
        for row in range(rows):
            t_row   = (row + 0.5) / rows
            left_x  = field_top_left[0]  + (field_bottom_left[0]  - field_top_left[0])  * t_row
            left_y  = field_top_left[1]  + (field_bottom_left[1]  - field_top_left[1])  * t_row
            right_x = field_top_right[0] + (field_bottom_right[0] - field_top_right[0]) * t_row
            usable_left  = left_x  + margin
            usable_right = right_x - margin
            for col in range(cols):
                t_col  = (col + 0.5) / cols
                px     = usable_left + (usable_right - usable_left) * t_col
                py     = left_y
                p_img  = pygame.transform.scale(imgs['plant'], (plant_size, plant_size))
                surface.blit(p_img, (int(px - plant_size // 2), int(py - plant_size)))