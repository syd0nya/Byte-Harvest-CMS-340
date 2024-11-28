"""
DELEAT THIS COMMENT AFTER READING
I was messing around with the code and, since I can't run it, there are likely to be bugs.
There might be bugs in the following
- might be missing some things to import:
    - from pytmx.util_pygame import load_pygame
    - from support import *
- __init__ self.planGraphics calls on the 'plant' folder instead of the 'friut' folder
- was messing around with grow speed... line 32-37 messes with random int values
- seeded the random for testing purposes... comment out that line latter (ln 33)
- If the plant sprite is too low on the soil, it's bc I did not add the y_offset... if it end's up looking ugly, the code for it is in 5:10:30 of the video
- I did not include the code of section that makes fully grown plants objects you can bump into... if you want that, go to video section 5:20:52 - 5:24:23
"""

import pygame
import settings
import random
from SoilLayer import SoilLayer

class Plant(pygame.sprite.Sprite):
    def __init__(self, plantType, gorups, soil):
        super().__init__(gorups)
        self.plantType = plantType
        self.groups = gorups
        self.soil = soil
        self.layer = LAYERS["ground plant"]

        if plantType == "corn" or "tomato":
            self.plantGraphics = import_folder("../graphics/plant/{plantType}")
        else: # if, for some reason plantType is not valid, plant tomato by default
            self.plantGraphics = import_folder("../graphics/plant/tomato")

        self.age = 0
        self.lifeSpan = len(self.plantGraphics) - 1 # lifeSpan depends on how many frames it takes for it to grow
        
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


