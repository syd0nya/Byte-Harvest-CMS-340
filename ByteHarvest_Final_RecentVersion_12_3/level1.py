# # # # Class to run all of the game aspects
# # # # Imports
# # # import pygame 
# # # from constants import *
# # # from player import Player
# # # from overlay import Overlay
# # # from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
# # # from pytmx.util_pygame import load_pygame
# # # from support import *
# # # from transition1 import Transition
# # # from SoilLayer import SoilLayer
# # # from weather import Rain, Sky
# # # from random import randint
# # # from menu1 import Menu
# # # from cameraGroup import CameraGroup

# # # class Level:
# # #     def __init__(self, farmScreen):
# # #         # Constructor
# # #         # Set up the farm surface on which everything will be drawn
# # #         self.farmScreen = farmScreen

# # #         # Make sprite groups for player call later
# # #         self.all_sprites = CameraGroup(self.farmScreen) # All sprites that move according to the camera
# # #         self.collision_sprites = pygame.sprite.Group() # Have collisions
# # #         self.tree_sprites = pygame.sprite.Group() # Trees
# # #         self.interactive_sprites = pygame.sprite.Group() # Interactable

# # #         # Make the soil layer
# # #         self.soilLayer = SoilLayer(self.all_sprites, self.collision_sprites)

# # #         # Determine if it's going to rain (stored in the SoilLayer class)
# # #         self.soilLayer.raining = randint(0,10) <= 3 # 30% chance

# # #         # Call setup() so that we can make the overlay and menu
# # #         self.setup()

# # #         # Make the overlay
# # #         self.overlay = Overlay(self.player)

# # #         # Make the transition
# # #         self.transition = Transition(self.reset, self.player)

# # #         # Make the sky
# # #         self.sky = Sky()
# # #         self.rain = Rain(self.all_sprites)

# # #         # Make the menu
# # #         self.menu = Menu(self.player, self.toggle_shop, self.farmScreen)
# # #         self.menu_active = False # Make sure the menu isn't immediately active

# # #         # Import the music and set music settings
# # #         pygame.mixer.music.load('graphics/score.mp3')
# # #         pygame.mixer.music.play(-1) # Infinite loops
# # #         pygame.mixer.music.set_volume(0.0)

# # #     def setup(self):
# # #         # General set up
# # #         # Upload map and other sprites
# # #         sprite_data = load_pygame('data/map.tmx')

# # #         # Import house layers 
# # #         for layer in ['HouseFloor', 'HouseFurnitureBottom']:
# # #             for x, y, surf in sprite_data.get_layer_by_name(layer).tiles():
# # #                 Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

# # #         for layer in ['HouseWalls', 'HouseFurnitureTop']:
# # #             for x, y, surf in sprite_data.get_layer_by_name(layer).tiles():
# # #                 Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

# # # 		# Import fence
# # #         for x, y, surf in sprite_data.get_layer_by_name('Fence').tiles():
# # #             Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

# # #         # Import water
# # #         lake_frames = import_folder('../graphics/water')
# # #         for x, y, surf in sprite_data.get_layer_by_name('Water').tiles(): #MAGGIE See if you can remove surf
# # #             Water((x*TILE_SIZE, y*TILE_SIZE), lake_frames, self.all_sprites)

# # #         # Import Trees
# # #         for tree in sprite_data.get_layer_by_name('Trees'):
# # #             Tree((tree.x, tree.y), tree.image, [self.all_sprites, self.collision_sprites, self.tree_sprites],
# # #                  tree.name, self.player_add)

# # #         # Import Wildflowers
# # #         for flower in sprite_data.get_layer_by_name('Decoration'):
# # #             WildFlower((flower.x, flower.y), flower.image, [self.all_sprites, self.collision_sprites])

# # #         # Import collision tiles (stored as csv)
# # #         for x, y, surf in sprite_data.get_layer_by_name('Collision').tiles():
# # #             Generic((x*TILE_SIZE, y*TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), [self.collision_sprites]) # Layer the same as default so not included

# # #         # tmx file stores player, shop, and bed in Player group
# # #         for obj in sprite_data.get_layer_by_name('Player'):
# # #             # Get the player
# # #             if obj.name == 'Start':
# # #                 self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites,
# # #                                      self.tree_sprites, self.interactive_sprites, self.soilLayer, self.toggle_shop)
                
# # #             # Get the shop as an interactive sprite
# # #             elif obj.name == 'Trader':
# # #                 Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactive_sprites,
# # #                             obj.name)
                
# # #             # Get the bed as an interactive sprite (only one left in player group)
# # #             else:
# # #                 Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactive_sprites,
# # #                             obj.name)
                
# # #         # Import ground
# # #         Generic((0,0), pygame.image.load('graphics/world/ground.png').convert_alpha(), self.all_sprites, LAYERS['ground'])

# # #     def player_add(self, item):
# # #         # Add item to player's inventory
# # #         self.player.item_inventory[item] += 1

# # #     def toggle_shop(self):
# # #         # Toggle whether the shop screen is active or not
# # #         self.menu_active = not self.menu_active

# # #     def reset(self):
# # #         # Reset the entire level, to be used in transition
# # #         # Update all plants to current grow stages
# # #         self.soilLayer.update_plants()

# # #         # Determine if it will rain for the next day
# # #         self.soilLayer.raining = randint(0,10) <= 3
# # #         if self.soilLayer.raining:
# # #             # If it does, auto water the plants
# # #             self.soilLayer.water_all
# # #         else:
# # #             # If it doesn't, unwater all the plants
# # #             self.soilLayer.remove_water

# # #         # Delete and remake apples on trees to randomize positions
# # #         for tree in self.tree_sprites:
# # #             for apple in tree.apple_sprites:
# # #                 apple.kill()
# # #             tree.create_fruit
        
# # #         # Reset the sky color to max
# # #         self.sky.start_color = [255, 255, 255]

# # #     def plant_collision(self):
# # #         # Check if any of the plants are being harvested by the player
# # #         # For any existing plants
# # #         for plant in self.soilLayer.plant_sprites:
# # #             # If this plant is harvestable AND colliding with player
# # #             if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
# # #                 # Add the plant to player inventory
# # #                 self.player_add(plant.plant_type)

# # #                 # Destroy this plant
# # #                 plant.kill()

# # #                 # Make a particle object to facilitate destroy animation
# # #                 Particle((plant.x, plant.y),plant.image,self.all_sprites,LAYERS['main']) # Default duration

# # #                 # Finally, remove the P marker from the ground grid
# # #                 self.soilLayer.grid[plant.x // TILE_SIZE][plant.y // TILE_SIZE].remove('P')
    
# # #     def run(self, dt):
# # #         # Run the entire level before updating to the display
# # #         # Fill the farm surface with black so that map edges don't attempt to overfill
# # #         self.farmScreen.fill('black')

# # #         # Draw all sprites
# # #         self.all_sprites.custom_draw(self.player)

# # #         # If the shop's active
# # #         if self.menu_active:
# # #             # Update the shop
# # #             self.menu.update()
# # #         # If it's not
# # #         else:
# # #             # Update all the sprites
# # #             self.all_sprites.update(dt)

# # #             # See if any plants are collided with player's new position
# # #             self.plant_collision()

# # #             # If it's raining, update the rain
# # #             if self.soilLayer.raining:
# # #                 self.rain.update()

# # #         # Display the overlay
# # #         self.overlay.display()

# # #         # Display the sky
# # #         self.sky.display(dt)

# # #         # If the player's sleeping, play the transition
# # #         if self.player.sleep:
# # #             self.transition.play()
# # import pygame
# # from pytmx.util_pygame import load_pygame
# # from random import randint
# # from constants import *
# # from sprites import Terrain, WaterTile, WildFlower, Tree, Interaction, Particle
# # from SoilLayer import SoilLayer
# # from weather import Snow, Snowflake
# # from overlay import Overlay
# # from cameraGroup import CameraGroup
# # from transition1 import Transition
# # from menu1 import Menu
# # from support import import_folder
# # from player import Player


# # class Level:
# #     def __init__(self, farm_screen):
# #         # Display surface for the game
# #         self.farm_screen = farm_screen

# #         # Sprite groups
# #         self.all_sprites = CameraGroup(self.farm_screen)  # Handles camera movements
# #         self.collision_sprites = pygame.sprite.Group()  # Handles collisions
# #         self.tree_sprites = pygame.sprite.Group()  # Tree-specific sprites
# #         self.interactive_sprites = pygame.sprite.Group()  # Interactable objects

# #         # Soil Layer
# #         self.soil_layer = SoilLayer(self.all_sprites)

# #         # Determine weather conditions
# #         self.snowing = randint(0, 10) <= 3  # 30% chance for snow

# #         # Initialize all components
# #         self.setup()

# #         # Overlay for UI
# #         self.overlay = Overlay(self.player)

# #         # Day transition
# #         self.transition = Transition(self.reset, self.player)

# #         # Snow
# #         self.snow = Snow(self.all_sprites) if self.snowing else None

# #         # Menu
# #         self.menu = Menu(self.player, self.toggle_shop, self.farm_screen)
# #         self.menu_active = False

# #         # Background music
# #         pygame.mixer.music.load('graphics/score.mp3')
# #         pygame.mixer.music.play(-1)  # Loop indefinitely
# #         pygame.mixer.music.set_volume(0.5)

# #     def setup(self):
# #         # Load the map
# #         sprite_data = load_pygame('data/map.tmx')

# #         # Import house layers
# #         for layer in ['HouseFloor', 'HouseFurnitureBottom']:
# #             for x, y, surf in sprite_data.get_layer_by_name(layer).tiles():
# #                 Terrain((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

# #         for layer in ['HouseWalls', 'HouseFurnitureTop']:
# #             for x, y, surf in sprite_data.get_layer_by_name(layer).tiles():
# #                 Terrain((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

# #         # Load water animation frames
# #         lake_frames = import_folder('graphics/water')
# #         if not lake_frames:
# #             fallback_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
# #             fallback_surface.fill((0, 0, 255))  # Blue placeholder
# #             lake_frames = [fallback_surface]

# #         # Add WaterTile objects to the map
# #         for x, y, _ in sprite_data.get_layer_by_name('Water').tiles():
# #             WaterTile(
# #                 start_pos=(x * TILE_SIZE, y * TILE_SIZE),
# #                 sprite_sequence=lake_frames,
# #                 group_list=self.all_sprites
# #             )

# #         # Add trees, decorations, collision tiles, etc.
# #         for tree in sprite_data.get_layer_by_name('Trees'):
# #             Tree(
# #                 start_pos=(tree.x, tree.y),
# #                 texture=tree.image,
# #                 group_list=[self.all_sprites, self.collision_sprites, self.tree_sprites],
# #                 player_inventory=self.player_add
# #             )

# #         for flower in sprite_data.get_layer_by_name('Decoration'):
# #             WildFlower(
# #                 start_pos=(flower.x, flower.y),
# #                 sprite_sequence=import_folder('graphics/flowers'),
# #                 group_list=[self.all_sprites, self.collision_sprites]
# #          )

# #         # Player and interactable objects
# #         for obj in sprite_data.get_layer_by_name('Player'):
# #             if obj.name == 'Start':
# #                 self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites,
# #                                  self.tree_sprites, self.interactive_sprites, self.soil_layer, self.toggle_shop)
# #             elif obj.name == 'Trader':
# #                 Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactive_sprites, obj.name)
# #             else:
# #                 Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactive_sprites, obj.name)

# #         # Add the ground layer
# #         Terrain((0, 0), pygame.image.load('graphics/world/ground.png').convert_alpha(), self.all_sprites, LAYERS['ground'])
# #         def player_add(self, item):
# #             # Add item to player's inventory
# #             self.player.item_inventory[item] += 1

# #     def toggle_shop(self):
# #         # Toggle shop menu
# #         self.menu_active = not self.menu_active

# #     def reset(self):
# #         # Reset the level for a new day
# #         self.soil_layer.update_plants()

# #         # Determine next day's weather
# #         self.snowing = randint(0, 10) <= 3

# #         # Reset snow objects
# #         if self.snowing:
# #             self.snow = Snow(self.all_sprites)
# #         else:
# #             self.snow = None

# #         # Reset fruits on trees
# #         for tree in self.tree_sprites:
# #             for apple in tree.fruit_sprites:
# #                 apple.kill()
# #             tree.create_fruits()

# #     def plant_collision(self):
# #         # Check for collisions between player and plants
# #         for plant in self.soil_layer.plant_sprites:
# #             if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
# #                 self.player_add(plant.plant_type)
# #                 plant.kill()
# #                 Particle((plant.rect.x, plant.rect.y), plant.image, self.all_sprites, LAYERS['main'])
# #                 self.soil_layer.grid[plant.rect.y // TILE_SIZE][plant.rect.x // TILE_SIZE].remove('P')

# #     def run(self, dt):
# #         # Main game logic
# #         self.farm_screen.fill('black')
# #         self.all_sprites.custom_draw(self.player)

# #         if self.menu_active:
# #             self.menu.update()
# #         else:
# #             self.all_sprites.update(dt)
# #             self.plant_collision()

# #             # Update snow effects
# #             if self.snowing:
# #                 self.snow.update()

# #         self.overlay.display()

# #         if self.player.sleep:
# #             self.transition.play()
# import pygame
# from constants import *
# from player import Player
# from overlay import Overlay
# from sprites import Terrain, WaterTile, WildFlower, Tree, Interaction, Particle
# from pytmx.util_pygame import load_pygame
# from support import import_folder
# from transition1 import Transition
# from SoilLayer import SoilLayer
# from weather import Snow
# from menu1 import Menu
# from cameraGroup import CameraGroup
# from animal import Animal
# from random import randint, choice
# from sprite_loader import load_spritesheet
# from pomodoroTimer import Pomodoro

# class Level:
#     def __init__(self, farm_screen):
#         # Display surface
#         self.farm_screen = farm_screen

#         # Sprite groups
#         self.all_sprites = CameraGroup(self.farm_screen)
#         self.collision_sprites = pygame.sprite.Group()
#         self.tree_sprites = pygame.sprite.Group()
#         self.interaction_sprites = pygame.sprite.Group()
#         self.animal_sprites = pygame.sprite.Group()

#         # Soil and weather
#         self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
#         self.snowing = randint(0, 10) <= 3

#         # Timer
#         self.pomodoro = Pomodoro()
#         self.timer_active = False

#         # Setup level and animals
#         self.setup()
#         self.setup_animals()

#         # UI elements
#         self.overlay = Overlay(self.player)
#         self.transition = Transition(self.reset, self.player)
#         self.snow = Snow(self.all_sprites) if self.snowing else None
        
#         # Menu
#         self.menu = Menu(self.player, self.toggle_shop, self.farm_screen)
#         self.menu_active = False

#         # Music
#         self.setup_audio()

#     def setup_audio(self):
#         try:
#             pygame.mixer.music.load('graphics/music.mp3')
#             pygame.mixer.music.play(-1)
#             pygame.mixer.music.set_volume(0.3)
#         except:
#             print("Music file not found")

#     def setup(self):
#         tmx_data = load_pygame('data/map.tmx')

#         # Setup house floors (no collision)
#         for layer in ['HouseFloor', 'HouseFurnitureBottom']:
#             for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
#                 Terrain(
#                     pos=(x * TILE_SIZE, y * TILE_SIZE),
#                     surf=surf,
#                     groups=[self.all_sprites],
#                     z=LAYERS['house bottom']
#                 )

#         # Setup house walls (with selective collision)
#         for layer in ['HouseWalls', 'HouseFurnitureTop']:
#             for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
#                 groups = [self.all_sprites]
#                 if layer == 'HouseWalls':
#                     # Only add collision for walls, not doors
#                     if not any(door in getattr(surf, 'name', '').lower() for door in ['door', 'entrance']):
#                         groups.append(self.collision_sprites)
#                 Terrain((x * TILE_SIZE, y * TILE_SIZE), surf, groups, LAYERS['main'])

#         # Setup fence
#         for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
#             Terrain(
#                 (x * TILE_SIZE, y * TILE_SIZE),
#                 surf,
#                 [self.all_sprites, self.collision_sprites]
#             )

#         # Setup water
#         water_frames = import_folder('graphics/water')
#         for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
#             WaterTile(
#                 (x * TILE_SIZE, y * TILE_SIZE),
#                 water_frames,
#                 self.all_sprites
#             )

#         # Setup trees
#         for obj in tmx_data.get_layer_by_name('Trees'):
#             Tree(
#                 pos=(obj.x, obj.y),
#                 surf=obj.image,
#                 groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
#                 name=obj.name,
#                 player_add=self.player_add
#             )

#         # Setup decoration
#         for obj in tmx_data.get_layer_by_name('Decoration'):
#             WildFlower(
#                 pos=(obj.x, obj.y),
#                 surf=obj.image,
#                 groups=[self.all_sprites, self.collision_sprites]
#             )

#         # Setup player and interactions
#         for obj in tmx_data.get_layer_by_name('Player'):
#             if obj.name == 'Start':
#                 self.player = Player(
#                     pos=(obj.x, obj.y),
#                     group=self.all_sprites,
#                     collision_sprites=self.collision_sprites,
#                     tree_sprites=self.tree_sprites,
#                     interaction_sprites=self.interaction_sprites,
#                     soil_layer=self.soil_layer,
#                     toggle_shop=self.toggle_shop
#                 )
#             elif obj.name == 'Trader':
#                 Interaction(
#                     pos=(obj.x, obj.y),
#                     size=(obj.width, obj.height),
#                     groups=self.interaction_sprites,
#                     name=obj.name
#                 )
#             else:  # Bed
#                 Interaction(
#                     pos=(obj.x, obj.y),
#                     size=(obj.width, obj.height),
#                     groups=self.interaction_sprites,
#                     name=obj.name
#                 )

#         # Ground
#         ground = pygame.image.load('graphics/world/ground.png').convert_alpha()
#         Terrain((0, 0), ground, self.all_sprites, LAYERS['ground'])

#     def setup_animals(self):
#         """Setup farm animals with proper positioning."""
#         try:
#             # Define safe spawn areas
#             SAFE_AREA = {
#                 'x_min': 400,
#                 'x_max': 800,
#                 'y_min': 400,
#                 'y_max': 600
#             }

#             # Create animals with spacing
#             animal_types = ['cow', 'chicken', 'pig']
#             spacing = 150  # Space between animals
            
#             for i, animal_type in enumerate(animal_types):
#                 x = SAFE_AREA['x_min'] + (i * spacing)
#                 y = SAFE_AREA['y_min']
                
#                 Animal(
#                     animal_type=animal_type,
#                     start_pos=(x, y),
#                     groups=[self.all_sprites, self.animal_sprites],
#                     collision_sprites=self.collision_sprites
#                 )
#                 print(f"Created {animal_type} at ({x}, {y})")

#         except Exception as e:
#             print(f"Error in setup_animals: {e}")

#     def handle_input(self):
#         """Handle keyboard input including timer controls."""
#         keys = pygame.key.get_pressed()
        
#         # Start timer with T key
#         if keys[pygame.K_t] and not self.timer_active:
#             self.timer_active = True
#             self.pomodoro.setup()

#     def player_add(self, item):
#         self.player.item_inventory[item] += 1

#     def toggle_shop(self):
#         self.menu_active = not self.menu_active

#     def reset(self):
#         # Reset day/night cycle
#         self.soil_layer.update_plants()

#         # Reset weather
#         self.snowing = randint(0, 10) <= 3
#         if self.snowing:
#             self.snow = Snow(self.all_sprites)
#         else:
#             self.snow = None

#         # Reset trees
#         for tree in self.tree_sprites.sprites():
#             for apple in tree.apple_sprites.sprites():
#                 apple.kill()
#             tree.create_fruit()

#     def plant_collision(self):
#         if hasattr(self.soil_layer, 'plant_sprites'):
#             for plant in self.soil_layer.plant_sprites.sprites():
#                 if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
#                     self.player_add(plant.plant_type)
#                     plant.kill()
#                     Particle(
#                         pos=plant.rect.topleft,
#                         surf=plant.image,
#                         groups=self.all_sprites,
#                         z=LAYERS['main']
#                     )
#                     self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
#     def display_timer(self):
#         if self.timer_active:
#             font = pygame.font.SysFont('couriernew', 32)
#             # Create timer display
#             if self.pomodoro.working:
#                 text = f"Work Time: {self.pomodoro.work_inter}m"
#                 color = (255, 100, 100)  # Red for work
#             else:
#                 text = f"Break Time: {self.pomodoro.play_inter}m"
#                 color = (100, 255, 100)  # Green for break
            
#             timer_surf = font.render(text, True, color)
#             timer_rect = timer_surf.get_rect(topleft=(10, 10))
#             self.farm_screen.blit(timer_surf, timer_rect)

#     def run(self, dt):
#         # Handle input
#         self.handle_input()

#         # Draw base
#         self.farm_screen.fill('black')

#         # Update timer if active
#         if self.timer_active:
#             self.pomodoro.run()

#         # Update game
#         if self.menu_active:
#             self.menu.update()
#         else:
#             self.all_sprites.custom_draw(self.player)
#             self.all_sprites.update(dt)
#             self.plant_collision()
            
#             if self.snowing:
#                 self.snow.update()
                
#         if self.timer_active:
#             self.display_timer()

#         # UI Elements
#         self.overlay.display()

#         # Transition effect
#         if self.player.sleep:
#             self.transition.play()

# level1.py

import pygame
from constants import *
from player import Player
from overlay import Overlay
from sprites import Terrain, WaterTile, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from sprite_loader import import_folder
from transition1 import Transition
from SoilLayer import SoilLayer
from weather import Snow
from menu1 import Menu
from cameraGroup import CameraGroup
from animal import Animal
from random import randint
from pomodoroTimer import Pomodoro

class Level:
    def __init__(self, farm_screen):
        # Display surface
        self.farm_screen = farm_screen

        # Sprite groups
        self.all_sprites = CameraGroup(self.farm_screen)
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.animal_sprites = pygame.sprite.Group()

        # Soil and weather
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.snowing = True  # Start with snow falling

        # Timer
        self.pomodoro = Pomodoro(self.farm_screen)
        self.timer_active = False

        # Setup level and animals
        self.setup()
        self.setup_animals()

        # UI elements
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        self.snow = Snow(self.all_sprites) if self.snowing else None

        # Menu
        self.menu = Menu(self.player, self.toggle_shop, self.farm_screen)
        self.menu_active = False

        # Music
        self.setup_audio()

    def setup_audio(self):
        try:
            pygame.mixer.music.load('graphics/score.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except:
            print("Music file not found")

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')

        # Setup house floors (no collision)
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                if surf:
                    Terrain(
                        pos=(x * TILE_SIZE, y * TILE_SIZE),
                        surf=surf,
                        groups=[self.all_sprites],
                        z=LAYERS['house bottom']
                    )

        # Setup house walls with collision, excluding the doorway
        for x, y, surf in tmx_data.get_layer_by_name('HouseWalls').tiles():
            if surf:
                tile_pos = (x * TILE_SIZE, y * TILE_SIZE)
                if not self.is_doorway_tile(x, y):
                    Terrain(
                        pos=tile_pos,
                        surf=surf,
                        groups=[self.all_sprites, self.collision_sprites],
                        z=LAYERS['main']
                    )
                else:
                    Terrain(
                        pos=tile_pos,
                        surf=surf,
                        groups=[self.all_sprites],
                        z=LAYERS['main']
                    )

        # Setup house furniture top without collision
        for x, y, surf in tmx_data.get_layer_by_name('HouseFurnitureTop').tiles():
            if surf:
                Terrain(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=surf,
                    groups=[self.all_sprites],
                    z=LAYERS['main']
                )

        # Setup fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            if surf:
                Terrain(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=surf,
                    groups=[self.all_sprites, self.collision_sprites]
                )

        # Setup water
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            if surf:
                WaterTile(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    frames=water_frames,
                    groups=[self.all_sprites]
                )

        # Setup trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=obj.name,
                player_add=self.player_add
            )

        # Setup decoration
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites]
            )

        # Setup collision tiles from the Collision layer
        for x, y, _ in tmx_data.get_layer_by_name('Collision').tiles():
            if not self.is_doorway_tile(x, y):
                Terrain(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA),
                    groups=[self.collision_sprites]
                )

        # Setup player and interactions
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction_sprites=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop
                )
            elif obj.name == 'Trader':
                Interaction(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=self.interaction_sprites,
                    name=obj.name
                )
            elif obj.name == 'Bed':
                Interaction(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=self.interaction_sprites,
                    name=obj.name
                )

        # Ground
        ground = pygame.image.load('graphics/world/ground.png').convert_alpha()
        Terrain((0, 0), ground, self.all_sprites, LAYERS['ground'])

    def is_doorway_tile(self, x, y):
        # Replace these with the actual tile coordinates of your doorway
        doorway_tiles = [
            (15, 10),
            (16, 10),
            # Add more tuples if the doorway spans multiple tiles
        ]
        return (x, y) in doorway_tiles

    def setup_animals(self):
        """Setup only a chicken with proper positioning."""
        try:
            # Place the chicken near the player
            chicken_position = (self.player.rect.centerx - 50, self.player.rect.centery)
            Animal(
                animal_type='chicken',
                start_pos=chicken_position,
                groups=[self.all_sprites, self.animal_sprites],
                collision_sprites=self.collision_sprites
            )
            print(f"Created chicken at {chicken_position}")
        except Exception as e:
            print(f"Error in setup_animals: {e}")

    def handle_input(self, event_list):
        """Handle keyboard input including timer controls."""
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and not self.timer_active:
                    self.pomodoro.setup()
                    self.timer_active = True

    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def toggle_shop(self):
        self.menu_active = not self.menu_active

    def reset(self):
        # Reset day/night cycle
        self.soil_layer.update_plants()

        # Reset weather
        self.snowing = True  # Keep snowing as per your requirement
        if self.snowing:
            if not self.snow:
                self.snow = Snow(self.all_sprites)
        else:
            if self.snow:
                self.snow.kill()
                self.snow = None

        # Reset trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

    def plant_collision(self):
        if hasattr(self.soil_layer, 'plant_sprites'):
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.rect):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(
                        pos=plant.rect.topleft,
                        surf=plant.image,
                        groups=self.all_sprites,
                        z=LAYERS['main']
                    )
                    grid_x = plant.rect.centerx // TILE_SIZE
                    grid_y = plant.rect.centery // TILE_SIZE
                    self.soil_layer.grid[grid_y][grid_x].remove('P')

    def run(self, dt, event_list):
        # Handle input
        self.handle_input(event_list)

        # Draw base
        self.farm_screen.fill('black')

        # Update game elements
        if self.menu_active:
            self.menu.update()
        else:
            self.all_sprites.custom_draw(self.player)
            self.all_sprites.update(dt)
            self.plant_collision()

        # UI Elements
        self.overlay.display()

        # Draw snow on top of everything
        if self.snowing and self.snow:
            self.snow.update(dt)  # Pass dt here

        # Update timer if active
        if self.timer_active:
            self.pomodoro.run(event_list)
            self.timer_active = self.pomodoro.timer_active

        # Transition effect
        if self.player.sleep:
            self.transition.play()
