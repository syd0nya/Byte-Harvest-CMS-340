import pygame
from pygame import Vector2

pygame.font.init()

# Screen dimensions
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
TILE_SIZE = 64

# Farm dimensions
FARM_HEIGHT = SCREEN_HEIGHT / 2
FARM_WIDTH = SCREEN_WIDTH

# Page dimensions for editor
PAGE_HEIGHT = 600
PAGE_WIDTH = 1000
MAX_CHARACTERS = 64

# Movement speed
SPEED = 200

# UI Positions
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

# Tool offset positions
PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50,40),
    'right': Vector2(50,40),
    'up': Vector2(0,-10),
    'down': Vector2(0,50)
}

# Rendering layers
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'snow ground': 5,
    'house bottom': 6,
    'ground plant': 7,
    'main': 8,
    'house top': 9,
    'snow ground': 10,
    'snow falling': 11,
    'fruit': 12,
    'overlay': 13,
}

# Apple positions for trees
APPLE_POS = {
    'Small': [(18,17), (30,37), (30,45), (20,30), (30,10)],
    'Large': [(30,24), (60,65), (16,40), (45,50), (42,70)]
}

# Growth speeds
GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

# Economy
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20
}

PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5
}

ANIMAL_SETTINGS = {
    'cow': {
        'frame_width': 32,
        'frame_height': 32,
        'animation_speed': 0.1,  # Slower animation
        'scale': 2.5  # Bigger sprite
    },
    'pig': {
        'frame_width': 32,
        'frame_height': 32,
        'animation_speed': 0.1,
        'scale': 2.5
    },
    'chicken': {
        'frame_width': 32,
        'frame_height': 32,
        'animation_speed': 0.1,
        'scale': 2.5
    }
}