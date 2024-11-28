import pygame
from support import *
from pytmx.util_pygame import load_pygame
from constants import *
from sprites import Terrain, WaterTile



class GameLevel:
    def __init__(self):
        # Initialize display and sprites
        self.game_display = pygame.display.get_surface()
        self.sprite_collection = ViewportGroup()
        
        self.initialize_world()
        self.interface = (self.character) # used to be overlay (LEI)
    
    def initialize_world(self):
        # Load map data
        map_data = load_pygame('data/map.tmx')
        
        # Initialize house structures
        house_layers = ['HouseFloor', 'HouseFurnitureBottom']
        for current_layer in house_layers:
            for tile_x, tile_y, tile_surface in map_data.get_layer_by_name(current_layer).tiles():
                Terrain(
                    position=(tile_x * TILE_SIZE, tile_y * TILE_SIZE),
                    surface=tile_surface, 
                    groups=self.sprite_collection,
                    depth=LAYERS['house bottom']
                )
        
        upper_layers = ['HouseWalls', 'HouseFurnitureTop']
        for current_layer in upper_layers:
            for tile_x, tile_y, tile_surface in map_data.get_layer_by_name(current_layer).tiles():
                Terrain(
                    position=(tile_x * TILE_SIZE, tile_y * TILE_SIZE),
                    surface=tile_surface,
                    groups=self.sprite_collection,
                    depth=LAYERS['main']
                )
        
        # Initialize player
        # self.character = Character( # was player last time 
        #     position=(640, 360),
        #     groups=self.sprite_collection
        # )
        
        # Create fence boundaries
        for tile_x, tile_y, tile_surface in map_data.get_layer_by_name('Fence').tiles():
            Terrain(
                position=(tile_x * TILE_SIZE, tile_y * TILE_SIZE),
                surface=tile_surface,
                groups=self.sprite_collection,
                depth=LAYERS['main']
            )
        
        # Initialize water elements
        water_sprites = import_folder('graphics_2/water')
        for tile_x, tile_y, tile_surface in map_data.get_layer_by_name('Water').tiles():
            WaterTile(
                position=(tile_x * TILE_SIZE, tile_y * TILE_SIZE),
                animation_frames=water_sprites,
                groups=self.sprite_collection
            )
        
        # Set ground layer
        Terrain(
            position=(0, 0),
            surface=pygame.image.load('graphics/world/ground.png').convert_alpha(),
            groups=self.sprite_collection,
            depth=LAYERS['ground']
        )
    
    def update(self, delta_time):
        self.game_display.fill("black")
        self.sprite_collection.render(self.character)
        self.sprite_collection.update(delta_time)
        self.interface.render()

# used to be the CameraGroup, logic and style changed 
class ViewportGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.game_display = pygame.display.get_surface()
        self.camera_offset = pygame.math.Vector2()
    
    def render(self, target):
        # Calculate viewport offset based on target position
        self.camera_offset.x = target.rect.centerx - SCREEN_WIDTH / 2
        self.camera_offset.y = target.rect.centery - SCREEN_HEIGHT / 2
        
        # Render sprites by layer
        for depth in LAYERS.values():
            for game_object in self.sprites():
                if game_object.depth == depth:
                    viewport_rect = game_object.rect.copy()
                    viewport_rect.center -= self.camera_offset
                    self.game_display.blit(game_object.image, viewport_rect)
