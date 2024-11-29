"""
DELEAT THIS COMMENT AFTER READING
I was messing around with the code and, since I can't run it, there are likely to be bugs.
There might be bugs in the following
- if statemts loke col == "F", then try "F" in col == True
- in getHit, there is method if self.raining... this might have changed to snowing
- def tillSoil is called get_hit in video
- did some crazy stuff with randoms again in ln 96
- in plantSeed, does not work it's bc I didn't include checkWatered as an input, istead in the Plant class I called it directly
"""

import pygame
import settings
import random
from pytmx.util_pygame import load_pygame
from WaterTile import WaterTile
from Plant import Plant
from support import import_folder
from support import import_folder_dict

class SoilLayer():
    def __init__(self, allSprites):
        self.allSprites = allSprites

        # make groups of sprites to make catagoryzing easier
        self.soilGraphics = pygame.sprite.Group()
        self.waterGraphics = pygame.sprite.Group()
        self.plantGraphics = pygame.sprite.Group()
        
        # make and initialize soil grid and tilled soil grid
        self.makeSoilGrid()
        self.makeTilledSoilGrid

        # soil graphics
        self.soilImg = import_folder_dict('../graphics/soil/')
        self.waterImg = import_folder('../graphics/soil_water')

        # audio / sounds
        self.hoeSound = pygame.mixer.Sound('../audio/hoe.wav')
        self.hoeSound.set_volume(0.1)
        
        self.plantSound = pygame.mixer.Sound('../audio/plant.wav') 
        self.plantSound.set_volume(0.2)

    # SOIL SET-UP
    def makeSoilGrid(self):
        self.grid = []

        ground = pygame.image.load('../graphics/world/ground.png')
        width = ground.get_width() // TILE_SIZE
        height = ground.get_height() // TILE_SIZE
        # print(f"gird = {width} x {height}")
        
        # make grid
        for row in range(height):
            rList = []
            for h in range(width):
                rList.append([])
            self.grid.append(rList)
        # print(self.grid)

        # populate grid
        farmableLayer = load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles()
        for tile in farmableLayer:
            x = tile[0]
            y = tile[1]
            self.grid[y][x].append("F")
        # print(self.grid)

    def makeTilledSoilGrid(self):
        # using grid made from makeSoildGrid, then make a grid that is big enough to support graphcs if framable
        self.tilledRects = []
        iRow = 0
        for row in self.grid:
            iCol = 0
            for col in row:
                if col == "F":
                    # sizes fror rect
                    x = iCol * TILE_SIZE
                    y = iRow * TILE_SIZE

                    # pygame.rect imputs (x pos, y pos, hight,  width)
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.tilledRects.append(rect)
                iCol += 1
            iRow += 1

    # SOIL INTERACTION
    def water (self, wateringPos):
        for soil_sprite in self.soilSprites.sprites(): 
            if soil_sprite.rect.collidepoint(wateringPos):
            # print("soil tile watered")

                # add w to tile
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append("W")
                # chose a random image from waterImg

                r = random.randint(0, len(self.waterImg))
                WaterTile(pos = soil_sprite.rect.topleft, 
                        surf = self.waterImg[r], 
                        grpups = [self.allSprites, self.waterGraphics]) #pos, surface, groups

    def tillSoil(self, hitPos):
        # for each rectangle, check if was hit using hitPos
        for rect in self.tilledRects:
            if rect.collidepoint(hitPos):
                # if so, put hitPos back into grid
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                
                # if position farmable
                if 'F' in self.grid[y][x]:
                    # print("farmable")
                    self.grid[y][x].append('X')
                    self.makeTilledSoilGrid() # updage grid
                
                    if self.raining():
                        self.waterAll()

                # sound
                self.hoeSound.play()

    def plantSeed(self, seed, targetPos):
        # go through soilGraphics groups, once it is at the correct img (based on targetPos), plant seed
        for soilGraphics in self.soilGraphics.sprites():
            if soilGraphics.rect.collidepoint(targetPos):
                # check that there isn't already a plant there
                # figure out coordiantes of where to plant seed
                x = soilGraphics.rect.x // TILE_SIZE
                y = soilGraphics.rect.y // TILE_SIZE

                if "P" not in self.grid[y][x]:
                    # sound
                    self.plantSoundplay()
                    # plant
                    Plant(plantType= seed,
                        groups= [self.allSprites, self.plantGraphics],
                        soil= soilGraphics)

    # STATUS
    def waterAll(self): #for rain
        # itterate through grid
        iRow = 0
        for row in self.grid:
            iCol = 0
            for col in row:
                # if tilled but not watered, water
                if col.count('X') > 0 and col.count('W') == 0:
                    col.append("W")
                    x = iCol * TILE_SIZE
                    y = iRow * TILE_SIZE
                    
                    r = random.randint(0, len(self.waterImg))
                    WaterTile(pos = (x, y), 
                              surf = self.waterImg[r], 
                              groups = [self.all_sprites, self.water_sprites])
                iCol += 1
            iRow += 1

    def removeWater(self): #for re-start after sleep
        # destroy all water sprites
        for sprite in self.waterSprites.sprites():
            sprite.kill()

		# clean up the grid
        for row in self.grid:
            for tile in row:
                if tile == "W":
                    tile.remove("W")

    def updatePlants(self):
        for plant in self.plantGraphics.sprites():
            plant.grow()
               
    def checkWatered(self, plantPos):
        x = plantPos[0] // TILE_SIZE
        y = plantPos[1] // TILE_SIZE

        gridCell = self.grid[y][x]
        if 'W' in gridCell:
            return True
        else:
            return False
