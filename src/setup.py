import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def setup_pygame():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Maze Agent")

def setup_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.1, 1.1, -1.1, 1.1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def handle_events():
    keys = {"up": False, "down": False, "left": False, "right": False, "restart": False, "quit": False}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keys["quit"] = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keys["quit"] = True
            elif event.key == pygame.K_SPACE:
                keys["restart"] = True
            elif event.key == pygame.K_UP:
                keys["up"] = True
            elif event.key == pygame.K_DOWN:
                keys["down"] = True
            elif event.key == pygame.K_LEFT:
                keys["left"] = True
            elif event.key == pygame.K_RIGHT:
                keys["right"] = True
    return keys

def process_movement(agent, maze, key_states):
    directions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    for key, (dx, dy) in directions.items():
        if key_states[key]:
            key_states[key] = False
            moved = agent.move(dx, dy, maze)
            return moved, not moved
    return False, False

