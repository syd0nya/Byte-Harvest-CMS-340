# # import pygame
# # from pygame import Vector2
# # from constants import LAYERS,  ANIMAL_SETTINGS
# # from sprite_loader import load_spritesheet, scale_images

# # class Animal(pygame.sprite.Sprite):
# #     def __init__(self, animal_type, start_pos, groups, collision_sprites=None):
# #         """
# #         Initialize an animal sprite.
        
# #         Args:
# #             animal_type (str): Type of animal ('chicken' or 'cow')
# #             start_pos (tuple): Starting position (x, y)
# #             groups (list): Pygame sprite groups to add this sprite to
# #             collision_sprites (pygame.sprite.Group, optional): Sprites to check collisions against
# #         """
# #         super().__init__(groups)
        
# #         # Basic setup
# #         self.animal_type = animal_type
        
# #         # Load sprite frames using settings from constants
# #         self.frames = load_spritesheet(
# #             path=f'graphics/assets/{animal_type}.png',
# #             frame_width=ANIMAL_SETTINGS[animal_type]['frame_width'],
# #             frame_height=ANIMAL_SETTINGS[animal_type]['frame_height']
# #         )
        
# #         # Scale frames if needed
# #         if 'scale' in ANIMAL_SETTINGS[animal_type]:
# #             scale = ANIMAL_SETTINGS[animal_type]['scale']
# #             self.frames = scale_images(self.frames, scale)
        
# #         # Animation setup
# #         self.frame_index = 0
# #         self.status = 'idle'
# #         self.image = self.frames[self.frame_index]
# #         self.rect = self.image.get_rect(topleft=start_pos)
        
# #         # Z-indexing
# #         self.z = LAYERS['main']
        
# #         # Movement attributes
# #         self.direction = Vector2()
# #         self.pos = Vector2(start_pos)
# #         self.speed = ANIMAL_SETTINGS[animal_type]['speed']
        
# #         # Collision setup
# #         self.hitbox = self.rect.copy().inflate(-10, -10)  # Smaller hitbox than sprite
# #         self.collision_sprites = collision_sprites
        
# #         # Animation attributes
# #         self.animation_speed = ANIMAL_SETTINGS[animal_type]['animation_speed']
# #         self.facing_right = True
        
# #         # Timer for random movement (if implemented)
# #         self.move_timer = pygame.time.get_ticks()
# #         self.move_duration = 0
# #         self.is_moving = False
    
# #     def move(self, dt):
# #         """Update the animal's position based on its direction."""
# #         # Normalize direction for diagonal movement
# #         if self.direction.magnitude() > 0:
# #             self.direction = self.direction.normalize()
        
# #         # Horizontal movement
# #         self.pos.x += self.direction.x * self.speed * dt
# #         self.hitbox.centerx = round(self.pos.x)
# #         self.rect.centerx = self.hitbox.centerx
# #         if self.collision_sprites:
# #             self.collision('horizontal')

# #         # Vertical movement
# #         self.pos.y += self.direction.y * self.speed * dt
# #         self.hitbox.centery = round(self.pos.y)
# #         self.rect.centery = self.hitbox.centery
# #         if self.collision_sprites:
# #             self.collision('vertical')
            
# #         # Update facing direction
# #         if self.direction.x > 0:
# #             self.facing_right = True
# #         elif self.direction.x < 0:
# #             self.facing_right = False
            
# #     def collision(self, direction):
# #         """Handle collisions with other sprites."""
# #         for sprite in self.collision_sprites.sprites():
# #             if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
# #                 if direction == 'horizontal':
# #                     if self.direction.x > 0:  # Moving right
# #                         self.hitbox.right = sprite.hitbox.left
# #                     if self.direction.x < 0:  # Moving left
# #                         self.hitbox.left = sprite.hitbox.right
# #                     self.rect.centerx = self.hitbox.centerx
# #                     self.pos.x = self.hitbox.centerx
                
# #                 if direction == 'vertical':
# #                     if self.direction.y > 0:  # Moving down
# #                         self.hitbox.bottom = sprite.hitbox.top
# #                     if self.direction.y < 0:  # Moving up
# #                         self.hitbox.top = sprite.hitbox.bottom
# #                     self.rect.centery = self.hitbox.centery
# #                     self.pos.y = self.hitbox.centery
    
# #     def animate(self, dt):
# #         """Update the animal's animation frame."""
# #         # Update animation frame
# #         self.frame_index += self.animation_speed
        
# #         # Loop animation
# #         if self.frame_index >= len(self.frames):
# #             self.frame_index = 0
            
# #         # Update image
# #         self.image = self.frames[int(self.frame_index)]
        
# #         # Flip image if facing left
# #         if not self.facing_right:
# #             self.image = pygame.transform.flip(self.image, True, False)
    
# #     def update_status(self):
# #         """Update the animal's status based on movement."""
# #         if self.direction.magnitude() == 0:
# #             if 'idle' not in self.status:
# #                 self.status = 'idle'
# #                 self.frame_index = 0
# #         else:
# #             if 'walk' not in self.status:
# #                 self.status = 'walk'
# #                 self.frame_index = 0
    
# #     def update(self, dt):
# #         """Update the animal's state each frame."""
# #         self.move(dt)
# #         self.update_status()
# #         self.animate(dt)
# # animal.py
# import pygame
# from constants import LAYERS

# class Animal(pygame.sprite.Sprite):
#     def __init__(self, animal_type, start_pos, groups, collision_sprites=None):
#         super().__init__(groups)
        
#         # Load and create frames
#         try:
#             self.sprite_sheet = pygame.image.load(f'graphics/assets/{animal_type}.png').convert_alpha()
            
#             # Each frame is 32x32 in your sprite sheet
#             self.frames = []
#             for i in range(4):  # 4 frames per animation
#                 frame_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
#                 frame_surf.blit(self.sprite_sheet, (0, 0), (i * 32, 0, 32, 32))
#                 # Scale up the frame (make it bigger)
#                 frame_surf = pygame.transform.scale(frame_surf, (96, 96))  # 3x bigger
#                 self.frames.append(frame_surf)
                
#         except Exception as e:
#             print(f"Failed to load {animal_type} sprites: {e}")
#             surf = pygame.Surface((96, 96))
#             surf.fill('red')
#             self.frames = [surf]

#         # Animation setup
#         self.frame_index = 0
#         self.image = self.frames[self.frame_index]
#         self.rect = self.image.get_rect(topleft=start_pos)
#         self.z = LAYERS['main']
        
#         # Animation settings - slower animation for idle
#         self.animation_speed = 0.1

#     def animate(self, dt):
#         self.frame_index += self.animation_speed
#         if self.frame_index >= len(self.frames):
#             self.frame_index = 0
#         self.image = self.frames[int(self.frame_index)]

#     def update(self, dt):
#         self.animate(dt)
# animal.py
# animal.py
import pygame
from random import randint
from constants import LAYERS, TILE_SIZE

class Animal(pygame.sprite.Sprite):
    def __init__(self, animal_type, start_pos, groups, collision_sprites):
        super().__init__(groups)
        self.collision_sprites = collision_sprites
        self.animal_type = animal_type

        # Load animal image
        try:
            self.image = pygame.image.load(f'graphics/assets/{animal_type}.png').convert_alpha()
            # Optionally scale the image if necessary
            self.image = pygame.transform.scale(self.image, (64, 64))  # Scale to 64x64 pixels
        except FileNotFoundError:
            print(f"No image found for {animal_type} at 'graphics/assets/{animal_type}.png', using placeholder")
            self.image = pygame.Surface((64, 64))
            self.image.fill('yellow')

        self.rect = self.image.get_rect(topleft=start_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Set the rendering layer (z-value)
        self.z = LAYERS['main']  # Ensure animals are drawn above ground elements

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.speed = 20  # Adjust speed as needed
        self.timer = 0
        self.move_time = 2000  # Move every 2 seconds

    def update(self, dt):
        self.timer += dt * 1000  # Convert dt to milliseconds
        if self.timer >= self.move_time:
            self.timer = 0
            # Random movement direction
            self.direction.x = randint(-1, 1)
            self.direction.y = randint(-1, 1)

        # Move animal
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Handle collisions
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                self.pos -= self.direction * self.speed * dt
                self.rect.topleft = (int(self.pos.x), int(self.pos.y))
                break  # Exit the loop after collision is handled
