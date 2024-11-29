import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
	def __init__(self, farmSurface):
		super().__init__()
		self.farm_surface = farmSurface
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - FARM_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					# Draw to the farm screen
					self.farm_surface.blit(sprite.image, offset_rect)
			
					
