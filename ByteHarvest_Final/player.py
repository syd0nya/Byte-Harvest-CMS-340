import pygame
import constants
import random
from timer_byte import Timer
from SoilLayer import SoilLayer
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, playerPos, group, collisionSprites, treeGraphics, soilLayer, action):
        super().__init__(group) # imedaetly put instance of player inside of group
        
        # set un images / graphics
        self.animations = {}
        self.setUpAnimation()
        self.characterDisplayType = "down_idle"
        self.iGraphicFrame = 0

        self.characterGraphic = self.animations[self.characterDisplayType][self.iGraphicFrame]
        self.posRect = self.characterGraphic.get_rect(center = playerPos)
        self.layer = constants.LAYERS["main"]


        self.sleep = False
        self.treeSprite = treeGraphics
        self.soilLayer= soilLayer

        # set up [] of existing items to cycle through
        self.tools = ['hoe', 'axe', 'water']
        self.iTools = 0
        self.seeds = ['corn', 'tomato']
        self.iSeeds = 0

        # starting inventory
        self.itemInventory = {}
        self.seedInventory = {}
        self.money = None
        self.initializeStartingInventory()

        # movement
        self.direction = pygame.math.Vector2()
        self.playerPos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.hitbox = self.posRect.copy().inflate((-126, -70))  
        self.collisionSprites = collisionSprites

        #  actions
        self.action = action

        # timer - mvmnt and events smooth
        self.timers = {
            "tool_use": Timer(350, self.use_tool),
            "tool_switch": Timer(200),
            "seed_use": Timer(350, self.use_seed),
            "seed_switch": Timer(200),
        }

        # sound effects
        self.watering = pygame.mixer.Sound('graphics/water.mp3')
        self.watering.set_volume(0.2)
        
        
    # INITIALIZATION
    def setUpAnimation(self):
        self.animations = {"up": [],            "down": [],             "right": [],            "left": [],
                           "up_idle": [],       "down_idle": [],        "right_idle": [],       "left_idle": [],
                           "up_axe": [],        "down_axe": [],         "right_axe": [],        "right_axe": [],
                           "up_water": [],      "down_water": [],       "right_water": [],      "right_water": [],
                           "up_hoe": [],        "down_hoe": [],          "right_hoe": [],       "right_hoe": []
                        }
        
        # for each animation, make the path to access it
        for animation in self.animations.keys():
            path = "graphics/character/" + animation
            self.animations[animation] = import_folder(path)

    def initializeStartingInventory(self):
        # Starting plant / item inveorty
        self.itemInventory = {
			'wood': 20,
			'apple': 20,
			'corn': 20,
			'tomato': 20
		}
		
		# Starting seed inventory
        self.seedInventory = {
		'corn': 5,
		'tomato': 5
          
		}
		# Starting money
        self.money = 200

	# CODE SHORTCUTS... type less
    def cycleThroughTool(self):
        self.iTools = (self.iTools + 1) % len(self.tools)

    def cycleThroughSeeds(self):
        self.iSeeds = (self.iSeeds + 1) % len(self.seeds)

    def randomSleepIdle():
        r = random.randint(0,3)

        if r == 0:
            return "left_idle"
        elif r == 1:
            return "righ_idle"
        elif r == 2:
            return "up_idle"
        else:
            return "down_idle"

    def startTimer(self, timerType):
        self.timers[timerType].activate()
        self.direction = pygame.math.Vector2()
        self.iGraphicFrame = 0

    def updateTimer(self):
        for timer in self.timers.values():
            timer.update()

    # INTERACTION
    def getDirection(self):
        if self.direction.y < 0:
            return "up"
        elif self.direction.y > 0:
            return "down"
        elif self.direction.x < 0:
            return "left"
        elif self.direction.x > 0:
            return "right"
        return self.characterDisplayType
    
    def keyboardInput(self):
        keys = pygame.get_pressed()

        # mvmnt
        # =====
        # as long as player not asleep or using tool, they can move
        if self.sleep == False and self.timers["tool_use"].active == False:
            # vertical movemnt
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
            else:
                self.direction.y = 0

            # horizontal mvmnt
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
            else:
                self.direction.x = 0

            # update icon
            if self.direction.x != 0 or self.direction.y != 0:
                self.characterDisplayType = self.getDirection()
            
        # switch tools
        # ============
        # space.... start timer for tool_use
        # q.... change selected tool
        if keys[pygame.K_SPACE]:
            self.startTimer(timerType = "tool_use")
        if keys[pygame.K_q] and self.timer["tool_switch"].active == False:
            self.cycleThroughTool()

        # seed
        # =====
        # left CTRL.... use seed
        # e.... change selected seed
        if keys[pygame.K_LCTRL]:
            self.startTimer(timerType = "seed_use")
        if keys[pygame.K_e] and self.timer["seed_switch"].active == False:
            self.cycleThroughSeeds()

        # intearaction (sleep)
        # ====================
        # when enter is pressed when at bed, sleep
        if keys[pygame.K_RETURN]:
            collided_interaction_sprite = pygame.sprite.spritecollide(self,self.action,False)

            if collided_interaction_sprite:
                self.sleep = True
                self.characterDisplayType = self.randomSleepIdle()

    def useTool(self):
        def useWater(self):
            self.soilLayer.water(targetPos)
            self.watering.play()
        
        targetPos = self.posRect.center + constants.PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

        # function map of tools and corresponding responses
        toolActions = {
        'hoe': self.soilLayer.tillSoil(targetPos),
        'axe': self.damage_tree(targetPos),
        'water': useWater()
        }

        # get tool, execute corresponding action
        currTool = self.tools[self.iTools]
        if currTool in toolActions:
            toolActions[currTool]()
        
    def useSeed(self):
        targetPos = self.posRect.center + constants.PLAYER_TOOL_OFFSET[self.characterDisplayType.split('_')[0]]
        
        # get selected seed and plant it
        selectedSeed = self.seeds[self.iSeeds]
        if self.seedInventory[selectedSeed] > 0:
            self.soilLayer.plantSeed(targetPos, selectedSeed)

            # remove one seed from inventory
            self.seedInventory[selectedSeed] -= 1

    def hitTree(self, targetPos): 
        # irrelevent, but I once knew a guy who broke his hand while hitting a tree (he did it bc he saw someone in an anime do it and thought it was cool)
        for tree in self.treeSprite.sprites():
            if tree.rect.collidepoint(targetPos):
                tree.damage()

    # MOVEMENT
    def collision(self, direction):
        for sprite in self.collisionSprites.sprites():
            # getting errors when hit box not found.... make try catch
            try:
                # access hit box
                hitbox = sprite.hitbox
            except AttributeError:
                # if hitbox not found, skip to next sprite
                continue
            
            # check for collision
            # to stop collisions from occuring if player hit box overlaps with another hit box
            # then move the player hit box to the opposite direction of movement to prevent overlap
            if hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # if hit while moving right
                        self.hitbox.right = hitbox.left # move hit box to left (to stop overlap)
                    if self.direction.x < 0:  # player moving left
                        self.hitbox.left = hitbox.right # move hit box right
                    self.posRect.centerx = self.hitbox.centerx 
                    self.playerPos.x = self.hitbox.centerx

                if direction == 'vertical':
                    if self.direction.y > 0:  # player move down
                        self.hitbox.bottom = hitbox.top
                    if self.direction.y < 0:  # move up
                        self.hitbox.top = hitbox.bottom
                    self.posRect.centery = self.hitbox.centery
                    self.playerPos.y = self.hitbox.centery

    def updatePosition(self, axis):
        # upate the player pos (posRect), and hit box, if collision going to happpen, then don't allow overal
        if axis == "x":
            self.hitbox.centerx = int(self.playerPos.x) # make sure not a floating point val
            self.posRect.centerx = self.hitbox.centerx
            self.collision("horizontal")
        elif axis == "y":
            self.hitbox.centery = int(self.playerPos.y)
            self.posRect.centery = self.hitbox.centery
            self.collision("vertical")

    def move(self, time):
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # move horizontally
        self.playerPos.x += self.direction.x * self.speed * time
        self.updatePosition('x')

        # move vertically
        self.playerPos.y += self.direction.y * self.speed * time
        self.updatePosition('y')

    # ANIMATION
    def animate(self, time):
        self.iGraphicFrame += 5 * time

        # once it reaches the last img in animation group, loop back to front
        if self.iGraphicFrame >= len(self.animations[self.characterDisplayType]):
            self.iGraphicFrame = 0

        self.characterGraphic = self.animations[self.characterDisplayType][int(self.iGraphicFrame)]

    def update(self, time):
        self.keyboardInput()
        self.move(time)
        self.animate
        
        self.updateTimer()
