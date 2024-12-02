import pygame
from constants import *
from support import import_folder
from WaterTile import WaterTile

class SoilLayer:
    def __init__(self, allSprites):
        self.allSprites = allSprites
        self.soilGraphics = pygame.sprite.Group()
        self.waterGraphics = pygame.sprite.Group()
        self.plantGraphics = pygame.sprite.Group()
        self.makeSoilGrid()
        self.makeTilledSoilGrid()

        self.soilImg = import_folder('graphics/soil/')
        self.waterImg = import_folder('graphics/soil_water')

    def makeSoilGrid(self):
        # Logic for creating the soil grid
        pass

    def makeTilledSoilGrid(self):
        # Logic for creating tilled soil
        pass

    def plantSeed(self, seed, targetPos, plant_class):
        """Inject the Plant class to avoid circular import."""
        for soilGraphics in self.soilGraphics.sprites():
            if soilGraphics.rect.collidepoint(targetPos):
                x = soilGraphics.rect.x // TILE_SIZE
                y = soilGraphics.rect.y // TILE_SIZE
                if "P" not in self.grid[y][x]:
                    plant_class(
                        plantType=seed,
                        groups=[self.allSprites, self.plantGraphics],
                        soil=soilGraphics
                    )
