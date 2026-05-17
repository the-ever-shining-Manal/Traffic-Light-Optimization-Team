import sys
import pygame
from simulation.environment import Environment

CAR_COLORS = [
    (255, 99, 71),    # red
    (30, 144, 255),   # blue
    (255, 215, 0),    # yellow
    (50, 205, 50),    # green
    (255, 105, 180),  # pink
    (255, 140, 0),    # orange
    (138, 43, 226),   # purple
]

WIDTH, HEIGHT = 1000, 650
ANIM_WIDTH = 700
ROAD_WIDTH = 120

# COLORS
GRASS = (34, 139, 34)
ROAD  = (50, 50, 50)
LANE  = (240, 240, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 50, 50)
GREEN = (50, 220, 50)
UI_BG = (30, 30, 30)
CAR   = (0, 170, 255)

DIRECTIONS = ["N", "S", "E", "W"]


# DRAW ROADS
def draw_roads(screen):
    screen.fill((0, 0, 0)) # Clear the entire screen
    pygame.draw.rect(screen, GRASS, (0, 0, ANIM_WIDTH, HEIGHT))

    pygame.draw.rect(screen, ROAD, (ANIM_WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.rect(screen, ROAD, (0, HEIGHT//2 - ROAD_WIDTH//2, ANIM_WIDTH, ROAD_WIDTH))

    # lane markings
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, LANE, (ANIM_WIDTH//2, i), (ANIM_WIDTH//2, i+20), 2)

    for i in range(0, ANIM_WIDTH, 40):
        pygame.draw.line(screen, LANE, (i, HEIGHT//2), (i+20, HEIGHT//2), 2)


# DRAW CARS
def draw_cars(screen, queues):
    spacing    = 20
    max_visible = 12

    # North
    for i in range(min(len(queues["N"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (ANIM_WIDTH//2 - 30, 20 + i*spacing, 14, 20))

    # South
    for i in range(min(len(queues["S"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (ANIM_WIDTH//2 + 15, HEIGHT - 20 - i*spacing, 14, 20))

    # West
    for i in range(min(len(queues["W"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (20 + i*spacing, HEIGHT//2 + 15, 20, 14))

    # East
    for i in range(min(len(queues["E"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (ANIM_WIDTH - 20 - i*spacing, HEIGHT//2 - 30, 20, 14))


# LIGHT PANELS
def draw_lights(screen, green):
    font = pygame.font.SysFont(None, 20)

    for d, pos in {
        "N": (ANIM_WIDTH//2, HEIGHT//2 - 90),
        "S": (ANIM_WIDTH//2, HEIGHT//2 + 90),
        "W": (ANIM_WIDTH//2 - 90, HEIGHT//2),
        "E": (ANIM_WIDTH//2 + 90, HEIGHT//2),
    }.items():

        color = GREEN if d == green else RED

        # box
        pygame.draw.rect(screen, BLACK, (*pos, 30, 30))
        pygame.draw.circle(screen, color, (pos[0]+15, pos[1]+15), 10)

        label = font.render(d, True, WHITE)
        screen.blit(label, (pos[0]+10, pos[1]-15))


# SIDE PANEL
def draw_side_panel(screen, env, green):
    pygame.draw.rect(screen, (40, 40, 45), (ANIM_WIDTH, 0, WIDTH - ANIM_WIDTH, HEIGHT - 80))
    pygame.draw.line(screen, (100, 100, 100), (ANIM_WIDTH, 0), (ANIM_WIDTH, HEIGHT - 80), 2)
    
    font_title = pygame.font.SysFont(None, 36)
    font_large = pygame.font.SysFont(None, 48)
    font_normal = pygame.font.SysFont(None, 32)
    
    title = font_title.render("Live Traffic Data", True, WHITE)
    screen.blit(title, (ANIM_WIDTH + 20, 20))
    
    gl_text = font_normal.render("Current Green:", True, WHITE)
    screen.blit(gl_text, (ANIM_WIDTH + 20, 80))
    
    gl_val = font_large.render(green, True, GREEN)
    screen.blit(gl_val, (ANIM_WIDTH + 200, 72))
    
    q_title = font_normal.render("Cars Waiting:", True, WHITE)
    screen.blit(q_title, (ANIM_WIDTH + 20, 150))
    
    y_offset = 200
    for d in ["N", "S", "E", "W"]:
        color = GREEN if d == green else WHITE
        d_text = font_large.render(f"Lane {d}: {len(env.queues[d])}", True, color)
        screen.blit(d_text, (ANIM_WIDTH + 40, y_offset))
        y_offset += 60

# GAME UI PANEL
def draw_ui(screen, env):
    font = pygame.font.SysFont(None, 26)

    # panel background
    pygame.draw.rect(screen, UI_BG, (0, HEIGHT-80, WIDTH, 80))

    text1 = font.render(f"Time: {env.time}",          True, WHITE)
    text2 = font.render(f"Cars Passed: {env.cars_passed}", True, WHITE)
    text3 = font.render(f"Total Wait: {env.total_wait}",  True, WHITE)

    screen.blit(text1, (20,  HEIGHT-70))
    screen.blit(text2, (250, HEIGHT-70))
    screen.blit(text3, (500, HEIGHT-70))

    # FIX: show queue lengths instead of raw deque objects
    q_text = font.render(
        f"N:{len(env.queues['N'])}  "
        f"S:{len(env.queues['S'])}  "
        f"E:{len(env.queues['E'])}  "
        f"W:{len(env.queues['W'])}",
        True, WHITE,
    )
    screen.blit(q_text, (20, HEIGHT-40))


# MAIN LOOP
def run_animation(algorithm_func, total_steps):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Traffic Simulation")

    clock = pygame.time.Clock()
    env   = Environment()

    for _ in range(total_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # FIX: separate step so we can draw cars BEFORE they are removed
        green = env.pre_step(algorithm_func)

        # DRAW
        draw_roads(screen)
        draw_cars(screen, env.queues)
        draw_lights(screen, green)
        draw_side_panel(screen, env, green)
        draw_ui(screen, env)

        env.post_step()

        pygame.display.flip()
        clock.tick(3)

    pygame.quit()
    return env