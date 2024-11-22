import pygame
import constants as c
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self. rect = self.image.get_rect(topleft = pos)
        self.z = c.LAYERS["soil"]

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f"..graphics/fruit/{plant_type}")
        self.soil = soil
        self.check_watered = check_watered

        # grow
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = c.GROW_SPEED[plant_type]
        self.harvestable = False

        # sprite
        self.image = self.frame[self.age]
        self.y_offset = - 16 if plant_type == "corn" else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = c.LAYERS["ground plant"]

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            # plant age +1 --> collision
            if int(self.age) > 0:
                self.z = c.LAYERS["main"]
                self.hitbox = self.rect.copy().inflate(x = -26, y = -self.rect.height * 0.4)

            # make sure it stops growing after max age
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            self.image = self.frame[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        
class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        # groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        #imgs
        self.soil_surface = pygame.image.load("../graphics/soil/o.png")

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load("..graphics/world/ground.png")
        h_tiles, v_tiles= ground.get_width() // c.TILE_SIZE, ground.get_height() // c.TILE_SIZE
        #print(h_tiles)
        #print(v_tiles)
        
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles) ]
        #print(self.grid)
        for x, y, _ in load_pygame("../data/map/tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append("F")
        #print(self.grid)
        #for row in self.grid:
        #    print(row)

    def create_hit_rects(self):
        self.hit_rects = []
        # find array inside array)
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "F" in cell:
                    x = index_col * c.TILE_SIZE
                    y = index_row * c.TILE_SIZE
                    rect = pygame.Rect(x, y, c.TILE_SIZE, c.TILE_SIZE)
                    self.hit_rects.append(rect)

    def check_watered(self, pos):
        x = pos[0] // c.TILE_SIZE  #self.rect.center returns a tuple, thus the indexing
        y = pos[1] // c.TILE_SIZE
        cell = self.grid[x][y]
        is_watered = "W" in cell
        return is_watered

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprite.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // c.TILE_SIZE
                y = soil_sprite.rect.y // c.TILE_SIZE

                if "P" not in self.grid[y][x]:
                    self.grid[y][x].append("P")
                    Plant(plant_type = seed, 
                          groups = [self.all_sprites, self.plant_sprites],
                          soil = soil_sprite,
                          collision = self.collision_sprites,
                          watered = self.check_watered)

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def create_soil_tiles(self):
        self.soil_sprites.empty()

        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "X" in cell:
                    SoilTile(
                        pos = ((index_col * c.TILE_SIZE),(index_row * c.TILE_SIZE)), 
                        surf = self.soil_surface, 
                        groups = [self.all_sprites,self.soil_sprites])
        
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoints(point):
                x = rect.x // c.TILE_SIZE
                y = rect.y // c.TILE_SIZE

                if "F" in self.grid[y][x]:
                    #print("Farmable")
                    self.grid[y][x].append("X")
                    self.create_soil_tiles()
