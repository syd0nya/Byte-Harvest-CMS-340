import pygame
from constants import *

class SoilTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups): # takes tile position, image of soil, and arr of groups that can interact
		super().__init__(groups)
		self.image = surf 
		self.rect = self.image.get_rect(topleft = pos)
		self.layer = LAYERS['soil'] #soild layer in constants
