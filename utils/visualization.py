import pygame
import sys
from simulation.environment import Environment
import random

CAR_COLORS = [
    (255, 99, 71),    # red
    (30, 144, 255),   # blue
    (255, 215, 0),    # yellow
    (50, 205, 50),    # green
    (255, 105, 180),  # pink
    (255, 140, 0),    # orange
    (138, 43, 226)    # purple
]
WIDTH, HEIGHT = 700, 650   # bigger window
ROAD_WIDTH = 120

# COLORS
GRASS = (34, 139, 34)
ROAD = (50, 50, 50)
LANE = (240, 240, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
UI_BG = (30, 30, 30)
CAR = (0, 170, 255)

DIRECTIONS = ["N", "S", "E", "W"]


#  DRAW ROADS
def draw_roads(screen):
    screen.fill(GRASS)

    pygame.draw.rect(screen, ROAD, (WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.rect(screen, ROAD, (0, HEIGHT//2 - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH))

    # lane markings
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, LANE, (WIDTH//2, i), (WIDTH//2, i+20), 2)

    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, LANE, (i, HEIGHT//2), (i+20, HEIGHT//2), 2)


#  DRAW CARS
def draw_cars(screen, queues):
    spacing = 20

    # North
    max_visible = 12
    for i in range(min(len(queues["N"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (WIDTH//2 - 30, 20 + i*spacing, 14, 20))

    # South
    for i in range(min(len(queues["S"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (WIDTH//2 + 15, HEIGHT - 20 - i*spacing, 14, 20))

    # West
    for i in range(min(len(queues["W"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (20 + i*spacing, HEIGHT//2 + 15, 20, 14))

    # East
    for i in range(min(len(queues["E"]), max_visible)):
        color = CAR_COLORS[i % len(CAR_COLORS)]
        pygame.draw.rect(screen, color, (WIDTH - 20 - i*spacing, HEIGHT//2 - 30, 20, 14))

#   LIGHT PANELS
def draw_lights(screen, green):
    font = pygame.font.SysFont(None, 20)

    for d, pos in {
        "N": (WIDTH//2, HEIGHT//2 - 90),
        "S": (WIDTH//2, HEIGHT//2 + 90),
        "W": (WIDTH//2 - 90, HEIGHT//2),
        "E": (WIDTH//2 + 90, HEIGHT//2)
    }.items():

        color = GREEN if d == green else RED

        # box
        pygame.draw.rect(screen, BLACK, (*pos, 30, 30))
        pygame.draw.circle(screen, color, (pos[0]+15, pos[1]+15), 10)

        label = font.render(d, True, WHITE)
        screen.blit(label, (pos[0]+10, pos[1]-15))


# GAME UI PANEL
def draw_ui(screen, env):
    font = pygame.font.SysFont(None, 26)

    # panel background
    pygame.draw.rect(screen, UI_BG, (0, HEIGHT-80, WIDTH, 80))

    text1 = font.render(f"Time: {env.time}", True, WHITE)
    text2 = font.render(f"Cars Passed: {env.cars_passed}", True, WHITE)
    text3 = font.render(f"Total Wait: {env.total_wait}", True, WHITE)

    screen.blit(text1, (20, HEIGHT-70))
    screen.blit(text2, (250, HEIGHT-70))
    screen.blit(text3, (500, HEIGHT-70))

    # queues
    q_text = font.render(f"Queues: {env.queues}", True, WHITE)
    screen.blit(q_text, (20, HEIGHT-40))


# MAIN LOOP
def run_animation(algorithm_func, total_steps):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(" Traffic Simulation")

    clock = pygame.time.Clock()
    env = Environment()

    for _ in range(total_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # LOGIC (unchanged)
        env.step(algorithm_func)
        green = algorithm_func(env.queues, env.time)

        # DRAW
        draw_roads(screen)
        draw_cars(screen, env.queues)
        draw_lights(screen, green)
        draw_ui(screen, env)

        pygame.display.flip()

        clock.tick(10)
    pygame.quit()
    return env