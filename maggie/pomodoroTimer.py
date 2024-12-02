# Class to handle the setting and changing of pomodoro phases
import pygame, datetime, time
from settings import *

class Pomodoro:
    # Constructor
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Set up the intervals
        self.initTime = 0           # Initial time
        self.nextTime = 0           # Next time to change phase
        self.workInter = 0          # Length of work intervals in minutes
        self.playInter = 0          # Length of play intervals in minutes, cannot exceed workInter
        self.numCycles = 0          # Number of cycles for session, integer
        self.numCyclesCompleted = 0 # Number of cycles completed, integer
        self.working = False         # Determines which phase the user is in, boolean

    def setup(self):
        # Make sure everything is valid
        self.getUserInput()
        
        # Set the initial time
        self.initTime = datetime.datetime.today()

        # Set the first nextTime
        timeDif = datetime.timedelta(0, 0, 0, 0, self.workInter)
        self.nextTime = self.initTime + timeDif

    def getUserInput(self):

        valid = False
        while not valid:

            # Get the user's desired time for work intervals (minutes)
            self.workInter = self.getNum("work")

            # Get the user's desired time for play intervals (minutes)
            self.playInter = self.getNum("break")

            # Are the intervals valid?
            if self.workInter > 0 and self.playInter > 0:
                # Is the play interval > work interval?
                if self.workInter < self.playInter:
                    self.printError('ratio')
                    continue
            else:
                self.printError('zero')
                continue

            # Finally, get the number of cycles the user wants to do
            self.numCycles = self.getNum("cycles")

            # Is the number of cycles reasonable
            if self.numCycles < 3 or self.numCycles > 10:
                self.printError('cycles')
            # If it is, exit the loop and continue on
            else:
                break

    # Print an error message
    def printError(self, type):
        # Make the text render
        errorFont = pygame.font.SysFont('couriernew', 30)
        
        # Is it a 0 error?
        if type == 'zero':
            s = "Please enter non-zero values"

        # Is the interval ratio incorrect?
        elif type == 'ratio':
            s = "Break intervals cannot be longer than work intervals"

        # Is it too many cycles?
        elif type == 'cycles':
            s = "We recommend between 3 - 10 cycles"

        # Make the error message
        error = errorFont.render(s, True, 'black', 'white')
        errorRect = error.get_rect()
        errorRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        self.display_surface.fill('black')
        self.display_surface.blit(error, errorRect)

    # Set the initial timer
    def startPhase(self):
        # Tell the user that the phase switched
        background = pygame.Rect(0, 0, 2*SCREEN_WIDTH // 3, SCREEN_WIDTH // 5)
        background.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        font = pygame.font.SysFont('couriernew', 40)
        message = font.render('Phase Switched!', True, 'black', 'white')
        messageRect = message.get_rect()
        messageRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)

        pygame.draw.rect(self.display_surface, 'white', background)
        pygame.draw.rect(self.display_surface, 'blue', background, 2)

        if self.working:
            s = "Time for a break!"            
        else:
            s = "Time to work!"

        message2 = font.render(s, True, 'black', 'white')
        message2Rect = message2.get_rect()
        message2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)

        self.display_surface.blit(message, messageRect)
        self.display_surface.blit(message2, message2Rect)
        pygame.display.update()

        # Delay for a bit so that the user can see the message
        time.sleep(3)

        # Get the current time from the user
        self.initTime = datetime.datetime.today()

        # Get the interval for the current time
        if self.working:
            interval = self.playInter
        else:
            interval = self.workInter

        # Switch self.working to reflect current phase
        self.working = not self.working

        # Set the next time for switch based on interval
        timeDif = datetime.timedelta(0, 0, 0, 0, interval)
        self.nextTime = self.initTime + timeDif

        # Update which number cycle the user is one
        if self.working == False:
            self.numCyclesCompleted += 1

    # Run the pomodoro timer
    def run(self):
        # If the timer phases are still going
        if self.numCyclesCompleted < self.numCycles:
            # Display the clock

            # Is the current time at the switch time
            if datetime.datetime.today() > self.nextTime:
                # If it is, switch the phase
                self.startPhase()


    def getNum(self, phase):
        phaseTime = -1

        # Set up the text surfaces
        if phase == "work" or phase == "break":
            s = "Please enter the time for the " + str(phase) + " phase: "
        else:
            s = "Please enter the number of phases you'd like to complete: "
        
        self.font = pygame.font.SysFont("couriernew", 24)
        response = ""

        while True:
            # Ask the user for the time
            screenRect = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.display_surface.fill('black', screenRect)
            request = self.font.render(s, True, 'black', 'white')

            request_rect = request.get_rect()
            request_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            self.display_surface.blit(request, request_rect)

            # Take in the user's time
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Was it a number?
                    if event.key >= 48 and event.key <= 57:
                        response += pygame.key.name(event.key)

                    # Was it a backspace
                    if event.key == 8 and response.__len__() >= 1:
                        response = response[:-1]

                    # Was it enter?
                    elif event.key == 13:
                        # Is the length non-zero?
                        if response.__len__() > 0:
                            phaseTime = int(response)
                            return phaseTime
                        
            # If the user is not done typing, update their shown input
            request = self.font.render(response, True, 'black', 'white')
            request_rect = request.get_rect()
            request_rect.center = (SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 5)
            self.display_surface.blit(request, request_rect)

            # Update the screen
            pygame.display.update()
