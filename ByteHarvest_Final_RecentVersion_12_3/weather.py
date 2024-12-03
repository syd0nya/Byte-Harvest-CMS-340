# weather.py

import pygame
from pygame import Vector2
import math
from random import randint, choice, uniform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LAYERS

class Snow:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.display_surface = self.all_sprites.display_surface

        # Load the ground image to get floor dimensions
        ground_image = pygame.image.load('graphics/world/ground.png').convert_alpha()
        self.floor_w, self.floor_h = ground_image.get_size()

        # Initialize timers and intervals
        self.spawn_timer = 0
        self.spawn_interval = 10  # Lower value for more frequent spawning
        self.max_snowflakes = 200  # Adjust for performance if necessary
        self.ground_spawn_timer = 0
        self.ground_spawn_interval = 100  # Less frequent than falling snow

        # Create snowflake surfaces
        self.snow_surfaces = {
            'small': self.create_snow_surfaces(8, 70),
            'medium': self.create_snow_surfaces(12, 25),
            'large': self.create_snow_surfaces(16, 5)
        }

        # Create ground effect surfaces
        self.ground_surfaces = self.create_ground_surfaces()

    def create_snow_surfaces(self, size, quantity):
        surfaces = []
        for _ in range(quantity):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 255, 200), (size / 2, size / 2), size / 2)
            surfaces.append(surf)
        return surfaces

    def create_ground_surfaces(self):
        surfaces = []
        sizes = [(8, 8), (10, 10), (12, 12)]

        for width, height in sizes:
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            # Create small patches of accumulated snow
            pygame.draw.ellipse(
                surf, (255, 255, 255, 160),
                (0, height / 4, width, height / 2)
            )
            surfaces.append(surf)
        return surfaces

    def create_snowflake(self):
        """Create a new snowflake if under the maximum limit."""
        current_snowflakes = [
            sprite for sprite in self.all_sprites if isinstance(sprite, Snowflake)
        ]
        if len(current_snowflakes) < self.max_snowflakes:
            # Choose snowflake type with weighted probability
            flake_type = choice(['small'] * 70 + ['medium'] * 25 + ['large'] * 5)

            # Create new snowflake
            Snowflake(
                surf=choice(self.snow_surfaces[flake_type]),
                pos=(randint(0, self.floor_w), -10),
                moving=True,
                groups=self.all_sprites,
                z=LAYERS['snow falling'],
                floor_h=self.floor_h
            )

    def create_ground_snow(self):
        """Create snow effect on the ground."""
        Snowflake(
            surf=choice(self.ground_surfaces),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['snow ground'],
            floor_h=self.floor_h
        )

    def update(self, dt):
        # Update falling snow
        self.spawn_timer += dt * 1000  # Convert dt to milliseconds
        if self.spawn_timer >= self.spawn_interval:
            self.create_snowflake()
            self.spawn_timer = 0

        # Update ground effects
        self.ground_spawn_timer += dt * 1000
        if self.ground_spawn_timer >= self.ground_spawn_interval:
            self.create_ground_snow()
            self.ground_spawn_timer = 0

class Snowflake(pygame.sprite.Sprite):
    def __init__(self, surf, pos, moving, groups, z, floor_h):
        super().__init__(groups)

        # Basic setup
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.floor_h = floor_h  # Store floor height

        # Movement and lifetime
        self.lifetime = randint(6000, 8000)  # Lifetime in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.moving = moving

        if self.moving:
            self.pos = Vector2(self.rect.topleft)
            self.direction = Vector2(uniform(-0.2, 0.2), 1)  # Reduced x drift for vertical fall

            # Speed based on size
            flake_size = self.image.get_width()
            if flake_size <= 8:
                self.speed = randint(30, 40)      # Adjusted speed
            elif flake_size <= 12:
                self.speed = randint(20, 30)
            else:
                self.speed = randint(15, 25)

            # Drift settings
            self.drift_timer = 0
            self.drift_change = randint(1000, 2000)

    def update(self, dt):
        if self.moving:
            # Update drift
            self.drift_timer += dt * 1000
            if self.drift_timer >= self.drift_change:
                self.direction.x = uniform(-0.2, 0.2)
                self.drift_timer = 0

            # Update position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

            # Kill if off screen (below the floor)
            if self.rect.top > self.floor_h:
                self.kill()

        # Check lifetime
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
