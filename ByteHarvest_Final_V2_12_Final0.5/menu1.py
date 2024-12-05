# # Class to present the menu to the user for trading

# # Imports
# import pygame
# from constants import *
# from timer_byte import Timer
# from pomodoroTimer import Pomodoro

# class Menu:
#     def __init__(self, player, toggle_menu, farmScreen):
#         # Constructor
#         # Initialize the player
#         self.player = player

#         # Initialize the toggle_menu function
#         self.toggle_menu = toggle_menu

#         # Get the display surface
#         self.farmScreen = farmScreen

#         # Get the font
#         self.font = pygame.font.SysFont('couriernew', 26)

#         # Set the spacing constants (to be used later with the menu options)
#         self.padding = 30

#         # Get the menu options
#         self.menu_options = []

#         # Get the sell options from the user's inventory
#         self.menu_options += self.player.item_inventory.keys()
#         self.num_sellable = self.menu_options.__len__() # Used later for index reference

#         # Get the buy options from the settings' seed list
#         self.menu_options += PURCHASE_PRICES.keys()

#         # Call the setup method 
#         self.setup()

#         # Start the selector at the top of the list
#         self.selectorIndex = 0

#         # Make a timer to facilitate delay between user clicks
#         self.timer = Timer(200)

#     def instructions(self):
#         s = "How to trade: "
#         trade_text = self.font.render(s, True, 'black', 'white')
#         trade_text_rect = trade_text.get_rect()
#         trade_text_rect.left = 2 * SCREEN_WIDTH // 3
#         trade_text_rect.top = FARM_HEIGHT // 6 - 15

#         self.farmScreen.blit(trade_text, trade_text_rect)

#         infoLines = []
#         infoLines.append("Scroll along the menu")
#         infoLines.append("using the up and down")
#         infoLines.append("keys on your keyboard")
#         infoLines.append(" ")
#         infoLines.append("To select an option, ")
#         infoLines.append("press the enter key")
#         infoLines.append(" ")
#         infoLines.append("Your current inventory")
#         infoLines.append("is shown to the left")

#         h = 1
#         for line in infoLines:
#             self.printLines(line, h)
#             h += 1

#     def printLines(self, s, height):
#         trade_text = self.font.render(s, True, 'black', 'white')
#         trade_text_rect = trade_text.get_rect()
#         trade_text_rect.left = 2 * SCREEN_WIDTH // 3
#         trade_text_rect.top = FARM_HEIGHT // 6 + (height * 35) - 10

#         self.farmScreen.blit(trade_text, trade_text_rect)

#     def display_money(self):
#         # Display the user's money
#         s = "Money: " + str(self.player.money)
#         userMoney = self.font.render(s, True, 'black', 'white')
#         userMoney_rect = userMoney.get_rect()
#         userMoney_rect.center = (SCREEN_WIDTH // 2, FARM_HEIGHT - 50)

#         self.farmScreen.blit(userMoney, userMoney_rect)

#     def display_inventory(self):
#         # Display the user's inventory and update as they buy
#         left = SCREEN_WIDTH // 5

#         # Draw the background for the inventory display
#         pygame.draw.rect(self.farmScreen, 'white', pygame.Rect(left - 70, FARM_HEIGHT // 7, 250, 300))
#         pygame.draw.rect(self.farmScreen, 'blue', pygame.Rect(left - 70, FARM_HEIGHT // 7, 250, 300), 2)

#         counter = 0
#         # Draw the item header
#         inven_text = self.font.render('Items: ', True, 'black', 'white')
#         inven_text_rect = inven_text.get_rect()
#         inven_text_rect.left = left - 50
#         inven_text_rect.top = FARM_HEIGHT // 6
#         self.farmScreen.blit(inven_text, inven_text_rect)

#         # Draw the items in inventory
#         for i in self.player.item_inventory:
#             s = i + ": " + str(self.player.item_inventory[i])
#             inven_text = self.font.render(s, True, 'black', 'white')
#             inven_text_rect = inven_text.get_rect()
#             inven_text_rect.left = left
#             inven_text_rect.top = FARM_HEIGHT // 4 + (30 * counter)
            
#             # Draw the item
#             self.farmScreen.blit(inven_text, inven_text_rect)
#             counter += 1

#         # Draw the seed header
#         counter = 1
#         seed_text = self.font.render('Seeds: ', True, 'black', 'white')
#         seed_text_rect = seed_text.get_rect()
#         seed_text_rect.left = left - 50
#         seed_text_rect.top = FARM_HEIGHT // 2 + 20
#         self.farmScreen.blit(seed_text, seed_text_rect)

#         # Draw the items in seed inventory
#         for i in self.player.seed_inventory:
#             s = i + ": " + str(self.player.seed_inventory[i])
#             inven_text = self.font.render(s, True, 'black', 'white')
#             inven_text_rect = inven_text.get_rect()
#             inven_text_rect.left = left
#             inven_text_rect.top = FARM_HEIGHT // 2 + 20 + (30 * counter)
            
#             # Draw the item
#             self.farmScreen.blit(inven_text, inven_text_rect)
#             counter += 1

#     def setup(self):
#         # Set up the display area for the menu
#         # Mathematical set up for menu area (where is the top/bottom option)
#         # Budget 50px height for each option, 20px padding on both sides
#         self.menu_height = (50 * self.menu_options.__len__()) + (self.padding * (self.menu_options.__len__() + 1))

#         self.menu_top = FARM_HEIGHT * 0.75 # Center of farm screen
#         self.menu_top -= self.menu_height // 2 # Place menu centered horizontally   

#         # Make each of the text surfaces 
#         self.option_texts = []
#         self.option_rects = []
#         j = 0
#         for i in self.menu_options:
#             # Make the text surface
#             # Get the name of the item
#             optionString = " " + i
#             optionString = optionString.ljust(27)

#             # Get the amount for the item
#             # If it's a sellable item, get the sell price
#             if j < self.num_sellable:
#                 amount = SALE_PRICES[self.menu_options[j]]
#             # If it's a buyable item, get the buy price
#             else:
#                 amount = PURCHASE_PRICES[self.menu_options[j]]

#             optionString += str(amount)
#             optionString = optionString.ljust(30)

#             # Render the actual string
#             self.text = self.font.render(optionString, True, 'black', 'white')

#             # Make the text rectangle
#             self.textRect = self.text.get_rect()
#             self.textRect.center = (SCREEN_WIDTH/2, self.menu_top + (j * (self.padding + 20))) # Space for padding and individual options

#             # Add the surface and rectangle into the arrays
#             self.option_texts.append(self.text)
#             self.option_rects.append(self.textRect)

#             # Up the counter
#             j += 1

#     def input(self):
#         # Get the user's input for menu interaction
#         # Get a list of all the keys pressed
#         pressed = pygame.key.get_pressed()

#         # Update the timer
#         self.timer.update()

#         # Did the user exit the menu
#         if pressed[pygame.K_ESCAPE]:
#             self.toggle_menu()
#             print("esc pressed")

#         # If the timer's not activated yet
#         if not self.timer.active:
#             # Activate the timer so only the first click is registered
#             # Did the user click up
#             if pressed[pygame.K_UP]:
#                 self.selectorIndex -= 1
#                 self.timer.activate()

#             # Did the user click down
#             elif pressed[pygame.K_DOWN]:
#                 self.selectorIndex += 1
#                 self.timer.activate()

#             # Did the user click space
#             elif pressed[pygame.K_RETURN]:
#                 self.timer.activate()
#                 item = self.menu_options[self.selectorIndex]
#                 # Were they selling or buy
#                 if self.selectorIndex < self.num_sellable:
#                     # Make sure the user has the item
#                     if self.player.item_inventory[item] >= 1:
#                         # Selling, decrease inventory
#                         self.player.item_inventory[item] -= 1

#                         # Increase money
#                         self.player.money += SALE_PRICES[item]
            
#                 else:
#                     # Make sure the user has the money
#                     if self.player.money >= PURCHASE_PRICES[item]:
#                         # Buying, increase inventory
#                         self.player.seed_inventory[item] += 1

#                         # Decrease money
#                         self.player.money -= PURCHASE_PRICES[item]

#         # Make sure the index is within bounds
#         if self.selectorIndex >= self.menu_options.__len__():
#             self.selectorIndex = 0
#         elif self.selectorIndex < 0:
#             self.selectorIndex = self.menu_options.__len__() - 1

#     def show_entry(self):
#         # Render each entry within the main menu space
#         for k in range(self.menu_options.__len__()):
#             # Display the text options
#             self.farmScreen.blit(self.option_texts[k], self.option_rects[k])

#             # If this option is selected
#             if self.selectorIndex == k:
#                 # Draw black box around this option
#                 border_rect = pygame.Rect(0, 0, 480, 35)
#                 border_rect.center = (SCREEN_WIDTH/2, self.menu_top + (k * (self.padding + 20)))

#                 pygame.draw.rect(self.farmScreen, 'black', border_rect, 3)

#                 buysell_font = pygame.font.SysFont('couriernew', 22)

#                 # If it's a sell option
#                 if k < self.num_sellable:
#                     # Set sell
#                     buysell_string = "SELL"
#                 else:
#                     # Set buy
#                     buysell_string = "BUY"

#                 buysell_text = buysell_font.render(buysell_string, True, 'black', None)
#                 buysell_rect = buysell_text.get_rect()
#                 buysell_rect.center = border_rect.center

#                 # Draw the buy/sell
#                 self.farmScreen.blit(buysell_text, buysell_rect)

#     def update(self):
#         # Update the shop by calling other methods
#         # Draw the background for the menu
#         backgroundRect = pygame.Rect(0, 0, 3*SCREEN_WIDTH // 4, FARM_HEIGHT - 50)
#         backgroundRect.center = (SCREEN_WIDTH // 2, FARM_HEIGHT // 2)
#         pygame.draw.rect(self.farmScreen, 'white', backgroundRect)
#         pygame.draw.rect(self.farmScreen, 'black', backgroundRect, 2)

#         # Print the instructions
#         self.instructions()

#         # Check for user input
#         self.input()

#         # Display the user's money
#         self.display_money()

#         # Display the user's inventory
#         self.display_inventory()

#         # Draw each of the options
#         self.show_entry()
import pygame
from constants import *
from timer_byte import Timer

class Menu:
    def __init__(self, player, toggle_menu, farm_screen):
        # Basic setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.farm_screen = farm_screen
        self.font = pygame.font.SysFont('couriernew', 26)
        
        # Menu spacing
        self.padding = 30
        
        # Menu options from player inventory and shop items
        self.menu_options = []
        self.menu_options += list(self.player.item_inventory.keys())
        self.num_sellable = len(self.menu_options)  # Track number of sellable items
        self.menu_options += PURCHASE_PRICES.keys()
        
        # Complete setup
        self.setup()
        
        # Selection management
        self.selector_index = 0
        self.timer = Timer(200)  # Timer for input delay

    def setup(self):
        # Calculate menu dimensions
        self.menu_height = (50 * len(self.menu_options)) + (self.padding * (len(self.menu_options) + 1))
        self.menu_top = FARM_HEIGHT * 0.75
        self.menu_top -= self.menu_height // 2

        # Create text surfaces and rectangles for menu options
        self.option_texts = []
        self.option_rects = []
        
        for i, option in enumerate(self.menu_options):
            # Format option string
            option_string = f" {option}".ljust(27)
            
            # Add price
            if i < self.num_sellable:
                amount = SALE_PRICES[option]
            else:
                amount = PURCHASE_PRICES[option]
            option_string += str(amount).ljust(3)

            # Create text surface
            text = self.font.render(option_string, True, 'black', 'white')
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH/2, self.menu_top + (i * (self.padding + 20)))

            self.option_texts.append(text)
            self.option_rects.append(text_rect)

    def display_money(self):
        text = f"Money: {self.player.money}"
        money_surf = self.font.render(text, True, 'black', 'white')
        money_rect = money_surf.get_rect(center=(SCREEN_WIDTH // 2, FARM_HEIGHT - 50))
        self.farm_screen.blit(money_surf, money_rect)

    def display_inventory(self):
        # Background for inventory
        left = SCREEN_WIDTH // 5
        inventory_bg = pygame.Rect(left - 70, FARM_HEIGHT // 7, 250, 300)
        pygame.draw.rect(self.farm_screen, 'white', inventory_bg)
        pygame.draw.rect(self.farm_screen, 'blue', inventory_bg, 2)

        # Items header
        header_text = self.font.render('Items: ', True, 'black', 'white')
        header_rect = header_text.get_rect(left=left - 50, top=FARM_HEIGHT // 6)
        self.farm_screen.blit(header_text, header_rect)

        # Display items
        for i, (item, count) in enumerate(self.player.item_inventory.items()):
            text = f"{item}: {count}"
            item_surf = self.font.render(text, True, 'black', 'white')
            item_rect = item_surf.get_rect(left=left, top=FARM_HEIGHT // 4 + (30 * i))
            self.farm_screen.blit(item_surf, item_rect)

        # Seeds header
        seed_header = self.font.render('Seeds: ', True, 'black', 'white')
        seed_header_rect = seed_header.get_rect(left=left - 50, top=FARM_HEIGHT // 2 + 20)
        self.farm_screen.blit(seed_header, seed_header_rect)

        # Display seeds
        for i, (seed, count) in enumerate(self.player.seed_inventory.items(), 1):
            text = f"{seed}: {count}"
            seed_surf = self.font.render(text, True, 'black', 'white')
            seed_rect = seed_surf.get_rect(left=left, top=FARM_HEIGHT // 2 + 20 + (30 * i))
            self.farm_screen.blit(seed_surf, seed_rect)

    def show_entry(self):
        for i, (text, rect) in enumerate(zip(self.option_texts, self.option_rects)):
            # Display menu option
            self.farm_screen.blit(text, rect)
            
            # Highlight selected option
            if self.selector_index == i:
                border_rect = pygame.Rect(0, 0, 480, 35)
                border_rect.center = (SCREEN_WIDTH/2, self.menu_top + (i * (self.padding + 20)))
                pygame.draw.rect(self.farm_screen, 'black', border_rect, 3)

                # Show BUY/SELL text
                action_font = pygame.font.SysFont('couriernew', 22)
                action_text = "SELL" if i < self.num_sellable else "BUY"
                action_surf = action_font.render(action_text, True, 'black')
                action_rect = action_surf.get_rect(center=border_rect.center)
                self.farm_screen.blit(action_surf, action_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.selector_index = (self.selector_index - 1) % len(self.menu_options)
                self.timer.activate()
            elif keys[pygame.K_DOWN]:
                self.selector_index = (self.selector_index + 1) % len(self.menu_options)
                self.timer.activate()
            elif keys[pygame.K_RETURN]:
                self.timer.activate()
                
                # Get selected item
                item = self.menu_options[self.selector_index]
                
                # Handle selling
                if self.selector_index < self.num_sellable:
                    if self.player.item_inventory[item] >= 1:
                        self.player.item_inventory[item] -= 1
                        self.player.money += SALE_PRICES[item]
                # Handle buying
                else:
                    if self.player.money >= PURCHASE_PRICES[item]:
                        self.player.seed_inventory[item] += 1
                        self.player.money -= PURCHASE_PRICES[item]

    def update(self):
        # Draw menu background
        menu_bg = pygame.Rect(0, 0, 3*SCREEN_WIDTH // 4, FARM_HEIGHT - 50)
        menu_bg.center = (SCREEN_WIDTH // 2, FARM_HEIGHT // 2)
        pygame.draw.rect(self.farm_screen, 'white', menu_bg)
        pygame.draw.rect(self.farm_screen, 'black', menu_bg, 2)

        self.input()
        self.display_money()
        self.display_inventory()
        self.show_entry()