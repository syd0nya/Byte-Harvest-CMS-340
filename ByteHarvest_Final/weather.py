import pygame
from pygame import Vector2
import math
from support import *
from sprites import Terrain
from random import randint, choice, uniform
from constants import *


class Snowflake(Terrain):
    def __init__(self, surf, pos, moving, groups, z):
        
        # general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(600, 800)
        self.start_time = pygame.time.get_ticks()
    
        
        self.moving = moving
        if self.moving:
            self.pos = Vector2(self.rect.topleft)
            self.direction = Vector2(uniform(-0.5, 0.5), 1.5)
            
            # Speed based on size
            flake_size = self.image.get_width()
            if flake_size <= 3:
                self.speed = randint(40, 60)
            elif flake_size <= 6:
                self.speed = randint(30, 45)
            else:
                self.speed = randint(20, 35)
                
            self.drift_timer = 0
            self.drift_change = randint(600, 1000)
            
    def update(self, dt):
        if self.moving:
            self.drift_timer += dt * 1000
            if self.drift_timer >= self.drift_change:
                self.direction.x = uniform(-0.5, 0.5)
                self.drift_timer = 0
                
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
            
            if self.rect.top > 2000:  # Using larger value for game world size
                self.kill()
                
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Snow:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.floor_w, self.floor_h = pygame.image.load('graphics/world/ground.png').get_size()
        
        # Create snow surfaces
        self.snow_flakes = {
            'small': self.create_snow_surfaces(3, 70),
            'medium': self.create_snow_surfaces(6, 25),
            'crystal': self.create_snow_surfaces(12, 5)
        }
        
        # Create ground effect surfaces
        self.snow_ground = self.create_ground_effects()
        
        self.spawn_timer = 0
        self.spawn_interval = 20
        self.max_snowflakes = 150
        self.ground_spawn_timer = 0
        self.ground_spawn_interval = 40  # Less frequent than falling snow
        
    def create_snow_surfaces(self, size, quantity):
        surfaces = []
        for _ in range(quantity):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            
            if size <= 3:  # small flakes
                pygame.draw.circle(surf, (255, 255, 255, 200), (size/2, size/2), size/2)
            elif size <= 6:  # medium flakes
                pygame.draw.circle(surf, (255, 255, 255, 220), (size/2, size/2), size/3)
                pygame.draw.line(surf, (255, 255, 255, 220), (size/2, 0), (size/2, size), 1)
                pygame.draw.line(surf, (255, 255, 255, 220), (0, size/2), (size, size/2), 1)
            else:  # crystal flakes
                center = size // 2
                for angle in range(0, 360, 60):
                    rad = angle * 3.14159 / 180
                    end_x = center + int(center * 0.8 * math.cos(rad))
                    end_y = center + int(center * 0.8 * math.sin(rad))
                    pygame.draw.line(surf, (255, 255, 255, 230), 
                                   (center, center), (end_x, end_y), 1)
            surfaces.append(surf)
        return surfaces

    def create_ground_effects(self):
        surfaces = []
        sizes = [(8, 8), (10, 10), (12, 12)]
        
        for width, height in sizes:
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            # Create small patches of accumulated snow
            pygame.draw.ellipse(surf, (255, 255, 255, 160), (0, height/4, width, height/2))
            surfaces.append(surf)
        return surfaces

    def create_snowflake(self):
        if len([sprite for sprite in self.all_sprites if isinstance(sprite, Snowflake)]) < self.max_snowflakes:
            flake_type = choice(['small'] * 70 + ['medium'] * 25 + ['crystal'] * 5)
            
            Snowflake(
                surf=choice(self.snow_flakes[flake_type]),
                pos=(randint(-20, self.floor_w + 20), -10),
                moving=True,
                groups=self.all_sprites,
                z=LAYERS['snow falling']
            )

    def create_ground_snow(self):
        Snowflake(
            surf=choice(self.snow_ground),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['snow ground']
        )
    
    def update(self):
        # Update falling snow
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.create_snowflake()
            self.spawn_timer = 0
            
        # Update ground effects
        self.ground_spawn_timer += 1
        if self.ground_spawn_timer >= self.ground_spawn_interval:
            self.create_ground_snow()
            self.ground_spawn_timer = 0