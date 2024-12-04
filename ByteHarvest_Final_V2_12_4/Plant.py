

# import pygame
# from constants import *
# import random
# from SoilLayer import SoilLayer
# from support import import_folder

# class Plant(pygame.sprite.Sprite):
#     def __init__(self, plantType, groups, soil):
#         super().__init__(groups)
#         self.plantType = plantType
#         self.soil = soil
#         self.layer = LAYERS['ground plant']
#         self.plantGraphics = import_folder('/graphics/plant/{plantType}')
#         self.age = 0
#         self.lifeSpan = len(self.plantGraphics) - 1
#         self.rect = self.image.get_rect(midbottom=soil.rect.midbottom)
#         self.currentGraphic = self.plantGraphics[self.age]
        
#         # 50% chance, standard grow speed
#         # 50% chance, different grow speed
#         # seed random for testing pruposes, comment out later
#         random.seed(123) 
#         r = random.randint(1, 10)
#         if r % 2 == 0:
#             self.growSpeed = GROW_SPEED
#         else:
#             self.growSpeed = r/10
            
#         # sprites
#         self.rect = self.image.get_rect(midB = soil.rect.midbottom) #place sprite at the middle of the bottom of soil sprite 
#         self.currentGaphic = self.plantGraphics[self.age]

#         self.canHarvest = False

#     def grow(self):
#         if SoilLayer.checkWatered(self.rect.center): #any position works, here, as long as it's the soil tile
#             # if at max life
#             if self.age + 1 >= self.lifeSpan:
#                 # stop ageing
#                 self.age = self.lifeSpan
#                 self.canHarvest = True
#             else:
#                 self.age += self.growSpeed

#             # udate img
#             intOfAge = int(self.age) # growSpeed can be a float, but we need the index value to be an int
#             self.currentGaphic = self.plantGraphics[intOfAge]

#             self.rect = self.image.get_rect(midB = self.soil.rect.midbottom) #img size changes --> make new rect

import pygame
from constants import *
import random
from support import import_folder

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        
        # Setup
        self.plant_type = plant_type
        self.frames = import_folder(f'graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered
        
        # Growth
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        
        # Sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -16
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
        self.z = LAYERS['ground plant']

        # Attributes
        self.harvestable = False
        
        # Randomize growth speed (50% chance of different speed)
        random.seed(123)  # For testing - remove in production
        r = random.randint(1, 10)
        if r % 2 == 0:
            self.grow_speed = GROW_SPEED[self.plant_type]
        else:
            self.grow_speed = r/10

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            # If plant reaches max age
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            # Update sprite
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
