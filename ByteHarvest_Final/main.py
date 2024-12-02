import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LAYERS
from player import Player
from SoilLayer import SoilLayer
from sprites import WaterTile, Terrain, Tree
from weather import Snow

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Byte Harvest - Test Run")
    clock = pygame.time.Clock()
    
    # Groups
    all_sprites = pygame.sprite.LayeredUpdates()
    collision_sprites = pygame.sprite.Group()
    water_sprites = pygame.sprite.Group()
    tree_sprites = pygame.sprite.Group()
    
    # Soil Layer
    soil_layer = SoilLayer(all_sprites)

    # Player
    player = Player(
        playerPos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        group=all_sprites,
        collisionSprites=collision_sprites,
        treeGraphics=tree_sprites,
        soilLayer=soil_layer,
        action=pygame.sprite.Group()  # Temporary placeholder for interactions
    )
    
    # Snow
    snow = Snow(all_sprites)

    # Create some trees for testing
    tree_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tree_texture.fill((0, 128, 0))  # Green placeholder
    for i in range(5):
        Tree(
            start_pos=(i * TILE_SIZE * 2, SCREEN_HEIGHT // 2),
            texture=tree_texture,
            group_list=[all_sprites, tree_sprites],
            player_inventory=player.itemInventory
        )

    # Ground layer (basic terrain)
    ground_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
    ground_texture.fill((139, 69, 19))  # Brown placeholder
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            Terrain(
                start_pos=(x, y),
                texture=ground_texture,
                group_list=[all_sprites],
                depth=LAYERS['ground']
            )

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Delta time for smooth movement
        dt = clock.tick(60) / 1000  # 60 FPS

        # Update
        all_sprites.update(dt)
        snow.update()

        # Draw
        screen.fill((135, 206, 250))  # Light blue for the sky
        all_sprites.draw(screen)
        pygame.display.flip()
    
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
