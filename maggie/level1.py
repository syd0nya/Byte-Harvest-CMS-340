# Class to run all of the game aspects
# Imports
import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition1 import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu1 import Menu
from cameraGroup import CameraGroup

class Level:
    def __init__(self, farmScreen):
        # Constructor
        # Set up the farm surface on which everything will be drawn
        self.farmScreen = farmScreen

        # Make sprite groups for player call later
        self.all_sprites = CameraGroup(self.farmScreen) # All sprites that move according to the camera
        self.collision_sprites = pygame.sprite.Group() # Have collisions
        self.tree_sprites = pygame.sprite.Group() # Trees
        self.interactive_sprites = pygame.sprite.Group() # Interactable

        # Make the soil layer
        self.soilLayer = SoilLayer(self.all_sprites, self.collision_sprites)

        # Determine if it's going to rain (stored in the SoilLayer class)
        self.soilLayer.raining = randint(0,10) <= 3 # 30% chance

        # Call setup() so that we can make the overlay and menu
        self.setup()

        # Make the overlay
        self.overlay = Overlay(self.player)

        # Make the transition
        self.transition = Transition(self.reset, self.player)

        # Make the sky
        self.sky = Sky()
        self.rain = Rain(self.all_sprites)

        # Make the menu
        self.menu = Menu(self.player, self.toggle_shop, self.farmScreen)
        self.menu_active = False # Make sure the menu isn't immediately active

        # Import the music and set music settings
        pygame.mixer.music.load('../audio/score.mp3')
        pygame.mixer.music.play(-1) # Infinite loops
        pygame.mixer.music.set_volume(0.0)

    def setup(self):
        # General set up
        # Upload map and other sprites
        sprite_data = load_pygame('../data/map.tmx')

        # Import house layers 
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in sprite_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in sprite_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

		# Import fence
        for x, y, surf in sprite_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Import water
        lake_frames = import_folder('../graphics/water')
        for x, y, surf in sprite_data.get_layer_by_name('Water').tiles(): #MAGGIE See if you can remove surf
            Water((x*TILE_SIZE, y*TILE_SIZE), lake_frames, self.all_sprites)

        # Import Trees
        for tree in sprite_data.get_layer_by_name('Trees'):
            Tree((tree.x, tree.y), tree.image, [self.all_sprites, self.collision_sprites, self.tree_sprites],
                 tree.name, self.player_add)

        # Import Wildflowers
        for flower in sprite_data.get_layer_by_name('Decoration'):
            WildFlower((flower.x, flower.y), flower.image, [self.all_sprites, self.collision_sprites])

        # Import collision tiles (stored as csv)
        for x, y, surf in sprite_data.get_layer_by_name('Collision').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), [self.collision_sprites]) # Layer the same as default so not included

        # tmx file stores player, shop, and bed in Player group
        for obj in sprite_data.get_layer_by_name('Player'):
            # Get the player
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites,
                                     self.tree_sprites, self.interactive_sprites, self.soilLayer, self.toggle_shop)
                
            # Get the shop as an interactive sprite
            elif obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactive_sprites,
                            obj.name)
                
            # Get the bed as an interactive sprite (only one left in player group)
            else:
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactive_sprites,
                            obj.name)
                
        # Import ground
        Generic((0,0), pygame.image.load('../graphics/world/ground.png').convert_alpha(), self.all_sprites, LAYERS['ground'])

    def player_add(self, item):
        # Add item to player's inventory
        self.player.item_inventory[item] += 1

    def toggle_shop(self):
        # Toggle whether the shop screen is active or not
        self.menu_active = not self.menu_active

    def reset(self):
        # Reset the entire level, to be used in transition
        # Update all plants to current grow stages
        self.soilLayer.update_plants()

        # Determine if it will rain for the next day
        self.soilLayer.raining = randint(0,10) <= 3
        if self.soilLayer.raining:
            # If it does, auto water the plants
            self.soilLayer.water_all
        else:
            # If it doesn't, unwater all the plants
            self.soilLayer.remove_water

        # Delete and remake apples on trees to randomize positions
        for tree in self.tree_sprites:
            for apple in tree.apple_sprites:
                apple.kill()
            tree.create_fruit
        
        # Reset the sky color to max
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        # Check if any of the plants are being harvested by the player
        # For any existing plants
        for plant in self.soilLayer.plant_sprites:
            # If this plant is harvestable AND colliding with player
            if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                # Add the plant to player inventory
                self.player_add(plant.plant_type)

                # Destroy this plant
                plant.kill()

                # Make a particle object to facilitate destroy animation
                Particle((plant.x, plant.y),plant.image,self.all_sprites,LAYERS['main']) # Default duration

                # Finally, remove the P marker from the ground grid
                self.soilLayer.grid[plant.x // TILE_SIZE][plant.y // TILE_SIZE].remove('P')
    
    def run(self, dt):
        # Run the entire level before updating to the display
        # Fill the farm surface with black so that map edges don't attempt to overfill
        self.farmScreen.fill('black')

        # Draw all sprites
        self.all_sprites.custom_draw(self.player)

        # If the shop's active
        if self.menu_active:
            # Update the shop
            self.menu.update()
        # If it's not
        else:
            # Update all the sprites
            self.all_sprites.update(dt)

            # See if any plants are collided with player's new position
            self.plant_collision()

            # If it's raining, update the rain
            if self.soilLayer.raining:
                self.rain.update()

        # Display the overlay
        self.overlay.display()

        # Display the sky
        self.sky.display(dt)

        # If the player's sleeping, play the transition
        if self.player.sleep:
            self.transition.play()
