# Class to present the menu to the user for trading

# Imports
import pygame
from constants import *
from timer_byte import Timer
from pomodoroTimer import Pomodoro

class Menu:
    def __init__(self, player, toggle_menu, farmScreen):
        # Constructor
        # Initialize the player
        self.player = player

        # Initialize the toggle_menu function
        self.toggle_menu = toggle_menu

        # Get the display surface
        self.farmScreen = farmScreen

        # Get the font
        self.font = pygame.font.SysFont('couriernew', 26)

        # Set the spacing constants (to be used later with the menu options)
        self.padding = 30

        # Get the menu options
        self.menu_options = []

        # Get the sell options from the user's inventory
        self.menu_options += self.player.item_inventory.keys()
        self.num_sellable = self.menu_options.__len__() # Used later for index reference

        # Get the buy options from the settings' seed list
        self.menu_options += PURCHASE_PRICES.keys()

        # Call the setup method 
        self.setup()

        # Start the selector at the top of the list
        self.selectorIndex = 0

        # Make a timer to facilitate delay between user clicks
        self.timer = Timer(200)

    def instructions(self):
        s = "How to trade: "
        trade_text = self.font.render(s, True, 'black', 'white')
        trade_text_rect = trade_text.get_rect()
        trade_text_rect.left = 2 * SCREEN_WIDTH // 3
        trade_text_rect.top = FARM_HEIGHT // 6 - 15

        self.farmScreen.blit(trade_text, trade_text_rect)

        infoLines = []
        infoLines.append("Scroll along the menu")
        infoLines.append("using the up and down")
        infoLines.append("keys on your keyboard")
        infoLines.append(" ")
        infoLines.append("To select an option, ")
        infoLines.append("press the enter key")
        infoLines.append(" ")
        infoLines.append("Your current inventory")
        infoLines.append("is shown to the left")

        h = 1
        for line in infoLines:
            self.printLines(line, h)
            h += 1

    def printLines(self, s, height):
        trade_text = self.font.render(s, True, 'black', 'white')
        trade_text_rect = trade_text.get_rect()
        trade_text_rect.left = 2 * SCREEN_WIDTH // 3
        trade_text_rect.top = FARM_HEIGHT // 6 + (height * 35) - 10

        self.farmScreen.blit(trade_text, trade_text_rect)

    def display_money(self):
        # Display the user's money
        s = "Money: " + str(self.player.money)
        userMoney = self.font.render(s, True, 'black', 'white')
        userMoney_rect = userMoney.get_rect()
        userMoney_rect.center = (SCREEN_WIDTH // 2, FARM_HEIGHT - 50)

        self.farmScreen.blit(userMoney, userMoney_rect)

    def display_inventory(self):
        # Display the user's inventory and update as they buy
        left = SCREEN_WIDTH // 5

        # Draw the background for the inventory display
        pygame.draw.rect(self.farmScreen, 'white', pygame.Rect(left - 70, FARM_HEIGHT // 7, 250, 300))
        pygame.draw.rect(self.farmScreen, 'blue', pygame.Rect(left - 70, FARM_HEIGHT // 7, 250, 300), 2)

        counter = 0
        # Draw the item header
        inven_text = self.font.render('Items: ', True, 'black', 'white')
        inven_text_rect = inven_text.get_rect()
        inven_text_rect.left = left - 50
        inven_text_rect.top = FARM_HEIGHT // 6
        self.farmScreen.blit(inven_text, inven_text_rect)

        # Draw the items in inventory
        for i in self.player.item_inventory:
            s = i + ": " + str(self.player.item_inventory[i])
            inven_text = self.font.render(s, True, 'black', 'white')
            inven_text_rect = inven_text.get_rect()
            inven_text_rect.left = left
            inven_text_rect.top = FARM_HEIGHT // 4 + (30 * counter)
            
            # Draw the item
            self.farmScreen.blit(inven_text, inven_text_rect)
            counter += 1

        # Draw the seed header
        counter = 1
        seed_text = self.font.render('Seeds: ', True, 'black', 'white')
        seed_text_rect = seed_text.get_rect()
        seed_text_rect.left = left - 50
        seed_text_rect.top = FARM_HEIGHT // 2 + 20
        self.farmScreen.blit(seed_text, seed_text_rect)

        # Draw the items in seed inventory
        for i in self.player.seed_inventory:
            s = i + ": " + str(self.player.seed_inventory[i])
            inven_text = self.font.render(s, True, 'black', 'white')
            inven_text_rect = inven_text.get_rect()
            inven_text_rect.left = left
            inven_text_rect.top = FARM_HEIGHT // 2 + 20 + (30 * counter)
            
            # Draw the item
            self.farmScreen.blit(inven_text, inven_text_rect)
            counter += 1

    def setup(self):
        # Set up the display area for the menu
        # Mathematical set up for menu area (where is the top/bottom option)
        # Budget 50px height for each option, 20px padding on both sides
        self.menu_height = (50 * self.menu_options.__len__()) + (self.padding * (self.menu_options.__len__() + 1))

        self.menu_top = FARM_HEIGHT * 0.75 # Center of farm screen
        self.menu_top -= self.menu_height // 2 # Place menu centered horizontally   

        # Make each of the text surfaces 
        self.option_texts = []
        self.option_rects = []
        j = 0
        for i in self.menu_options:
            # Make the text surface
            # Get the name of the item
            optionString = " " + i
            optionString = optionString.ljust(27)

            # Get the amount for the item
            # If it's a sellable item, get the sell price
            if j < self.num_sellable:
                amount = SALE_PRICES[self.menu_options[j]]
            # If it's a buyable item, get the buy price
            else:
                amount = PURCHASE_PRICES[self.menu_options[j]]

            optionString += str(amount)
            optionString = optionString.ljust(30)

            # Render the actual string
            self.text = self.font.render(optionString, True, 'black', 'white')

            # Make the text rectangle
            self.textRect = self.text.get_rect()
            self.textRect.center = (SCREEN_WIDTH/2, self.menu_top + (j * (self.padding + 20))) # Space for padding and individual options

            # Add the surface and rectangle into the arrays
            self.option_texts.append(self.text)
            self.option_rects.append(self.textRect)

            # Up the counter
            j += 1

    def input(self):
        # Get the user's input for menu interaction
        # Get a list of all the keys pressed
        pressed = pygame.key.get_pressed()

        # Update the timer
        self.timer.update()

        # Did the user exit the menu
        if pressed[pygame.K_ESCAPE]:
            self.toggle_menu()
            print("esc pressed")

        # If the timer's not activated yet
        if not self.timer.active:
            # Activate the timer so only the first click is registered
            # Did the user click up
            if pressed[pygame.K_UP]:
                self.selectorIndex -= 1
                self.timer.activate()

            # Did the user click down
            elif pressed[pygame.K_DOWN]:
                self.selectorIndex += 1
                self.timer.activate()

            # Did the user click space
            elif pressed[pygame.K_RETURN]:
                self.timer.activate()
                item = self.menu_options[self.selectorIndex]
                # Were they selling or buy
                if self.selectorIndex < self.num_sellable:
                    # Make sure the user has the item
                    if self.player.item_inventory[item] >= 1:
                        # Selling, decrease inventory
                        self.player.item_inventory[item] -= 1

                        # Increase money
                        self.player.money += SALE_PRICES[item]
            
                else:
                    # Make sure the user has the money
                    if self.player.money >= PURCHASE_PRICES[item]:
                        # Buying, increase inventory
                        self.player.seed_inventory[item] += 1

                        # Decrease money
                        self.player.money -= PURCHASE_PRICES[item]

        # Make sure the index is within bounds
        if self.selectorIndex >= self.menu_options.__len__():
            self.selectorIndex = 0
        elif self.selectorIndex < 0:
            self.selectorIndex = self.menu_options.__len__() - 1

    def show_entry(self):
        # Render each entry within the main menu space
        for k in range(self.menu_options.__len__()):
            # Display the text options
            self.farmScreen.blit(self.option_texts[k], self.option_rects[k])

            # If this option is selected
            if self.selectorIndex == k:
                # Draw black box around this option
                border_rect = pygame.Rect(0, 0, 480, 35)
                border_rect.center = (SCREEN_WIDTH/2, self.menu_top + (k * (self.padding + 20)))

                pygame.draw.rect(self.farmScreen, 'black', border_rect, 3)

                buysell_font = pygame.font.SysFont('couriernew', 22)

                # If it's a sell option
                if k < self.num_sellable:
                    # Set sell
                    buysell_string = "SELL"
                else:
                    # Set buy
                    buysell_string = "BUY"

                buysell_text = buysell_font.render(buysell_string, True, 'black', None)
                buysell_rect = buysell_text.get_rect()
                buysell_rect.center = border_rect.center

                # Draw the buy/sell
                self.farmScreen.blit(buysell_text, buysell_rect)

    def update(self):
        # Update the shop by calling other methods
        # Draw the background for the menu
        backgroundRect = pygame.Rect(0, 0, 3*SCREEN_WIDTH // 4, FARM_HEIGHT - 50)
        backgroundRect.center = (SCREEN_WIDTH // 2, FARM_HEIGHT // 2)
        pygame.draw.rect(self.farmScreen, 'white', backgroundRect)
        pygame.draw.rect(self.farmScreen, 'black', backgroundRect, 2)

        # Print the instructions
        self.instructions()

        # Check for user input
        self.input()

        # Display the user's money
        self.display_money()

        # Display the user's inventory
        self.display_inventory()

        # Draw each of the options
        self.show_entry()