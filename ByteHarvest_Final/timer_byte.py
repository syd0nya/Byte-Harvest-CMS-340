import pygame

class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.time_left = duration
        self.active = False

    def start(self):
        # Start the timer
        self.time_left = self.duration
        self.active = True

    def stop(self):
        # Stop the timer
        self.active = False
        self.time_left = self.duration

    def update(self, dt):
        # Lower time left
        if self.active:
            self.time_left -= dt
            if self.time_left <= 0:
                if self.func:
                    self.func()
                self.stop()