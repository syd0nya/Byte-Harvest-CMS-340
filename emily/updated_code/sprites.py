import pygame
from random import randint, choice
from constants import *

class Terrain(pygame.sprite.Sprite):
    def __init__(self, start_pos, texture, group_list, depth=LAYERS['main']):
        super().__init__(group_list)
        self.image = texture
        self.rect = self.image.get_rect(topleft=start_pos)
        self.depth = depth
        
        # find the collision boundaries 
        shrink_x = self.rect.width * 0.2
        shrink_y = self.rect.height * 0.75
        self.bounds = self.rect.copy().inflate(-shrink_x, -shrink_y)
        
class WaterTile(Terrain):
    def __init__(self, start_pos, sprite_sequence, group_list):
        # Set up animation sequence
        self.sprites = sprite_sequence
        self.anim_index = 0
        
        # initialize the sprite within the first frame 
        super().__init__(
            start_pos=start_pos,
            texture=self.sprites[self.anim_index],
            group_list=group_list,
            depth=LAYERS['water']
        )

class WildFlower(Terrain):
    def __init__(self, start_pos, sprite_sequence, group_list):
        # Set up animation sequence
        self.sprites = sprite_sequence
        self.anim_index = 0

        #  initialize the sprite within the first frame
        super().__init__(
            start_pos=start_pos, 
            texture=self.sprites[self.anim_index],
              group_list=group_list
        )

        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

    def update(self, dt):
        #animate by going through sequence
        self.anim_index += 3 * dt
        if self.anim_index >= len(self.sprites):
            self.anim_index = 0
        self.image = self.sprites[int(self.anim_index)]


class Tree(Terrain):
    def __init__(self, start_pos, texture, group_list, player_inventory):
        super().__init__(start_pos, texture, group_list)
        self.health = 5
        self.alive = True
        self.stump_texture = pygame.image.load(r'C:\Users\sydth\OneDrive\Desktop\ByteHarvestGame\flowers\large.png').convert_alpha()
        self.fruit_texture = pygame.image.load(r'C:\Users\sydth\OneDrive\Desktop\ByteHarvestGame\flowers\apple.png').convert_alpha()
        self.fruit_positions = [(10, -30), (-20, -40), (15, -50)] 
        self.fruits = pygame.sprite.Group()
        self.player_inventory = player_inventory

        # Generate fruits
        self.create_fruits()

        # Axe sound
        self.axe_sound = pygame.mixer.Sound(r'C:\Users\sydth\OneDrive\Desktop\ByteHarvestGame\flowers\axe.mp3')

    def create_fruits(self):
       
        for pos in self.fruit_positions:
            if randint(0, 10) < 5: 
                fruit = pygame.sprite.Sprite(self.fruits)
                fruit.image = self.fruit_texture
                fruit.rect = fruit.image.get_rect(
                    topleft=(self.rect.x + pos[0], self.rect.y + pos[1])
                )

    def take_damage(self):
       
        if self.alive:
            self.health -= 1
            self.axe_sound.play()

            # Drop a fruit if available
            if len(self.fruits) > 0:
                random_fruit = choice(self.fruits.sprites())
                random_fruit.kill()  
                self.player_inventory.append("apple")  

            # Check if tree is dead
            if self.health <= 0:
                self.alive = False
                self.image = self.stump_texture
                self.rect = self.image.get_rect(topleft=self.rect.topleft)
                self.player_inventory.append("wood")  

    def update(self, *args):
        if self.alive:
            self.fruits.update(*args)
