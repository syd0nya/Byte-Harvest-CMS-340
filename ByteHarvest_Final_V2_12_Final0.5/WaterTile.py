# import pygame
# from constants import *
# class WaterTile(pygame.sprite.Sprite):
# 	def __init__(self, pos, surf, groups):
# 		# same logic as soilTile, just different layer... image imput will be different
# 		super().__init__(groups)
# 		self.image = surf
# 		self.rect = self.image.get_rect(topleft = pos)
# 		self.layer = LAYERS['soil water']

import pygame
from constants import LAYERS

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        
        # Animation setup
        self.frames = frames
        self.frame_index = 0
        
        # Sprite setup
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Layer setup
        self.z = LAYERS['water']

    def animate(self, dt):
        # Update frame index
        self.frame_index += 5 * dt
        
        # Loop animation
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        # Update image
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)