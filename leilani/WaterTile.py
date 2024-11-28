import pygame
import settings

class WaterTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		# same logic as soilTile, just different layer... image imput will be different
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.layer = LAYERS['soil water']