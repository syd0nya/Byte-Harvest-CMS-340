# # Class to store user-input text

# # Imports
# import pygame, pygame.draw
# from constants import *

# class Editor:

#     # No args constructor
#     def __init__(self):
#         # Display surface to draw onto
#         self.display_surface = pygame.display.get_surface()

#         # Initialize pygame's built-in font module to make a font object
#         pygame.font.init()
#         self.font = pygame.font.SysFont("couriernew", 24) # Monospaced pygame font

#         # Render initial text
#         self.text = self.font.render('', True, 'black', 'white') # Black text on white background

#         # Set the text to appear in the center of the page
#         self.textRect = self.text.get_rect()
#         self.textRect.center = (SCREEN_WIDTH/2 - 450, SCREEN_HEIGHT/5)

#         self.pageOffset = 0

#         # User input
#         self.userInput = ""

#     def run(self, textSide):        
#         # Make the background color with day color
#         background = textSide
#         self.display_surface.fill((114, 183, 219), background) # light blue

#         # Make a white rectangle for the actual page
#         pygame.draw.rect(self.display_surface, 'white', pygame.Rect((SCREEN_WIDTH/2)-(PAGE_WIDTH/2), 
#                                                                     (SCREEN_HEIGHT/8), 
#                                                                     PAGE_WIDTH, PAGE_HEIGHT))
        
#         # Draw the margins on the page
#         pygame.draw.rect(self.display_surface, 'black', pygame.Rect((SCREEN_WIDTH/2) - 460,
#                                                                     (SCREEN_HEIGHT/8),
#                                                                     2, PAGE_HEIGHT))
#         pygame.draw.rect(self.display_surface, 'black', pygame.Rect((SCREEN_WIDTH/2) + 460,
#                                                                     (SCREEN_HEIGHT/8),
#                                                                     2, PAGE_HEIGHT))

#         event_list = pygame.event.get(pygame.KEYDOWN)
#         self.handle_events(event_list)

#         self.display()
    
#     def display(self):
#         # Reprint the text
#         self.text = self.font.render(self.userInput, True, 'black', 'white')

#         # Update the editor
#         self.display_surface.blit(self.text, self.textRect)


#     # Handle all the key strokes
#     # (If you try to do it in the run method pygame misses some of the keystrokes)
#     def handle_events(self, events):
#         # If any event happens, check for user input
#         for event in events:
#             if event.type == pygame.KEYDOWN:
#                 # Is it a letter or space
#                 if event.key < 127 and event.key > 33:
#                     # Is it an uppercase letter
#                     if event.mod == 1:
#                         self.userInput += pygame.key.name(event.key).upper()
#                     else:
#                         self.userInput += pygame.key.name(event.key)

#                 # Is it a backspace
#                 elif (event.key == 8) and (self.userInput.__len__() > 0):
#                     # Get string without the last character
#                     s = self.userInput[:-1]

#                     # Reassign userInput
#                     self.userInput = s

#                 # Is it a space
#                 elif event.key == 32:
#                     self.userInput += " "

#                 # Is it enter
#                 elif event.key == 13:
#                     self.userInput = self.userInput.ljust(MAX_CHARACTERS)

import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, 
    PAGE_WIDTH, PAGE_HEIGHT, 
    MAX_CHARACTERS
)

class Editor:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Initialize pygame's font module
        pygame.font.init()
        self.font = pygame.font.SysFont("couriernew", 24)  # Monospaced font

        # Initial text setup
        self.text = self.font.render('', True, 'black', 'white')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (SCREEN_WIDTH/2 - 450, SCREEN_HEIGHT/5)

        # Page offset for scrolling
        self.page_offset = 0

        # User input storage
        self.user_input = ""

    def run(self, text_side):
        # Draw background
        background = text_side
        self.display_surface.fill((114, 183, 219), background)  # Light blue background

        # Draw the page
        self.draw_page()
        
        # Handle input
        event_list = pygame.event.get(pygame.KEYDOWN)
        self.handle_events(event_list)

        # Display current text
        self.display()

    def draw_page(self):
        # Draw white page background
        pygame.draw.rect(
            self.display_surface, 
            'white', 
            pygame.Rect(
                (SCREEN_WIDTH/2)-(PAGE_WIDTH/2), 
                (SCREEN_HEIGHT/8), 
                PAGE_WIDTH, 
                PAGE_HEIGHT
            )
        )
        
        # Draw margins
        left_margin = pygame.Rect(
            (SCREEN_WIDTH/2) - 460,
            (SCREEN_HEIGHT/8),
            2,  # Width of margin line
            PAGE_HEIGHT
        )
        right_margin = pygame.Rect(
            (SCREEN_WIDTH/2) + 460,
            (SCREEN_HEIGHT/8),
            2,  # Width of margin line
            PAGE_HEIGHT
        )
        
        pygame.draw.rect(self.display_surface, 'black', left_margin)
        pygame.draw.rect(self.display_surface, 'black', right_margin)
    
    def display(self):
        # Update text surface with current input
        self.text = self.font.render(self.user_input, True, 'black', 'white')
        
        # Draw the text
        self.display_surface.blit(self.text, self.text_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Handle letters and standard characters
                if event.key < 127 and event.key > 31:
                    if event.mod & pygame.KMOD_SHIFT:  # Check for shift key
                        self.user_input += pygame.key.name(event.key).upper()
                    else:
                        self.user_input += pygame.key.name(event.key)

                # Handle backspace
                elif event.key == pygame.K_BACKSPACE and len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]

                # Handle space
                elif event.key == pygame.K_SPACE:
                    self.user_input += " "

                # Handle enter/return
                elif event.key == pygame.K_RETURN:
                    self.user_input = self.user_input.ljust(MAX_CHARACTERS)

        # Keep input within maximum character limit
        if len(self.user_input) > MAX_CHARACTERS:
            self.user_input = self.user_input[:MAX_CHARACTERS]