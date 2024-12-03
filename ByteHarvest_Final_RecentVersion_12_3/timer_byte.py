# import pygame

# class Timer:
#     def __init__(self, duration, func = None):
#         self.duration = duration
#         self.func = func
#         self.time_left = duration
#         self.active = False

#     def start(self):
#         # Start the timer
#         self.time_left = self.duration
#         self.active = True

#     def stop(self):
#         # Stop the timer
#         self.active = False
#         self.time_left = self.duration

#     def update(self, dt):
#         # Lower time left
#         if self.active:
#             self.time_left -= dt
#             if self.time_left <= 0:
#                 if self.func:
#                     self.func()
#                 self.stop()

import pygame

class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func    # Function to call when timer completes
        self.start_time = 0
        self.active = False

    def activate(self):
        """Start the timer."""
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        """Stop the timer."""
        self.active = False
        self.start_time = 0

    def update(self):
        """Update the timer and call function if duration reached."""
        current_time = pygame.time.get_ticks()
        
        if self.active and current_time - self.start_time >= self.duration:
            if self.func:
                self.func()
            self.deactivate()