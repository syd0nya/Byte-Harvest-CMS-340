import pygame
from constants import *
from pygame import Vector2
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = SPEED
        
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle':[], 'up_idle':[], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [], 
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
            
        print(self.animations)
        
        
    def input(self):
        
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
            
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1  
            self.status = 'right' 
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
            
        print(self.direction)  
        
        
    def get_status(self):
        """
        If the player is not moving:
        
        Add _idle to the status then
        
        """
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        
    def animate(self, dt):
        # self.frame_index starts at 0 which gets us the very first image
        self.frame_index += 4 * dt # increase by a certain number
        # this basically 
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0 # makes sure that no error happens when it gets to the end of the animations
        self.image = self.animations[self.status][int(self.frame_index)] # getting the integer of the animations
        
    def move(self, dt):
        # normalizing the vector to make sure the direction of the vector is always 1
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
       
        
           
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
            