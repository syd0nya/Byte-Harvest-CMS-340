import pygame
from constants import *
from random import randint, choice
from timer_game import Timer

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Water(Generic):
	def __init__(self, pos, frames, groups):

		#animation setup
		self.frames = frames
		self.frame_index = 0

		# sprite setup
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups, 
				z = LAYERS['water']) 

	def animate(self,dt):
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,dt):
		self.animate(dt)

class WildFlower(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Tree(Generic):
	def __init__(self, pos, surf, groups, name, player_add):
		super().__init__(pos, surf, groups)

		# tree attributes
		self.health = 5
		self.alive = True
		stump_path = f'graphics/stumps/{"small" if name == "Small" else "large"}.png'
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()
		self.invul_timer = Timer(200)

		# apples
		self.apple_surf = pygame.image.load('graphics/fruit/apple.png')
		self.apple_pos = APPLE_POS[name]
		self.apple_sprites = pygame.sprite.Group()
		self.create_fruit()

		# Adding to inventory
		self.player_add = player_add

	def damage(self):
		
		# damaging the tree
		self.health -= 1

		# remove an apple
		if len(self.apple_sprites.sprites()) > 0:
			random_apple = choice(self.apple_sprites.sprites())
			Particle(
				pos = random_apple.rect.topleft,
				surf = random_apple.image,
				groups = self.groups()[0],
				z = LAYERS['fruit'])
			# Update inventory with apple
			self.player_add('apple')
			random_apple.kill()

	def check_death(self):
		if self.health <= 0:
			self.image = self.stump_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
			self.alive = False
			# Update inventory with wood
			self.player_add('wood')

	def update(self,dt):
		if self.alive:
			self.check_death()

	def create_fruit(self):
		for pos in self.apple_pos:
			if randint(0,10) < 2:
				x = pos[0] + self.rect.left
				y = pos[1] + self.rect.top
				Generic(
					pos = (x,y), 
					surf = self.apple_surf, 
					groups = [self.apple_sprites,self.groups()[0]],
					z = LAYERS['fruit'])

class Particle(GenericFloor):

    # Inherit constructor
    def __init__(self, pos, surf, groups, z, duration = 200):
        super.__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks() # Get time of creation
        self.duration = duration # Store duration input as an attribute of the object

        # White surface over object
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface() # silhouette of original surface
        new_surf.set_colorkey((0,0,0)) # turning silhouette pure white
        self.image = new_surf

    # Self update method to clear sprite
    def update(self, dt):

        # Check duration of sprite life
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Interaction(GenericFloor):
	def __init__(self, position, size, groups, name):
		surface = pygame.surface(size)
		super().__init__(position, surface, groups)
		self.name = name