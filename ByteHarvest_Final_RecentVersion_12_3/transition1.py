# # Class to transition the user from one day to the next

# # Imports
# import pygame
# from constants import *

# class Transition:
#     def __init__(self, reset, player):
#         # Constructor

#         # Get the display surface
#         self.display_surface = pygame.display.get_surface()

#         # Get the reset function from Level
#         self.reset = reset

#         # Get the player
#         self.player = player

#         # Set the overlay image for the color change on the whole screen
#         self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

#         # Set the initial overlay color
#         self.color = 255

#         # Set the color change speed
#         self.speed = -2

#     def play(self):
#         # Play the transition between days
#         print("play")

#         # Change the color gradually
#         self.color += self.speed

#         # If the color hits the bottom
#         if self.color <= 0:
#             # Start the lightening and reset everything
#             self.speed *= -1
#             self.color = 0
#             self.reset()

#         # If the color hits the top
#         elif self.color >= 255:
#             # Make the player stop sleeping
#             self.player.sleep = False

#             # Reset the speed for the next play call
#             self.speed = -2
#             self.color = 255

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Transition:
    def __init__(self, reset, player):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # Overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255  # Starting with white
        self.speed = -2   # Speed of the fade

    def play(self):
        # Fade to black
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1  # Reverse the fade
            self.color = 0
            self.reset()      # Reset the level when fully black
        
        # Return to white and end transition
        if self.color >= 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2

        # Fill overlay with current color
        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)