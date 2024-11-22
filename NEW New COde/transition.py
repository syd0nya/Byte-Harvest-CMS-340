import pygame
import constants as c

class Transition:
    def __init__(self, reset, player):
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        #overlay images
        self.image = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play(self):
        # reset --> wake up --> set spped to -2


        self.color += self.speed
        # make sure it stays within rgb range
        if self.color <=0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2
        self.image.fill(r=self.color, g=self.color, b=self.color) #(255, 255, 255) = white
        self.display_surface.blit(self.image,(0,0), special_flags=pygame.BLEND_RGBA_MULT)