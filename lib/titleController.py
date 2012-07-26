#!/usr/bin/python
'''Controller for all events on the title screen. Should be made to inherit a generic controller class

right now just sits there and waits for exit
'''

import os
import data
import pygame
from pygame import *
from pygame.image import *
from pygame.locals import *

reload(data)

class titleController:
	#controls the title screen
	
	def __init__(self, screeen):
		self.screen = screeen #point to main display object, though it should be passed to the render function
		self.title_bg = pygame.image.load(data.filepath("titleish.jpg"))
		self.font = pygame.font.Font(data.filepath("visitor1.ttf"), 24)
		self.selected = "start"
		self.text_start = "Get Down to Business"
		self.text_level = "test 1"
		self.text_exit = "Bizness Time is Over"
		self.level_list = self.getlevels()
		self.level_index = 0
		
	
	def function(self):
		return "title"

	def parseKeyDown(self, ekey, gamestate, game_selection):
		#do something on keypress
		if ekey == 32: #pressed space - start game
			print "space key pressed"
			if self.selected == "start":
				return ["game","superawesomemap"]
			elif self.selected == "level":
					game_selection = self.level_list[self.level_index]
					return ["game", game_selection]
			else:
				return ["quit",None]
					
		elif ekey == 275: #right arrow
			if self.selected == "level":
				if self.level_index >= len(self.level_list) - 1:
					self.level_index = 0
				else:
					self.level_index += 1
				
		elif ekey == 273:
			#pressed down
			if self.selected == "start":
				print "switching to exit"
				self.selected = "exit"
			elif self.selected == "exit":
				print "switching to level"
				self.selected = "level"
			else :
				print "self.selected = "+self.selected
				self.selected = "start"
		elif ekey == 274: #u[ array?
			if self.selected == "start":
				#print "switching to exit"
				self.selected = "level"
			elif self.selected == "exit":
				#print "switching to level"
				self.selected = "start"
			else :
				#print "self.selected = "+self.selected
				self.selected = "exit"
		else:
			print "Key pressed "+str(ekey)
			return ["title","none"]
		return ["title","none"]
	
	def parseKeyUp(self, ekey, gamestate):
		#do something on keyup
		print "key was released - "+ str(ekey)
		return "title"
		
	def update(self):
		#update data for each tick
		#nothing here since it is a static title screen
		self.blar = 2

	def render(self, escreen):
		#render data onto display surface
		escreen.blit(self.title_bg, (0,0))
		tmptext = self.font.render(self.text_start,1,(250,250,250))
		escreen.blit(tmptext, [600, 400])
		tmptext = self.font.render("< " + self.level_list[self.level_index]+" >",1,(250,250,250))
		escreen.blit(tmptext, [600, 450])
		tmptext = self.font.render(self.text_exit,1,(250,250,250))
		escreen.blit(tmptext, [600, 500])
		tmptext = self.font.render("8==D",1,(255,255,255))
		if self.selected == "start":
			tmpy = 400
		if self.selected == "level":
			tmpy = 450
		if self.selected == "exit":
			tmpy = 500
		#print "self selectes ISSSS "+self.selected
		escreen.blit(tmptext, [520, tmpy])
		
	def getlevels(self):
		rawlist = os.listdir(data.filepath("levels"))
		reallist = []
		if len(rawlist) > 10:
			print "Too many entries in rawlist"
			return None
		#else:
		#	print "rawlist is this big: "+str(len(rawlist))
		#	print "first elemenet is: "+rawlist[0]
		#	return None
		for lentry in rawlist:
			if lentry.endswith(".xml"):
				print "added level : "+lentry
				reallist.append(lentry[:-4])
		return reallist