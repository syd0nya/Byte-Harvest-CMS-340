# import pygame
# from random import randint, choice
# from constants import *

# # class Terrain(pygame.sprite.Sprite):
# #     def __init__(self, start_pos, texture, group_list, depth=LAYERS['main']):
# #         super().__init__(group_list)
# #         self.image = texture
# #         self.rect = self.image.get_rect(topleft=start_pos)
# #         self.depth = depth
        
# #         # find the collision boundaries 
# #         shrink_x = self.rect.width * 0.2
# #         shrink_y = self.rect.height * 0.75
# #         self.bounds = self.rect.copy().inflate(-shrink_x, -shrink_y)
        
# # class WaterTile(Terrain):
# #     def __init__(self, start_pos, sprite_sequence, group_list):
# #         # Set up animation sequence
# #         self.sprites = sprite_sequence
# #         self.anim_index = 0
        
# #         # initialize the sprite within the first frame 
# #         super().__init__(
# #             start_pos=start_pos,
# #             texture=self.sprites[self.anim_index],
# #             group_list=group_list,
# #             depth=LAYERS['water']
# #         )

# # class WildFlower(Terrain):
# #     def __init__(self, start_pos, sprite_sequence, group_list):
# #         # Set up animation sequence
# #         self.sprites = sprite_sequence
# #         self.anim_index = 0

# #         #  initialize the sprite within the first frame
# #         super().__init__(
# #             start_pos=start_pos, 
# #             texture=self.sprites[self.anim_index],
# #               group_list=group_list
# #         )

# #         self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

# #     def update(self, dt):
# #         #animate by going through sequence
# #         self.anim_index += 3 * dt
# #         if self.anim_index >= len(self.sprites):
# #             self.anim_index = 0
# #         self.image = self.sprites[int(self.anim_index)]


# # class Tree(Terrain):
# #     def __init__(self, start_pos, texture, group_list, player_inventory):
# #         super().__init__(start_pos, texture, group_list)
# #         self.health = 5
# #         self.alive = True
# #         self.stump_texture = pygame.image.load('graphics/stumps/large.png').convert_alpha()
# #         self.fruit_texture = pygame.image.load('graphics/fruit/apple.png').convert_alpha()
# #         self.fruit_positions = [(10, -30), (-20, -40), (15, -50)] 
# #         self.fruits = pygame.sprite.Group()
# #         self.player_inventory = player_inventory

# #         # Generate fruits
# #         self.create_fruits()

# #         # Axe sound
# #         self.axe_sound = pygame.mixer.Sound('graphics/axe.mp3')

# #     def create_fruits(self):
       
# #         for pos in self.fruit_positions:
# #             if randint(0, 10) < 5: 
# #                 fruit = pygame.sprite.Sprite(self.fruits)
# #                 fruit.image = self.fruit_texture
# #                 fruit.rect = fruit.image.get_rect(
# #                     topleft=(self.rect.x + pos[0], self.rect.y + pos[1])
# #                 )

# #     def take_damage(self):
       
# #         if self.alive:
# #             self.health -= 1
# #             self.axe_sound.play()

# #             # Drop a fruit if available
# #             if len(self.fruits) > 0:
# #                 random_fruit = choice(self.fruits.sprites())
# #                 random_fruit.kill()  
# #                 self.player_inventory.append("apple")  

# #             # Check if tree is dead
# #             if self.health <= 0:
# #                 self.alive = False
# #                 self.image = self.stump_texture
# #                 self.rect = self.image.get_rect(topleft=self.rect.topleft)
# #                 self.player_inventory.append("wood")  

# #     def update(self, *args):
# #         if self.alive:
# #             self.fruits.update(*args)


# # class Particle(Terrain):
# #     def __init__(self, start_pos, sprite_sequence, group_list, index, duration = 200):
# #         # Set up animation sequence
# #         self.sprites = sprite_sequence
# #         self.anim_index = 0
# #         self.duration = duration
# #         self.start_time = pygame.time.get_ticks()

# #          #  initialize the sprite within the first frame
# #         super().__init__(
# #              start_pos=start_pos,
# #             texture=self.sprites[self.anim_index],
# #             group_list=group_list,
# #             depth=index
# #          )
# #     def update(self, dt):
# #         # animate particle
# #         self.anim_index += 3 * dt
# #         if self.anim_index >= len(self.sprites):
# #             self.anim_index = 0
# #         self.image = self.sprites[int(self.anim_index)]

# #         # Handle expiration
# #         if pygame.time.get_ticks() - self.start_time > self.duration:
# #             self.kill()  

# # class Interaction (Terrain):
# #     def __init__(self, start_pos, size, group_list, name):
# #         # Create a surface
# #         self.image = pygame.Surface(size)
# #         super().__init__(group_list)

# #         # Select sprite position
# #         self.rectt = self.image.get_rect(topleft=start_pos)
# #         self.name = name

# import pygame
# from constants import LAYERS, TILE_SIZE
# from random import randint, choice
# from support import import_folder

# class Terrain(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups, z=LAYERS['main']):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)
#         self.z = z
        
#         # Find collision boundaries 
#         shrink_x = self.rect.width * 0.2
#         shrink_y = self.rect.height * 0.75
#         self.hitbox = self.rect.copy().inflate(-shrink_x, -shrink_y)

# class WaterTile(pygame.sprite.Sprite):
#     def __init__(self, pos, frames, groups):
#         super().__init__(groups)
#         self.frames = frames
#         self.frame_index = 0
        
#         self.image = self.frames[self.frame_index]
#         self.rect = self.image.get_rect(topleft=pos)
#         self.z = LAYERS['water']

#     def animate(self, dt):
#         self.frame_index += 5 * dt
#         if self.frame_index >= len(self.frames):
#             self.frame_index = 0
#         self.image = self.frames[int(self.frame_index)]

#     def update(self, dt):
#         self.animate(dt)

# class WildFlower(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)
#         self.z = LAYERS['main']
#         self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

# class Tree(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups, name, player_add):
#         super().__init__(groups)
        
#         # Tree setup
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)
#         self.z = LAYERS['main']
#         self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.75)
        
#         # Tree attributes
#         self.name = name
#         self.health = 5
#         self.alive = True
#         self.player_add = player_add

#         # Apples
#         self.apple_surf = pygame.image.load('graphics/fruit/apple.png')
#         self.apple_pos = APPLE_POS[name]
#         self.apple_sprites = pygame.sprite.Group()
#         self.create_fruit()

#         # Sounds
#         self.axe_sound = pygame.mixer.Sound('graphics/axe.mp3')

#     def damage(self):
#         # Damage the tree
#         self.health -= 1

#         # Play sound
#         self.axe_sound.play()

#         # Remove an apple
#         if len(self.apple_sprites.sprites()) > 0:
#             random_apple = choice(self.apple_sprites.sprites())
#             Particle(
#                 pos=random_apple.rect.topleft,
#                 surf=random_apple.image,
#                 groups=self.groups()[0],
#                 z=LAYERS['fruit']
#             )
#             self.player_add('apple')
#             random_apple.kill()

#     def check_death(self):
#         if self.health <= 0:
#             Particle(
#                 pos=self.rect.topleft,
#                 surf=self.image,
#                 groups=self.groups()[0],
#                 z=LAYERS['fruit'],
#                 duration=300
#             )
#             self.image = pygame.image.load('graphics/stumps/small.png').convert_alpha()
#             self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
#             self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
#             self.alive = False
#             self.player_add('wood')

#     def create_fruit(self):
#         for pos in self.apple_pos:
#             if randint(0, 10) < 2:
#                 x = pos[0] + self.rect.left
#                 y = pos[1] + self.rect.top
#                 Fruit(
#                     pos=(x, y),
#                     surf=self.apple_surf,
#                     groups=[self.apple_sprites, self.groups()[0]],
#                     z=LAYERS['fruit']
#                 )

#     def update(self, dt):
#         if self.alive:
#             self.check_death()

# class Particle(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups, z, duration=200):
#         super().__init__(groups)
#         self.z = z
        
#         # Basic setup
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)
        
#         # Animation
#         self.start_time = pygame.time.get_ticks()
#         self.duration = duration

#         # White surface for fade effect
#         mask_surf = pygame.mask.from_surface(self.image)
#         new_surf = mask_surf.to_surface()
#         new_surf.set_colorkey((0, 0, 0))
#         self.image = new_surf

#     def update(self, dt):
#         current_time = pygame.time.get_ticks()
#         if current_time - self.start_time > self.duration:
#             self.kill()

# class Fruit(pygame.sprite.Sprite):
#     def __init__(self, pos, surf, groups, z):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_rect(topleft=pos)
#         self.z = z

# class Interaction(pygame.sprite.Sprite):
#     def __init__(self, pos, size, groups, name):
#         super().__init__(groups)
#         self.image = pygame.Surface(size)
#         self.rect = self.image.get_rect(topleft=pos)
#         self.name = name

import pygame
from constants import LAYERS, TILE_SIZE, APPLE_POS
from random import randint, choice
from sprite_loader import import_folder

class Terrain(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

        # Collision boundaries
        shrink_x = self.rect.width * 0.2
        shrink_y = self.rect.height * 0.75
        self.hitbox = self.rect.copy().inflate(-shrink_x, -shrink_y)

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['water']

    def update(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

class WildFlower(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(groups)

        # Tree setup
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.75)

        # Tree attributes
        self.name = name
        self.health = 5
        self.alive = True
        self.player_add = player_add  # Reference to player_add function for inventory management

        # Apples
        self.apple_surf = pygame.image.load('graphics/fruit/apple.png').convert_alpha()
        self.apple_pos = APPLE_POS.get(name, [])  # Get apple positions for this tree type
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        # Sounds
        self.axe_sound = pygame.mixer.Sound('graphics/axe.mp3')

    def create_fruit(self):
        """Create apples on the tree at predefined positions."""
        if self.alive:
            for pos in self.apple_pos:
                apple_x = self.rect.left + pos[0]
                apple_y = self.rect.top + pos[1]
                Apple(
                    pos=(apple_x, apple_y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites],
                    player_add=self.player_add
                )

    def damage(self):
        """Damage the tree, and remove it if health is depleted."""
        self.health -= 1
        self.axe_sound.play()

        if self.health <= 0:
            self.alive = False
            self.kill()  # Remove the tree from all sprite groups
            for apple in self.apple_sprites:
                apple.kill()  # Remove all apples when the tree is destroyed


class Apple(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, player_add):
        super().__init__(groups)

        # Apple setup
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['fruit']
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)

        # Reference to player's inventory management
        self.player_add = player_add

    def collect(self):
        """Handle apple collection by the player."""
        if self.player_add:
            self.player_add("apple")  # Add to player's inventory
        self.kill()  # Remove the apple sprite
        
        
class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z, duration=200):
        super().__init__(groups)
        self.z = z

        # Basic setup
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        # Animation
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # Fade effect
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Interaction(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, name):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.name = name


class SoilWaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']  # Ensure correct rendering layer