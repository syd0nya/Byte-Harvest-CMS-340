import pygame
from pygame.math import Vector2

# Constants that are used throughout classes


# screen size based on monitor
pygame.init()
userScreen = pygame.display.Info()

# Subtract height for exit bar
SCREEN_WIDTH = userScreen.current_w #1280
SCREEN_HEIGHT = userScreen.current_h - 60 #720
FARM_HEIGHT = SCREEN_HEIGHT * 0.3
TILE_SIZE = 64

# Text page settings (room for 55 characters across)
PAGE_WIDTH = 800
PAGE_HEIGHT = 600

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

# layers of surfaces (what goes on top of what)
LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

# Where do apples go on trees
APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

# How fast crops grow
GROW_SPEED = {
	'corn': 3,
	'tomato': 0.7
}

# How much crops sell for
SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}

# How much crops cost to buy
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}