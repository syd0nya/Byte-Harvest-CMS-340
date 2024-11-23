import pygame, sys
from settings import *
from level import Level		# Class to run the farm game
from editor import Editor	# Class to run the text editor


class Game:
	def __init__(self):
		# Initialize pygame to run
		pygame.init()

		# Screen settings
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # Total screen
		self.farmScreen = pygame.Surface((SCREEN_WIDTH,FARM_HEIGHT)) # Farm surface
		pygame.display.set_caption('Sprout land')

		# Clock settings
		self.clock = pygame.time.Clock()

		# Make the two main objects
		self.level = Level(self.farmScreen) # Grab the farmScreen
		self.editors = []

		# Make the first line of text
		self.editor1 = Editor()
		self.editors.append(self.editor1)
		self.i = 0


	def run(self):
		while True:
			for event in pygame.event.get(pygame.QUIT):
				# Close game after quit
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
  
			# Get the timechange
			dt = self.clock.tick() / 1000

			# Does the text editor need to go to another line?
			if self.editors[-1].userInput.__len__() == 60:
				self.i += 1
				self.editors.append(Editor())
				self.editors[self.i].textRect.center = (SCREEN_WIDTH/2 - 360, SCREEN_HEIGHT/5 + (30*self.i))
				self.editors[self.i].pageOffset = 50 * self.i

			# Update the latest line
			self.editors[-1].run()

			# Refresh all lines
			for editor in self.editors:
				editor.display()

			# Refresh the level (after the text editor so it appears on top)
			self.level.run(dt)
			self.screen.blit(self.farmScreen, (0, (SCREEN_HEIGHT - FARM_HEIGHT))) # Draw the level onto the display screen

			# Update the screen
			pygame.display.update()

if __name__ == '__main__':
	# Make a new game
	game = Game()
	game.run()