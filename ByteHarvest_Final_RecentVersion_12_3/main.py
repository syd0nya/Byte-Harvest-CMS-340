# main.py
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from level1 import Level

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Byte Harvest")
        
        # Create clock for timing
        self.clock = pygame.time.Clock()

        # Create farm surface
        self.farm_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create level
        self.level = Level(self.farm_screen)

    def run(self):
        running = True
        while running:
            # Event handling
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False

            # Calculate delta time
            dt = self.clock.tick(60) / 1000  # 60 FPS

            # Update level
            self.level.run(dt, event_list)

            # Draw farm screen to main display
            self.screen.blit(self.farm_screen, (0, 0))
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    # Create and run game
    game = Game()
    game.run()
