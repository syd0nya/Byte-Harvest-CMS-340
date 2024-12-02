import pygame
import constants

"""
DE BUGGING
If you are getting issues then it is probably from
ln 24 and/or 30, add .convert_alpha() to end... example: toolImg = pygame.image.load(toolImgPath).convert_alpha()

rn overlay is at top left... if u want that to change, go to ln 3
"""

class Overlay:
    def __init__(self, player):
        #draw directly on display surface
        self.displaySurface = pygame.display.get_surface()
        self.player = player

        # create surfaces for tools and seeds accecsed through key-value-pair by...
        # for each tool/seed create path --> load img --> add to correct layer
        self.overlayFolder = "graphics/overlay/"
        self.toolsSurf = {}
        for tool in player.tools:
            toolImgPath = f"{self.overlayFolder}{tool}.png"
            toolImg = pygame.image.load(toolImgPath).convert_alpha()
            self.tools_surf[tool] = toolImg

        self.seedsSurf = {}
        for seed in player.seeds:
            seedImgPath = f"{self.overlayFolder}{seed}.png"
            seedImg = pygame.image.load(seedImgPath).convert_alpha()
            self.seeds_surf[seed] = seedImg
        # print(self.toolsSurf)
        # print(self.seedsSurf)

# for putting images on top of 
    def display(self):
        # get the surface from seed/tool Surf [] from init using player input as i
        toolsSurf = self.toolsSurf[self.player.selected_tool()]
        self.displaySurface.blit(toolsSurf(0,0)) #top left of screen

        # seeds
        seedsSurf = self.seedsSurf[self.player.selected_seed()]
        self.displaySurface.blit(seedsSurf(10,0))



