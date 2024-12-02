

import pygame
from constants import *
import random
from SoilLayer import SoilLayer
from support import import_folder

class Plant(pygame.sprite.Sprite):
    def __init__(self, plantType, groups, soil):
        super().__init__(groups)
        self.plantType = plantType
        self.soil = soil
        self.layer = LAYERS['ground plant']
        self.plantGraphics = import_folder('/graphics/plant/{plantType}')
        self.age = 0
        self.lifeSpan = len(self.plantGraphics) - 1
        self.rect = self.image.get_rect(midbottom=soil.rect.midbottom)
        self.currentGraphic = self.plantGraphics[self.age]
        
        # 50% chance, standard grow speed
        # 50% chance, different grow speed
        # seed random for testing pruposes, comment out later
        random.seed(123) 
        r = random.randint(1, 10)
        if r % 2 == 0:
            self.growSpeed = GROW_SPEED
        else:
            self.growSpeed = r/10
            
        # sprites
        self.rect = self.image.get_rect(midB = soil.rect.midbottom) #place sprite at the middle of the bottom of soil sprite 
        self.currentGaphic = self.plantGraphics[self.age]

        self.canHarvest = False

    def grow(self):
        if SoilLayer.checkWatered(self.rect.center): #any position works, here, as long as it's the soil tile
            # if at max life
            if self.age + 1 >= self.lifeSpan:
                # stop ageing
                self.age = self.lifeSpan
                self.canHarvest = True
            else:
                self.age += self.growSpeed

            # udate img
            intOfAge = int(self.age) # growSpeed can be a float, but we need the index value to be an int
            self.currentGaphic = self.plantGraphics[intOfAge]

            self.rect = self.image.get_rect(midB = self.soil.rect.midbottom) #img size changes --> make new rect


