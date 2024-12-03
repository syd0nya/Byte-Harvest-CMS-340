# # # Class to handle the setting and changing of pomodoro phases
# # import pygame, datetime, time
# # from constants import *

# # class Pomodoro:
# #     # Constructor
# #     def __init__(self):

# #         # Get the display surface
# #         self.display_surface = pygame.display.get_surface()

# #         # Set up the intervals
# #         self.initTime = 0           # Initial time
# #         self.nextTime = 0           # Next time to change phase
# #         self.workInter = 0          # Length of work intervals in minutes
# #         self.playInter = 0          # Length of play intervals in minutes, cannot exceed workInter
# #         self.numCycles = 0          # Number of cycles for session, integer
# #         self.numCyclesCompleted = 0 # Number of cycles completed, integer
# #         self.working = False         # Determines which phase the user is in, boolean

# #     def setup(self):
# #         # Make sure everything is valid
# #         self.getUserInput()
        
# #         # Set the initial time
# #         self.initTime = datetime.datetime.today()

# #         # Set the first nextTime
# #         timeDif = datetime.timedelta(0, 0, 0, 0, self.workInter)
# #         self.nextTime = self.initTime + timeDif

# #     def getUserInput(self):

# #         valid = False
# #         while not valid:

# #             # Get the user's desired time for work intervals (minutes)
# #             self.workInter = self.getNum("work")

# #             # Get the user's desired time for play intervals (minutes)
# #             self.playInter = self.getNum("break")

# #             # Are the intervals valid?
# #             if self.workInter > 0 and self.playInter > 0:
# #                 # Is the play interval > work interval?
# #                 if self.workInter < self.playInter:
# #                     self.printError('ratio')
# #                     continue
# #             else:
# #                 self.printError('zero')
# #                 continue

# #             # Finally, get the number of cycles the user wants to do
# #             self.numCycles = self.getNum("cycles")

# #             # Is the number of cycles reasonable
# #             if self.numCycles < 3 or self.numCycles > 10:
# #                 self.printError('cycles')
# #             # If it is, exit the loop and continue on
# #             else:
# #                 break

# #     # Print an error message
# #     def printError(self, type):
# #         # Make the text render
# #         errorFont = pygame.font.SysFont('couriernew', 30)
        
# #         # Is it a 0 error?
# #         if type == 'zero':
# #             s = "Please enter non-zero values"

# #         # Is the interval ratio incorrect?
# #         elif type == 'ratio':
# #             s = "Break intervals cannot be longer than work intervals"

# #         # Is it too many cycles?
# #         elif type == 'cycles':
# #             s = "We recommend between 3 - 10 cycles"

# #         # Make the error message
# #         error = errorFont.render(s, True, 'black', 'white')
# #         errorRect = error.get_rect()
# #         errorRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

# #         self.display_surface.fill('black')
# #         self.display_surface.blit(error, errorRect)

# #     # Set the initial timer
# #     def startPhase(self):
# #         # Tell the user that the phase switched
# #         background = pygame.Rect(0, 0, 2*SCREEN_WIDTH // 3, SCREEN_WIDTH // 5)
# #         background.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# #         font = pygame.font.SysFont('couriernew', 40)
# #         message = font.render('Phase Switched!', True, 'black', 'white')
# #         messageRect = message.get_rect()
# #         messageRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)

# #         pygame.draw.rect(self.display_surface, 'white', background)
# #         pygame.draw.rect(self.display_surface, 'blue', background, 2)

# #         if self.working:
# #             s = "Time for a break!"            
# #         else:
# #             s = "Time to work!"

# #         message2 = font.render(s, True, 'black', 'white')
# #         message2Rect = message2.get_rect()
# #         message2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)

# #         self.display_surface.blit(message, messageRect)
# #         self.display_surface.blit(message2, message2Rect)
# #         pygame.display.update()

# #         # Delay for a bit so that the user can see the message
# #         time.sleep(3)

# #         # Get the current time from the user
# #         self.initTime = datetime.datetime.today()

# #         # Get the interval for the current time
# #         if self.working:
# #             interval = self.playInter
# #         else:
# #             interval = self.workInter

# #         # Switch self.working to reflect current phase
# #         self.working = not self.working

# #         # Set the next time for switch based on interval
# #         timeDif = datetime.timedelta(0, 0, 0, 0, interval)
# #         self.nextTime = self.initTime + timeDif

# #         # Update which number cycle the user is one
# #         if self.working == False:
# #             self.numCyclesCompleted += 1

# #     # Run the pomodoro timer
# #     def run(self):
# #         # If the timer phases are still going
# #         if self.numCyclesCompleted < self.numCycles:
# #             # Display the clock

# #             # Is the current time at the switch time
# #             if datetime.datetime.today() > self.nextTime:
# #                 # If it is, switch the phase
# #                 self.startPhase()


# #     def getNum(self, phase):
# #         phaseTime = -1

# #         # Set up the text surfaces
# #         if phase == "work" or phase == "break":
# #             s = "Please enter the time for the " + str(phase) + " phase: "
# #         else:
# #             s = "Please enter the number of phases you'd like to complete: "
        
# #         self.font = pygame.font.SysFont("couriernew", 24)
# #         response = ""

# #         while True:
# #             # Ask the user for the time
# #             screenRect = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
# #             self.display_surface.fill('black', screenRect)
# #             request = self.font.render(s, True, 'black', 'white')

# #             request_rect = request.get_rect()
# #             request_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# #             self.display_surface.blit(request, request_rect)

# #             # Take in the user's time
# #             for event in pygame.event.get():
# #                 if event.type == pygame.KEYDOWN:
# #                     # Was it a number?
# #                     if event.key >= 48 and event.key <= 57:
# #                         response += pygame.key.name(event.key)

# #                     # Was it a backspace
# #                     if event.key == 8 and response.__len__() >= 1:
# #                         response = response[:-1]

# #                     # Was it enter?
# #                     elif event.key == 13:
# #                         # Is the length non-zero?
# #                         if response.__len__() > 0:
# #                             phaseTime = int(response)
# #                             return phaseTime
                        
# #             # If the user is not done typing, update their shown input
# #             request = self.font.render(response, True, 'black', 'white')
# #             request_rect = request.get_rect()
# #             request_rect.center = (SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 5)
# #             self.display_surface.blit(request, request_rect)

# #             # Update the screen
# #             pygame.display.update()

# # import pygame
# # import datetime
# # import time
# # from constants import *

# # class Pomodoro:
# #     def __init__(self):
# #         # Get display surface
# #         self.display_surface = pygame.display.get_surface()
        
# #         # Time intervals
# #         self.init_time = 0           # Initial time
# #         self.next_time = 0           # Next time to change phase
# #         self.work_inter = 0          # Length of work intervals (minutes)
# #         self.play_inter = 0          # Length of play intervals (minutes)
# #         self.num_cycles = 0          # Number of cycles for session
# #         self.num_cycles_completed = 0 # Number of cycles completed
# #         self.working = False         # Current phase state

# #     def setup(self):
# #         # Get user input and validate
# #         self.get_user_input()
        
# #         # Set initial time
# #         self.init_time = datetime.datetime.today()
        
# #         # Set first interval
# #         time_diff = datetime.timedelta(0, 0, 0, 0, self.work_inter)
# #         self.next_time = self.init_time + time_diff

# #     def get_user_input(self):
# #         valid = False
# #         while not valid:
# #             # Get work interval
# #             self.work_inter = self.get_num("work")
            
# #             # Get play interval
# #             self.play_inter = self.get_num("break")
            
# #             # Validate intervals
# #             if self.work_inter > 0 and self.play_inter > 0:
# #                 if self.work_inter < self.play_inter:
# #                     self.print_error('ratio')
# #                     continue
# #             else:
# #                 self.print_error('zero')
# #                 continue
            
# #             # Get number of cycles
# #             self.num_cycles = self.get_num("cycles")
            
# #             # Validate cycles
# #             if self.num_cycles < 3 or self.num_cycles > 10:
# #                 self.print_error('cycles')
# #             else:
# #                 break

# #     def print_error(self, error_type):
# #         error_font = pygame.font.SysFont('couriernew', 30)
        
# #         if error_type == 'zero':
# #             message = "Please enter non-zero values"
# #         elif error_type == 'ratio':
# #             message = "Break intervals cannot be longer than work intervals"
# #         elif error_type == 'cycles':
# #             message = "We recommend between 3 - 10 cycles"
            
# #         error_surf = error_font.render(message, True, 'black', 'white')
# #         error_rect = error_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        
# #         self.display_surface.fill('black')
# #         self.display_surface.blit(error_surf, error_rect)

# #     def start_phase(self):
# #         # Show phase change message
# #         background = pygame.Rect(0, 0, 2*SCREEN_WIDTH // 3, SCREEN_WIDTH // 5)
# #         background.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
# #         font = pygame.font.SysFont('couriernew', 40)
# #         message = font.render('Phase Switched!', True, 'black', 'white')
# #         message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        
# #         pygame.draw.rect(self.display_surface, 'white', background)
# #         pygame.draw.rect(self.display_surface, 'blue', background, 2)
        
# #         # Show phase specific message
# #         if self.working:
# #             phase_message = "Time for a break!"
# #         else:
# #             phase_message = "Time to work!"
            
# #         phase_surf = font.render(phase_message, True, 'black', 'white')
# #         phase_rect = phase_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        
# #         self.display_surface.blit(message, message_rect)
# #         self.display_surface.blit(phase_surf, phase_rect)
# #         pygame.display.update()
        
# #         # Pause to show message
# #         time.sleep(3)
        
# #         # Update times and states
# #         self.init_time = datetime.datetime.today()
# #         interval = self.play_inter if self.working else self.work_inter
# #         self.working = not self.working
        
# #         time_diff = datetime.timedelta(0, 0, 0, 0, interval)
# #         self.next_time = self.init_time + time_diff
        
# #         if not self.working:
# #             self.num_cycles_completed += 1

# #     def run(self):
# #         # Check if timer should continue
# #         if self.num_cycles_completed < self.num_cycles:
# #             # Check for phase switch
# #             if datetime.datetime.today() > self.next_time:
# #                 self.start_phase()

# #     def get_num(self, phase):
# #         phase_time = -1
        
# #         # Set prompt message
# #         if phase == "work" or phase == "break":
# #             prompt = f"Please enter the time for the {phase} phase: "
# #         else:
# #             prompt = "Please enter the number of phases you'd like to complete: "
        
# #         self.font = pygame.font.SysFont("couriernew", 24)
# #         response = ""
        
# #         while True:
# #             # Clear input area
# #             screen_rect = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
# #             self.display_surface.fill('black', screen_rect)
            
# #             # Show prompt
# #             prompt_surf = self.font.render(prompt, True, 'black', 'white')
# #             prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
# #             self.display_surface.blit(prompt_surf, prompt_rect)
            
# #             # Handle input
# #             for event in pygame.event.get():
# #                 if event.type == pygame.KEYDOWN:
# #                     # Number keys
# #                     if event.key >= 48 and event.key <= 57:
# #                         response += pygame.key.name(event.key)
# #                     # Backspace
# #                     elif event.key == pygame.K_BACKSPACE and len(response) >= 1:
# #                         response = response[:-1]
# #                     # Enter
# #                     elif event.key == pygame.K_RETURN:
# #                         if len(response) > 0:
# #                             return int(response)
            
# #             # Show current input
# #             if response:
# #                 input_surf = self.font.render(response, True, 'black', 'white')
# #                 input_rect = input_surf.get_rect(center=(SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 5))
# #                 self.display_surface.blit(input_surf, input_rect)
            
# #             pygame.display.update()

# import pygame
# import datetime
# import time
# from constants import *

# class Pomodoro:
#     def __init__(self):
#         # Get display surface
#         self.display_surface = pygame.display.get_surface()

#         # Time intervals
#         self.init_time = None
#         self.next_time = None
#         self.work_inter = 0
#         self.play_inter = 0
#         self.num_cycles = 0
#         self.num_cycles_completed = 0
#         self.working = False

#     def setup(self):
#         # Get user input and validate
#         self.get_user_input()

#         # Set initial time
#         self.init_time = datetime.datetime.now()

#         # Set first interval
#         time_diff = datetime.timedelta(minutes=self.work_inter)
#         self.next_time = self.init_time + time_diff
#         self.working = True

#     def get_user_input(self):
#         # For now, set default values for simplicity
#         self.work_inter = 25  # Work interval in minutes
#         self.play_inter = 5   # Break interval in minutes
#         self.num_cycles = 4   # Number of cycles

#         # Validate intervals
#         if self.work_inter <= 0 or self.play_inter <= 0:
#             self.print_error('zero')
#         elif self.play_inter > self.work_inter:
#             self.print_error('ratio')
#         elif not (3 <= self.num_cycles <= 10):
#             self.print_error('cycles')

#     def print_error(self, error_type):
#         error_font = pygame.font.SysFont('couriernew', 30)

#         if error_type == 'zero':
#             message = "Please enter non-zero values"
#         elif error_type == 'ratio':
#             message = "Break intervals cannot be longer than work intervals"
#         elif error_type == 'cycles':
#             message = "We recommend between 3 - 10 cycles"

#         error_surf = error_font.render(message, True, 'black', 'white')
#         error_rect = error_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

#         self.display_surface.fill('black')
#         self.display_surface.blit(error_surf, error_rect)
#         pygame.display.update()

#     def start_phase(self):
#         # Show phase change message
#         background = pygame.Rect(0, 0, 2*SCREEN_WIDTH // 3, SCREEN_WIDTH // 5)
#         background.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

#         font = pygame.font.SysFont('couriernew', 40)
#         message = font.render('Phase Switched!', True, 'black', 'white')
#         message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))

#         pygame.draw.rect(self.display_surface, 'white', background)
#         pygame.draw.rect(self.display_surface, 'blue', background, 2)

#         # Show phase specific message
#         if self.working:
#             phase_message = "Time for a break!"
#         else:
#             phase_message = "Time to work!"

#         phase_surf = font.render(phase_message, True, 'black', 'white')
#         phase_rect = phase_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

#         self.display_surface.blit(message, message_rect)
#         self.display_surface.blit(phase_surf, phase_rect)
#         pygame.display.update()

#         # Pause to show message
#         time.sleep(3)

#         # Update times and states
#         self.init_time = datetime.datetime.now()
#         interval = self.play_inter if self.working else self.work_inter
#         self.working = not self.working

#         time_diff = datetime.timedelta(minutes=interval)
#         self.next_time = self.init_time + time_diff

#         if not self.working:
#             self.num_cycles_completed += 1

#     def run(self):
#         # Check if timer should continue
#         if self.num_cycles_completed < self.num_cycles:
#             # Check for phase switch
#             if datetime.datetime.now() >= self.next_time:
#                 self.start_phase()
#         else:
#             # Timer completed
#             self.timer_active = False
#             # You might want to display a message or reset

#     def get_remaining_time(self):
#         now = datetime.datetime.now()
#         remaining = self.next_time - now
#         if remaining.total_seconds() < 0:
#             remaining = datetime.timedelta(seconds=0)
#         return remaining

# pomodoroTimer.py

# pomodoroTimer.py
import pygame
import datetime
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Pomodoro:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        # Time intervals
        self.init_time = None
        self.next_time = None
        self.work_inter = ''
        self.play_inter = ''
        self.num_cycles = ''
        self.num_cycles_completed = 0
        self.working = False

        # Input handling
        self.collecting_input = True
        self.input_stage = 0  # 0: work_inter, 1: play_inter, 2: num_cycles
        self.current_input = ''
        self.error_message = ''
        self.font = pygame.font.SysFont('couriernew', 24)
        self.timer_active = False

    def setup(self):
        # Initialize input variables
        self.work_inter = ''
        self.play_inter = ''
        self.num_cycles = ''
        self.num_cycles_completed = 0
        self.working = False

        # Set input flags
        self.collecting_input = True
        self.input_stage = 0
        self.current_input = ''
        self.error_message = ''
        self.timer_active = True

    def get_user_input(self, event_list):
        # Handle input events
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # User pressed Enter, move to next input stage
                    if self.current_input != '':
                        if self.input_stage == 0:
                            self.work_inter = self.current_input
                            self.current_input = ''
                            self.input_stage = 1
                        elif self.input_stage == 1:
                            self.play_inter = self.current_input
                            self.current_input = ''
                            self.input_stage = 2
                        elif self.input_stage == 2:
                            self.num_cycles = self.current_input
                            self.current_input = ''
                            self.input_stage = 3  # Move to validation
                            self.validate_inputs()
                    else:
                        # No input entered
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    self.current_input = self.current_input[:-1]
                else:
                    # Append character if it's a number
                    if event.unicode.isdigit():
                        self.current_input += event.unicode

    def validate_inputs(self):
        # Convert inputs to integers
        try:
            self.work_inter = int(self.work_inter)
            self.play_inter = int(self.play_inter)
            self.num_cycles = int(self.num_cycles)
        except ValueError:
            self.error_message = 'Please enter valid numbers.'
            self.reset_input()
            return

        # Validate intervals
        if self.work_inter <= 0 or self.play_inter <= 0:
            self.error_message = 'Intervals must be greater than zero.'
            self.reset_input()
        elif self.play_inter > self.work_inter:
            self.error_message = 'Break cannot be longer than work interval.'
            self.reset_input()
        elif not (1 <= self.num_cycles <= 10):
            self.error_message = 'Cycles must be between 1 and 10.'
            self.reset_input()
        else:
            # Inputs are valid, start timer
            self.init_time = datetime.datetime.now()
            time_diff = datetime.timedelta(minutes=self.work_inter)
            self.next_time = self.init_time + time_diff
            self.working = True
            self.collecting_input = False
            self.error_message = ''

    def reset_input(self):
        # Reset input for re-entry
        self.input_stage = 0
        self.current_input = ''
        self.work_inter = ''
        self.play_inter = ''
        self.num_cycles = ''

    def display_input(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black (alpha = 128)
        self.display_surface.blit(overlay, (0, 0))

        # Draw input prompt box
        background_rect = pygame.Rect(0, 0, SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.3)
        background_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.display_surface, 'black', background_rect)
        pygame.draw.rect(self.display_surface, 'white', background_rect, 2)

        prompt = ''
        if self.input_stage == 0:
            prompt = 'Enter work interval in minutes:'
        elif self.input_stage == 1:
            prompt = 'Enter break interval in minutes:'
        elif self.input_stage == 2:
            prompt = 'Enter number of cycles:'

        # Render prompt
        prompt_surf = self.font.render(prompt, True, 'white')
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.display_surface.blit(prompt_surf, prompt_rect)

        # Render current input
        input_surf = self.font.render(self.current_input, True, 'white')
        input_rect = input_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display_surface.blit(input_surf, input_rect)

        # Render error message if any
        if self.error_message != '':
            error_surf = self.font.render(self.error_message, True, 'red')
            error_rect = error_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.display_surface.blit(error_surf, error_rect)

    def start_phase(self):
        # Show phase change message
        background = pygame.Rect(0, 0, 2 * SCREEN_WIDTH // 3, SCREEN_WIDTH // 5)
        background.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        font = pygame.font.SysFont('couriernew', 40)
        message = font.render('Phase Switched!', True, 'black', 'white')
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))

        pygame.draw.rect(self.display_surface, 'white', background)
        pygame.draw.rect(self.display_surface, 'blue', background, 2)

        # Show phase specific message
        if self.working:
            phase_message = "Time for a break!"
        else:
            phase_message = "Time to work!"

        phase_surf = font.render(phase_message, True, 'black', 'white')
        phase_rect = phase_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

        self.display_surface.blit(message, message_rect)
        self.display_surface.blit(phase_surf, phase_rect)

        # Pause to show message
        pygame.display.update()
        pygame.time.delay(2000)

        # Update times and states
        self.init_time = datetime.datetime.now()
        interval = self.play_inter if self.working else self.work_inter
        self.working = not self.working

        time_diff = datetime.timedelta(minutes=interval)
        self.next_time = self.init_time + time_diff

        if not self.working:
            self.num_cycles_completed += 1

    def run(self, event_list):
        if self.collecting_input:
            self.get_user_input(event_list)
            self.display_input()
        else:
            # Check if timer should continue
            if self.num_cycles_completed < self.num_cycles:
                # Check for phase switch
                if datetime.datetime.now() >= self.next_time:
                    self.start_phase()
                # Display timer (remaining time)
                self.display_timer()
            else:
                # Timer completed
                self.timer_active = False
                # Display completion message
                self.display_completion_message()

    def get_remaining_time(self):
        now = datetime.datetime.now()
        remaining = self.next_time - now
        if remaining.total_seconds() < 0:
            remaining = datetime.timedelta(seconds=0)
        return remaining

    def display_timer(self):
        # Display remaining time
        font = pygame.font.SysFont('couriernew', 48)
        remaining_time = self.get_remaining_time()
        minutes, seconds = divmod(int(remaining_time.total_seconds()), 60)

        if self.working:
            text = f"Work Time: {minutes}m {seconds}s"
            color = (255, 100, 100)  # Red for work
        else:
            text = f"Break Time: {minutes}m {seconds}s"
            color = (100, 255, 100)  # Green for break

        timer_surf = font.render(text, True, color)
        timer_rect = timer_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.display_surface.blit(timer_surf, timer_rect)

    def display_completion_message(self):
        completion_font = pygame.font.SysFont('couriernew', 48)
        completion_surf = completion_font.render('Pomodoro session completed!', True, 'white')
        completion_rect = completion_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display_surface.blit(completion_surf, completion_rect)
