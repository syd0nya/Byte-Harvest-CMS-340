import pygame
import constants as c
from timer_game import Timer

class Menue:
    def __init__ (self, player, toggle_menue):
        self.player = player
        self.toggle_menue = toggle_menue
        self.dispay_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(font = "../font/LycheeSoda.ttf", size = 30)

        # formatting 
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        #print(self.options)
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # mmvment
        self.index = 0
        self.timer = Timer(200)

    def setup(self):
        # text surface
        self.text_surf = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(string = item, 
                                        AA = False, 
                                        color = "Black")
            self.text_surf.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
        
        self.total_height += (len(self.text_surf) - 1) * self.space
        self.menue_top = c.SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(
            l = c.SCREEN_HEIGHT / 2 - self.total_height / 2,
            t = self.menue_top,
            w = self.width,
            h = self.total_height
        )

    def input(self):
        # get input --> esc = close shop menue 
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menue()

        # navigate menue
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

        # make sure movemnt of selected item on menue dosnt go out of bounds
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index < len(self.options) - 1:
            self.inxex = 0

    def display_money(self):
        text_surf = self.font.render(string = f"${self.player.money}",
                                     AA = False, 
                                     color = "Black")
        text_rect = text_surf.get_rect(midbottom = (c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, "White", text_rect.inflate(10,10),0,6)
        self.display_surface.blit(text_surf, text_rect)

    def show_entry(self, text_surf, ammount, top, selected):
        #background
        bg_rect = pygame.Rect(
            l = self.main_rect.left,
            t = top,
            w = self.width,
            h = text_surf.get_height() + self.padding * 2
        )
        pygame.draw.rect(self.dispay_surface, "White", bg_rect, 0 ,4 )
        
        #text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery ))
        self.display_surface.blit(text_surf, text_rect)

        #ammount 
        ammount_surf = self.font.render(text = str(ammount),
                                        AA = False,
                                        color = "Black" )
        ammount_rect = ammount_surf.get_rect(midright = (self.main_rect.right - 20 , bg_rect.centery))
        self.display_surface.blit(ammount_surf, ammount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.dispay_surface, "Black", bg_rect, 4, 4)

    def update(self):
        self.input()
        self.display_money()
        # pygame.draw.rect(self.dispay_surface, "red", self.main_rect)
        #self.display_surface.blit(pygame.Surface((1000,1000), (0,0)))
        for text_index, text_surf in enumerate(self.text_surf):
           top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
           ammount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
           ammount = ammount_list[text_index]
           self.show_entry(text_surf, ammount, top, self.index == text_index)
           
           #self.dispay_surface.blit(text_surf, (100, text_index * 50))