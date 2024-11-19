# Particle class to show when an object is being destroyed/consumed
# Maggie, building off work in Emily's branch at 10:00 pm 11/18/20224

import pygame, sys
from settings import *
from level import Level
from sprites import GenericFloor

# Maggie addition, 10:00 pm 11/18/2024 -------------------------------------------------

# Particle class, used to show when an object is being consumed
# Inherits from Generic Class
class Particle(GenericFloor):

    # Inherit constructor
    def __init__(self, pos, surf, groups, z, duration = 200):
        super.__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks() # Get time of creation
        self.duration = duration # Store duration input as an attribute of the object

        # White surface over object
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface() # silhouette of original surface
        new_surf.set_colorkey((0,0,0)) # turning silhouette pure white
        self.image = new_surf

    # Self update method to clear sprite
    def update(self, dt):

        # Check duration of sprite life
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()