import pygame
import math

def draw_scene(surface, width, height, intensity, watering_active, imgs):
    intensity = max(0.0, min(1.0, intensity))

    CLEAR_SKY  = (135, 206, 235)
    STORMY_SKY = (20, 20, 40)

    def lerp(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    SKY_COLOR    = lerp(CLEAR_SKY, STORMY_SKY, intensity)
    GROUND_COLOR = (40, 80, 40)
    ROOF_COLOR   = (140, 70, 40)
    GUTTER_COLOR = (120, 120, 130)
    PIPE_COLOR   = (120, 120, 130)
    TANK_FRONT   = (60, 100, 160)
    GARDEN_SOIL  = (107, 75, 16)
    PLANT_COLOR  = (20, 150, 20)

    surface.fill(SKY_COLOR)

    # Ground 
    ground_y = height - 200
    #pygame.draw.rect(surface, GROUND_COLOR, (0, ground_y, width, 200))

    # House  →  image: x=80, y=260, w=300, h=210
    HOUSE_IMG_X, HOUSE_IMG_Y = 80,  260
    HOUSE_IMG_W, HOUSE_IMG_H = 300, 210
    #pygame.draw.rect(surface, SKY_COLOR, (HOUSE_IMG_X, HOUSE_IMG_Y, HOUSE_IMG_W, HOUSE_IMG_H))

    # Roof  →  image: x=70, y=170, w=320, h=90
    ROOF_IMG_X, ROOF_IMG_Y = 70,  170
    ROOF_IMG_W, ROOF_IMG_H = 320, 90
    
    # Trapezoid corners matched to bounding box of image
    roof_points = [
        (ROOF_IMG_X + 20, ROOF_IMG_Y),                    # back-left
        (ROOF_IMG_X + ROOF_IMG_W - 20, ROOF_IMG_Y),                    # back-right
        (ROOF_IMG_X + ROOF_IMG_W, ROOF_IMG_Y + ROOF_IMG_H),       # front-right
        (ROOF_IMG_X, ROOF_IMG_Y + ROOF_IMG_H),       # front-left
    ]
    #pygame.draw.polygon(surface, ROOF_COLOR, roof_points)

    # Gutter  →  image: x=60, y=260, w=340, h=10
    GUTTER_IMG_X, GUTTER_IMG_Y = 60,  260
    GUTTER_IMG_W, GUTTER_IMG_H = 340, 10
    #pygame.draw.rect(surface, GUTTER_COLOR, (GUTTER_IMG_X, GUTTER_IMG_Y, GUTTER_IMG_W, GUTTER_IMG_H))

    # Tank  →  image: x=390, y=320, w=95, h=120
    TANK_IMG_X, TANK_IMG_Y = 390, 320
    TANK_IMG_W, TANK_IMG_H = 95,  120
    #pygame.draw.rect(surface, TANK_FRONT, (TANK_IMG_X, TANK_IMG_Y, TANK_IMG_W, TANK_IMG_H))

    # Gutter-to-tank pipe
    gutter_right_x    = GUTTER_IMG_X + GUTTER_IMG_W          # 400
    gutter_y          = GUTTER_IMG_Y                          # 260
    tank_top_center_x = TANK_IMG_X + TANK_IMG_W // 2         # 437
    drop_height       = TANK_IMG_Y - gutter_y                 # 60 (320-260)
    GUTTER_PIPE_W     = 6                                     # pipe thickness

    # Segment 1 — vertical drop from gutter right end downward
    gt_vert1_x = gutter_right_x - GUTTER_PIPE_W // 2
    gt_vert1_y = gutter_y
    gt_vert1_h = drop_height

    # Segment 2 — horizontal run from gutter right to above tank center
    gt_horiz_x = gutter_right_x - GUTTER_PIPE_W // 2
    gt_horiz_y = gutter_y + drop_height - GUTTER_PIPE_W // 2
    gt_horiz_w = tank_top_center_x - gutter_right_x + GUTTER_PIPE_W

    # Segment 3 — short vertical drop into tank top
    gt_vert2_x = tank_top_center_x - GUTTER_PIPE_W // 2
    gt_vert2_y = gutter_y + drop_height - GUTTER_PIPE_W // 2
    gt_vert2_h = 12

    # Always draw primitive fallback first
    #pygame.draw.rect(surface, PIPE_COLOR, (gt_vert1_x, gt_vert1_y, GUTTER_PIPE_W, gt_vert1_h))
    #pygame.draw.rect(surface, PIPE_COLOR, (gt_horiz_x, gt_horiz_y, gt_horiz_w, GUTTER_PIPE_W))
    #pygame.draw.rect(surface, PIPE_COLOR, (gt_vert2_x, gt_vert2_y, GUTTER_PIPE_W, gt_vert2_h))

    # Field trapezoid 
    field_w, field_h, field_offset = 260, 140, 40
    field_y = ground_y - field_h + 150
    field_x = TANK_IMG_X + TANK_IMG_W + 60    # 545

    field_points = [
        (field_x, field_y),
        (field_x + field_w, field_y),
        (field_x + field_w - field_offset, field_y + field_h),
        (field_x - field_offset, field_y + field_h),
    ]
    #pygame.draw.polygon(surface, GARDEN_SOIL, field_points)
    #pygame.draw.polygon(surface, (80, 110, 60), field_points, 2)

    field_top_left, field_top_right, field_bottom_right, field_bottom_left = field_points

    # Field edge pipes
    PIPE_WIDTH = 6
    #pygame.draw.line(surface, PIPE_COLOR, field_top_left,  field_bottom_left,  PIPE_WIDTH)
    #pygame.draw.line(surface, PIPE_COLOR, field_top_right, field_bottom_right, PIPE_WIDTH)

    # Tank-to-field horizontal pipe
    tank_pipe_x = TANK_IMG_X + TANK_IMG_W          # 485
    tank_pipe_y = TANK_IMG_Y + TANK_IMG_H - 25     # 415
    tank_pipe_w = int(field_top_left[0]) - tank_pipe_x
    #pygame.draw.rect(surface, PIPE_COLOR, (tank_pipe_x, tank_pipe_y, tank_pipe_w, PIPE_WIDTH))

    # Spray pipes across field
    PIPE_LINES  = 6
    spray_lines = []
    for i in range(PIPE_LINES):
        t  = i / (PIPE_LINES - 1)
        sy = int(field_top_left[1] + (field_bottom_left[1] - field_top_left[1]) * t)
        sx = int(field_top_left[0] + (field_bottom_left[0] - field_top_left[0]) * t)
        rx = int(field_top_right[0] + (field_bottom_right[0] - field_top_right[0]) * t)
        #pygame.draw.line(surface, PIPE_COLOR, (sx, sy), (rx, sy), 3)
        spray_lines.append((sx, sy, rx))

    # Primitive X plants
    rows, cols, line_len, margin = 5, 5, 7, 15
    for row in range(rows):
        t_row    = (row + 0.5) / rows
        left_x   = field_top_left[0]  + (field_bottom_left[0]  - field_top_left[0])  * t_row
        left_y   = field_top_left[1]  + (field_bottom_left[1]  - field_top_left[1])  * t_row
        right_x  = field_top_right[0] + (field_bottom_right[0] - field_top_right[0]) * t_row
        usable_left  = left_x  + margin
        usable_right = right_x - margin
        for col in range(cols):
            t_col = (col + 0.5) / cols
            px = usable_left + (usable_right - usable_left) * t_col
            py = left_y
            #pygame.draw.line(surface, PLANT_COLOR, (px - line_len, py - line_len), (px + line_len, py + line_len), 2)
            #pygame.draw.line(surface, PLANT_COLOR, (px - line_len, py + line_len), (px + line_len, py - line_len), 2)

    # ════════════════════════════════════════════════════════════════════════
    #  IMAGE OVERLAYS
    # ════════════════════════════════════════════════════════════════════════

    # 1. Ground
    if imgs.get('ground'):
        surface.blit(pygame.transform.scale(imgs['ground'], (width, 200)), (0, ground_y))

    # 2. House
    if imgs.get('house'):
        surface.blit(pygame.transform.scale(imgs['house'], (HOUSE_IMG_W, HOUSE_IMG_H)), (HOUSE_IMG_X, HOUSE_IMG_Y))

    # 3. Roof
    if imgs.get('roof'):
        surface.blit(pygame.transform.scale(imgs['roof'], (ROOF_IMG_W, ROOF_IMG_H)), (ROOF_IMG_X, ROOF_IMG_Y))

    # 4. Gutter
    if imgs.get('gutter'):
        surface.blit(pygame.transform.scale(imgs['gutter'], (GUTTER_IMG_W, GUTTER_IMG_H)),  (GUTTER_IMG_X, GUTTER_IMG_Y))

    # 4.5 Gutter - Tank 
    if imgs.get('pipe'):
        # Segment 1 — vertical drop
        if gt_vert1_h > 0:
            surf_v1 = pygame.transform.scale(imgs['pipe'], (GUTTER_PIPE_W, gt_vert1_h))
            surface.blit(surf_v1, (gt_vert1_x, gt_vert1_y))

        # Segment 2 — horizontal run
        if gt_horiz_w > 0:
            surf_h = pygame.transform.scale(imgs['pipe'], (gt_horiz_w, GUTTER_PIPE_W))
            surface.blit(surf_h, (gt_horiz_x, gt_horiz_y))

        # Segment 3 — short drop into tank
        if gt_vert2_h > 0:
            surf_v2 = pygame.transform.scale(imgs['pipe'], (GUTTER_PIPE_W, gt_vert2_h))
            surface.blit(surf_v2, (gt_vert2_x, gt_vert2_y))
    
    # 5. Tank
    if imgs.get('tank'):
        surface.blit(pygame.transform.scale(imgs['tank'], (TANK_IMG_W, TANK_IMG_H)), (TANK_IMG_X, TANK_IMG_Y))

    # 6. Tank-to-field pipe image
    if imgs.get('pipe') and tank_pipe_w > 0:
        surface.blit(pygame.transform.scale(imgs['pipe'], (tank_pipe_w, PIPE_WIDTH)), (tank_pipe_x, tank_pipe_y))

    # 7. Field image
    if imgs.get('field'):
        xs   = [p[0] for p in field_points]
        ys   = [p[1] for p in field_points]
        bb_x = int(min(xs));  bb_y = int(min(ys))
        bb_w = int(max(xs) - min(xs));  bb_h = int(max(ys) - min(ys))
        surface.blit(pygame.transform.scale(imgs['field'], (bb_w, bb_h)), (bb_x, bb_y))

    # 8. Pipe images over field
    if imgs.get('pipe'):
        SPRAY_PIPE_W = 6
        
        # Vertical feeder pipes on both left and right edges between rows
        for i, (sx, sy, rx) in enumerate(spray_lines):
            if i == 0:
                continue
            prev_sy  = spray_lines[i - 1][1]
            feeder_h = sy - prev_sy
            if feeder_h > 0:
                surf_l = pygame.transform.scale(imgs['pipe'], (SPRAY_PIPE_W, feeder_h))
                surface.blit(surf_l, (sx - SPRAY_PIPE_W // 2, prev_sy))
                surf_r = pygame.transform.scale(imgs['pipe'], (SPRAY_PIPE_W, feeder_h))
                surface.blit(surf_r, (rx - SPRAY_PIPE_W // 2, prev_sy))
        
        # Horizontal spray pipe images across each row
        for (sx, sy, rx) in spray_lines:
            h_len = rx - sx
            if h_len > 0:
                h_surf = pygame.transform.scale(imgs['pipe'], (h_len, SPRAY_PIPE_W))
                surface.blit(h_surf, (sx, sy - SPRAY_PIPE_W // 2))

    # 9. Plant images
    if imgs.get('plant'):
        plant_size = 40
        for row in range(rows):
            t_row    = (row + 0.5) / rows
            left_x   = field_top_left[0]  + (field_bottom_left[0]  - field_top_left[0])  * t_row
            left_y   = field_top_left[1]  + (field_bottom_left[1]  - field_top_left[1])  * t_row
            right_x  = field_top_right[0] + (field_bottom_right[0] - field_top_right[0]) * t_row
            usable_left  = left_x  + margin
            usable_right = right_x - margin
            for col in range(cols):
                t_col = (col + 0.5) / cols
                px    = usable_left + (usable_right - usable_left) * t_col
                py    = left_y
                p_img = pygame.transform.scale(imgs['plant'], (plant_size, plant_size))
                surface.blit(p_img, (int(px - plant_size // 2), int(py - plant_size)))

    # 10. Animated water jets
    if watering_active:
        current_time  = pygame.time.get_ticks()
        JET_SPACING   = 20
        JET_WIDTH     = 2
        MAX_JET_LEN   = 12
        WAVE_SPEED    = 400
        DROP_INTERVAL = 150
        DROP_FRAMES   = 4

        for (sx, sy, rx) in spray_lines:
            for x in range(sx, rx, JET_SPACING):
                phase_offset = (x - sx) * 60
                t = ((current_time + phase_offset) % WAVE_SPEED) / WAVE_SPEED
                jet_len = int(MAX_JET_LEN * (0.3 + 0.7 * abs(math.sin(t * math.pi))))
                pygame.draw.line(surface, (0, 200, 255), (x, sy), (x, sy - jet_len), JET_WIDTH)
                drop_frame = (current_time // DROP_INTERVAL + (x - sx) // JET_SPACING) % DROP_FRAMES
                drop_y     = sy + drop_frame * 4
                drop_alpha = max(0, 255 - drop_frame * 60)
                drop_surf  = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(drop_surf, (0, 180, 255, drop_alpha), (2, 2), 2)
                surface.blit(drop_surf, (x - 2, drop_y))