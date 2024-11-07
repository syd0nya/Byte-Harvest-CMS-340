import pygame
from constants import *
from pygame import Vector2
from support import import_folder
from timer_game import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        
        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos) # x and y positions 
        self.z = LAYERS['main'] # separate variable
        
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = SPEED
        
        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)            
            
        }
        
        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index] 
        
        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
        
    def use_tool(self):
        pass
        # print(self.selected_tool)
    def use_seed(self):
        pass
        
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
        
        if not self.timers['tool use'].active:
            
            # player shouldnt be able to use a tool if they are already using one
            # directions for moving
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
                
            # tool use
            if keys[pygame.K_SPACE]:
                # timer for the tool use
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2() # added so that the player doesn't continue moving in a direction while using the tool 
                self.frame_index = 0
                
            # change tools
            # timer must be added to wait a couple of milliseconds
            # Change tools
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]
                
            # seed use
            if keys[pygame.K_LCTRL]:
                # timer for the tool use
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2() # added so that the player doesn't continue moving in a direction while using the tool 
                self.frame_index = 0
                print('use seed')
            
            
            
            
            
            # change seed portion
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index = (self.seed_index + 1) % len(self.seeds)
                self.selected_seed = self.seeds[self.seed_index]
            
                
        
    def get_status(self):
        """
        If the player is not moving:
        
        Add _idle to the status then
        
        """
        #idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
            
        # tool use again here
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool
            
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
        
        
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
        self.update_timers()
        self.move(dt)
        self.animate(dt)
            