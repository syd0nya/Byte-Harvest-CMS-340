import pygame, pygame.draw
from settings import *
import keyboard
import string

# Class to store user inputed text
class Editor:

    # No args constructor
    def __init__(self):
        # Display surface to draw onto
        self.display_surface = pygame.display.get_surface()

        # Initialize pygame's built-in font module to make a font object
        pygame.font.init()
        self.font = pygame.font.SysFont('arial.ttf', 32) # Default pygame font

        # Render initial text
        self.text = self.font.render('', True, 'black', 'white') # Gray text on white background

        # Set the text to appear in the center of the page
        self.textRect = self.text.get_rect()
        self.textRect.center = (SCREEN_WIDTH/2 - 360, SCREEN_HEIGHT/5)

        self.pageOffset = 0

        # User input
        self.userInput = ""

    def run(self):        

        # Make a white rectangle for the actual page
        pygame.draw.rect(self.display_surface, 'white', pygame.Rect((SCREEN_WIDTH/2)-(PAGE_WIDTH/2), 
                                                                    (SCREEN_HEIGHT/8) + self.pageOffset, 
                                                                    PAGE_WIDTH, PAGE_HEIGHT))
        
        event_list = pygame.event.get()
        self.handle_events(event_list)

        self.display()
    
    def display(self):
        # Reprint the text
        self.text = self.font.render(self.userInput, True, 'black', 'white')

        # Update the editor
        self.display_surface.blit(self.text, self.textRect)


    def handle_events(self, events):
        # If any event happens, check for user input
        shift = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Is it a letter or space
                if event.key < 127 and event.key > 33:
                    # Is it an uppercase letter
                    if event.mod == 1:
                        self.userInput += pygame.key.name(event.key).upper()
                    else:
                        self.userInput += pygame.key.name(event.key)

                # Is it a backspace
                elif (event.key == 8) and (self.userInput.__len__() > 0):
                    # Get string without the last character
                    s = self.userInput[:-1]

                    # Reassign userInput
                    self.userInput = s

                # Is it a space
                elif event.key == 32:
                    self.userInput += " "
                    

                