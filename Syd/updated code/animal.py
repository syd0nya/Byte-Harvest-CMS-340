import pygame
from support import import_folder 

class Animal(pygame.sprite.Sprite):
    def __init__(self, animal_type, start_pos, sprite_sequence_folder, speed, group_list):
        super().__init__(group_list)

        # Set the animal type
        self.animal_type = animal_type

        # Import sprites for the specific animal
        self.import_assets(sprite_sequence_folder)
        self.anim_index = 0
        self.image = self.animations['idle'][self.anim_index]
        self.rect = self.image.get_rect(topleft=start_pos)
        self.hitbox = self.rect.inflate(-20, -20) 
        self.position = pygame.math.Vector2(self.rect.topleft)

        # Movement
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)

        # Animation 
        self.status = 'idle'
        self.last_update_time = 0
        self.animation_speed = 0.2  

    def import_assets(self, sprite_sequence_folder):
        
        self.animations = {'idle': [], 'walk': [], 'run': []}
        base_path = f"{sprite_sequence_folder}/{self.animal_type}"
        for animation in self.animations.keys():
            path = f"{base_path}/{animation}"
            self.animations[animation] = import_folder(path)

    def set_direction(self, direction):
        
        self.direction = pygame.math.Vector2(direction)

        # Update based on movement
        if self.direction.magnitude() == 0:
            self.status = 'idle'
        else:
            self.status = 'walk'

    def animate(self, dt):
       
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed * 1000:
            self.last_update_time = current_time
            self.anim_index += 1
            if self.anim_index >= len(self.animations[self.status]):
                self.anim_index = 0
            self.image = self.animations[self.status][self.anim_index]

    def move(self, dt):
        
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.position += self.direction * self.speed * dt
        self.rect.topleft = self.position
        self.hitbox.center = self.rect.center

    def stop(self):
      
        self.set_direction((0, 0))

    def update(self, dt):
        
        self.move(dt)
        self.animate(dt)
