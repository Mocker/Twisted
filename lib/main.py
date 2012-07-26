'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
try:
	import sys
	import random
	import math
	import os
	import getopt
	import pygame
	import time
	import data
	from xml.sax import *
	from xml.sax import saxutils
	from xml.sax.handler import feature_namespaces
	from pygame.locals import *
	from pygame import *
	import titleController
	import gameController
	import player

except ImportError, err:
    print "couldn't load module %s" % (err)
    sys.exit(2)

reload(data)
reload(titleController)
reload(gameController)
reload(player)
	
MAP_H = 10000
MAP_W = 10000
SCREEN_W = 1024
SCREEN_H = 768
GAME_TITLE = "BIZNESS TIME"

def main():
	random.seed(None)
	global pygame

	print "Hello from your game'aaaaa main()"
	pygame.mixer.init()
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
	pygame.display.flip()
	GAME_ENGINE = gEngine(screen)
	
	GAME_ENGINE.run() #start main game loop
	
	
	
	
	
	
	
	
class gEngine:
	#main game engine
	#contains game loop, player info, settings
	#passes ingame details to map object
	global SCREEN_W
	global SCREEN_H
	global MAP_H
	global MAP_W
	global GAME_TITLE
	global background
	state = "title"
	#font = pygame.font.Font(data.filepath("visitor1.ttf"), 24)
	
	def __init__(self, screeen):
		#initialize game engine, pygame surfaces etc
		self.screen = screeen
		self.background = pygame.Surface([SCREEN_W,SCREEN_H])
		self.background = self.background.convert()
		bgimg = pygame.image.load(data.filepath("titleish.jpg"))
		self.screen.blit(bgimg, (0,0))
		pygame.display.flip()
		self.clock = pygame.time.Clock()
		pygame.display.set_caption(GAME_TITLE)
		pygame.mouse.set_visible(1)
		GAME_STATE = "title"
		self.controller = titleController.titleController(self.screen)
		
	def run(self):
		#do game loop
		GAME_STATE = "title"
		GAME_SELECTION = "none"
		while(GAME_STATE != "quit"):
			self.clock.tick(60)
			#get input
			for event in pygame.event.get():
				if event.type == QUIT:
					GAME_STATE = "quit"
				elif event.type == KEYDOWN and event.key == K_ESCAPE and GAME_STATE != "title":
					GAME_STATE = "title"
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					GAME_STATE = "quit"
				elif event.type == KEYDOWN :
					tmpres = self.controller.parseKeyDown(event.key, GAME_STATE, GAME_SELECTION)
					GAME_SELECTION = tmpres[1]
					GAME_STATE = tmpres[0]
				elif event.type == KEYUP:
					GAME_STATE = self.controller.parseKeyUp(event.key, GAME_STATE)
			#change controller if needed
			if GAME_STATE == "game" and self.controller.function() != "game":
				self.controller = gameController.gameController(self.screen, GAME_SELECTION)
			if GAME_STATE == "title" and self.controller.function() != "title":
				self.controller = titleController.titleController(self.screen)
				
			#update the current controller
			self.controller.update()
			if GAME_STATE == "game" and self.controller.level_status == "exit":
				GAME_STATE = "title"

			#render the current controller
			self.background.fill((0,0,0))
			self.screen.blit(self.background, (0,0))
			self.controller.render(self.screen)
			#flip display
			pygame.display.flip()	
		
