
import pygame
from pygame import Vector2

pygame.font.init()



SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
TILE_SIZE = 64

# movement speed
SPEED = 200


OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50,40),
    'right': Vector2(50,40),
    'up': Vector2(0,-10),
    'down': Vector2(0,50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'snow ground': 7,    # Ground snow accumulation effects
    'snow falling': 8,   # The falling snow
    'main': 9,          
    'house top': 10,
    'fruit': 11
}

APPLE_POS = {
    'Small': [(18,17), (30,37), (30,45), (20,30), (30,10)],
    'Large': [(30,24), (60,65), (16,40), (45,50), (42,70)]
}

GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}
