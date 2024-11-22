import pygame
from constants import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from shop import Menue
from sky import Rain, Sky

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		# soil + reset
		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset, self.player)

		# shop
		self.menue = Menue(
			player = self.player,
			toggle_menue= self.toggle_shop
		)
		self.shop_active = False

		#sky
		self.sky = Sky()

	def setup(self):
		tmx_data = load_pygame('data/map.tmx')

		# house 
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

		# Fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		# water 
		water_frames = import_folder('graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		# trees 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(	pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		# wildflowers 
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		# collion tiles
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		# Player 
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), 
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soild_layer = self.soil_layer,
					toggle_shop = self.toggle_shop
					)
			if obj.name == "Bed":
				Interaction(position = (obj.x,obj.y), 
							size = (obj.width,obj.height), 
							groups = self.interaction_sprites, 
							name = obj.name)

			if obj.name == "Trader":
				Interaction(position = (obj.x,obj.y), 
							size = (obj.width,obj.height), 
							groups = self.interaction_sprites, 
							name = obj.name)


		Generic(
			pos = (0,0),
			surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def toggle_shop(self):
		self.shop_active = not self.shop_active
	
	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)
		self.all_sprites.update(dt)
		self.plant_collision()
		
		# upadte
		if self.shop_active:
			self.menue.update
		else:
			self.all_sprites.update(dt)
			self.plant_collision()

		self.overlay.display()

		#rain
		if self.raining and not self.shop_active:
			self.rain.update()
		
		#day
		self.sky.display(dt)

		if self.player.sleep:
			self.transition.play()

		#shop
		#print(self.shop_active)
		#inveotry - harvest
		#print(self.player.item_inventory)

	def reset(self):
		# plants
		self.soil_layer.update_plants()

		# reset trees
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()

		# reset sky (night --> day)
		self.sky.start_color = [255, 255, 255]


	def plant_collision(self):
		# if there are any plants
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					# update inventory
					self.player_add(plant.plant_type)
					# remove from layers
					plant.kill()
					# for cool dissapear effect
					Particle(pos = plant.rect.topleft,
			  				surf = plant.image,
							groups = self.all_sprites,
							z = LAYERS["main"])
					# clear soil grid
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove("P") # [row][col]

	
class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)
