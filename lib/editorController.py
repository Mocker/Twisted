#!/usr/bin/python

import os
import data
import pygame
import edmap
import levels
from settings import *
from pygame import *
from pygame.image import *
from pygame.locals import *
from pygame.color import *
from animations import *
from edmap import *

reload(data)
reload(edmap)
reload(levels)

class editorController:

	#controls the title screen
	def parseKeyDown(self, ekey, gamestate, game_selection):
		self.status_alert = ""
		if ekey == 304: #lshift
			self.holdshift = True
		elif ekey == 117 and self.typing_status == "none": # u = undo
			self.mlevel.removeLastGround()
		elif ekey == 99 and self.typing_status == "none": #c = set color
			self.typing_status = "set color: "
			self.typing_word = self.selected_color
		elif ekey == 105 and self.typing_status == "none": #i = set image
			self.typing_status = "set image (use 'none' to use colors instead): "
			self.typing_word = self.selected_image
		elif ekey == 110 and self.typing_status == "none": #n - set title
			self.typing_status = "set name"
		elif ekey == 98 and self.typing_status == "none": #b - set background image
			self.typing_status = "set background: "
			self.typing_word = self.mlevel.bg_name
		elif self.typing_status == "Save "+self.level_name+".xml ? (y/n) " :
			print "save!"
			if ekey == 121:
				if self.saveFile():
					self.status_alert = "File succesfully saved!"
				else:
					self.status_alert = "ERROR: could not save file"
			self.typing_status = "none"
			self.typing_word = "none"
		elif ekey == 13 and self.typing_status == "set name": #enter - set title
			self.level_name = self.typing_word[2:]
			self.mlevel.levelname = self.level_name
			self.typing_status = "none"
		elif ekey == 115 and self.typing_status == "none" : #s - save
			self.typing_status = "Save "+self.level_name+".xml ? (y/n) "
			self.typing_word = ""
		elif ekey == 13 and self.typing_status == "set image (use 'none' to use colors instead): ": #enter - set image
			if self.typing_word != "none" and len(self.typing_word) > 2: #error checking?!?!?lol yea right
				tmppath = data.filepath("buildingmaterials/"+self.typing_word)
				if os.path.exists(tmppath):
					self.selected_image = "buildingmaterials/"+self.typing_word
			elif self.typing_word == "none":
				self.selected_image = "none"
			self.typing_status = "none"
		elif ekey == 13 and self.typing_status == "set background: ": #enter - set background
			if self.typing_word != "none" and len(self.typing_word) > 2: #error checking?!?!?lol yea right
				tmppath = data.filepath(self.typing_word)
				if os.path.exists(tmppath):
					self.mlevel.setBG(self.typing_word)
					self.level.setBG(self.mlevel.bg)
			self.typing_word = ""
			self.typing_status = "none"
		
		elif ekey == 13 and self.typing_status == "set color: ": #enter - set color
			self.typing_status = "none"
			if len(self.typing_word) == 11 and self.typing_word[3] == ",": #same length, assume it is a valid color
				self.selected_color = self.typing_word
		elif ekey == 8 and self.typing_status != "none" and len(self.typing_word) > 0: #backspace
			self.typing_word = self.typing_word[:-1]
		elif self.typing_status != "none" and ((ekey < 123 and ekey > 96) or ekey == 32 or (ekey < 58 and ekey > 47) or ekey == 44 or ekey == 46) :
			if self.typing_status == "set name" and ekey != 32 and ekey != 44 and ekey != 46:
				self.typing_word += chr(ekey)
			else:
				self.typing_word += chr(ekey)
		return ["game", game_selection]
	
	def parseKeyUp(self, ekey, gamestate):
		if ekey == 304: #lshift
			self.holdshift = False
		return "game"
		
	def parseMouseDown(self, pos):
		#mouse click
		self.pos = pos
		tmpcolor = self.selected_color
		tmpimage = None
		if self.selected_image != "none":
			tmpcolor = "image"
			tmpimage = self.selected_image
		if self.holdshift == True and self.pos[0] > 0 and self.pos[0] < SCREEN_W and self.pos[1] > 0 and self.pos[1] < SCREEN_H:
			tempw = abs(self.tempcoord[0] - (self.level.bg_offset[0] + self.pos[0]))
			temph = abs(self.tempcoord[1] - self.pos[1])
			tmpx = self.tempcoord[0]
			tmpy = self.tempcoord[1]
			if tmpx > (self.level.bg_offset[0] + self.pos[0]):
				tmpx = self.pos[0] + self.level.bg_offset[0]
			if tmpy > self.pos[1]:
				tmpy = self.pos[1]
			temprect = pygame.Rect(tmpx,tmpy,tempw,temph)
			self.mlevel.addground(tmpx,tmpy,tempw,temph,tmpcolor,tmpimage)
		elif self.holdshift == False and self.pos[0] > 0 and self.pos[0] < SCREEN_W and self.pos[1] > 0 and self.pos[1] < SCREEN_H:
			self.tempcoord[0] = self.pos[0] + self.level.bg_offset[0]
			self.tempcoord[1] = self.pos[1]
			
	def parseKeys(self):
		keys = pygame.key.get_pressed()
		inputs = []
		if keys[K_LEFT]:
			self.level.bg_offset[0] -= 20
			print "left"
		if keys[K_RIGHT]:
			self.level.bg_offset[0] += 20
			print "right"
		if keys[K_UP]:
			print"up"
		if keys[304]: #lshift
			self.holdshift = True

	def __init__(self, screeen, selection):
		print "stupid init"
		#animations.load_animations()
		#print "Length of ANIMATIONS_PLAYER = "+str(len(ANIMATIONS_PLAYER))
		self.screen = screeen #point to main display object, though it should be passed to the render function
		self.font = pygame.font.Font(data.filepath("visitor1.ttf"), 18)
		self.fontsm = pygame.font.Font(data.filepath("visitor1.ttf"), 12)
		self.selected_level = selection
		self.tempcoord = [0,0]
		self.holdshift = False
		self.typing_status = "none"
		self.typing_word = "| "
		self.level_name = self.selected_level
		self.selected_color = "010,010,010"
		self.color_sample = pygame.Surface([25,25])
		self.selected_image = "none"
		self.status_alert = ""
		
		#color picker
		#black, dark grey, gray, light grey, white, brown sdfldksfjsdl;fkd;fldskfjdsfl;kj;
		
		self.background = pygame.image.load(data.filepath("bigbackground.jpg"))
		if self.selected_level != "none":
			lvlpath = "levels/"+self.selected_level+".xml"
			self.mloader = levels.MapLoader(data.filepath(lvlpath))
		else:
			self.mloader = levels.MapLoader(data.filepath("levels/testlevel.xml"))
		self.level = edmap.Mappy(screeen, data.load_image("bigbackground.jpg"))
		self.moved = False
		self.map_list = self.mloader.parseMap("list maps")
		if self.selected_level != "none":
			self.mlevel = self.mloader.parseMap(self.map_list[0])
		else:
			self.mlevel = self.mloader.newMap()
		print "Test 1 loaded. Length of ground list = "+str(len(self.mlevel.ground))
		self.level.setBG(self.mlevel.bg)
	
	def function(self):
		return "game"

	def render(self, escreen):
		#render data onto display surface
		#self.screen.blit(self.background, (0,0))
		self.level.render()
		screenrect = pygame.Rect(self.level.bg_offset[0],self.level.bg_offset[1],SCREEN_W,SCREEN_H)
		x = 0
		for ground in self.mlevel.ground:
			if screenrect.colliderect(ground):
				gtemp = pygame.Surface([ground.width,ground.height])
				gtemp = gtemp.convert()
				gtempcolor = self.mlevel.groundattr[x][0]
				#print "temp color = "+str(gtempcolor)
				if gtempcolor != "image" and len(gtempcolor) == 3:
					gtemp.fill(gtempcolor)
				else :
					gtemp = self.mlevel.groundattr[x][1]
					#gtemp.fill((2,2,2))
				self.screen.blit(gtemp, (ground.x - self.level.bg_offset[0] , ground.y - self.level.bg_offset[1]))
			x += 1
		tmptext = "Current Level: "+self.level_name
		tmptext = self.font.render(tmptext,1,(250,250,250))
		self.screen.blit(tmptext, [50, SCREEN_H + 50])
		tmptext = "Click to select a point on the map, then hold down shift and click another location to draw a rectangle."
		tmptext = self.fontsm.render(tmptext,1,(250,250,250))
		self.screen.blit(tmptext, [50, SCREEN_H + 10])
		tmptext = "U = Remove last rectangle.    N = Set name for level. C = Set Color (*note: it must be exactly formatted xxx,xxx,xxx with padded zeroes*)"
		tmptext = self.fontsm.render(tmptext,1,(250,250,250))
		self.screen.blit(tmptext, [50, SCREEN_H + 20])
		tmptext = self.fontsm.render("i = set image for rectangle.  b = set background image",1,(250,250,250))
		self.screen.blit(tmptext, [50, SCREEN_H + 30])
		tmptext = self.font.render("Image: "+self.selected_image,1,(250,250,250))
		self.screen.blit(tmptext, [350, SCREEN_H + 50])
		color1 = int(self.selected_color[:3])
		color2 = int(self.selected_color[4:7])
		color3 = int(self.selected_color[8:11])
		tmpcolor = (color1,color2,color3)
		self.color_sample.fill(tmpcolor)
		self.screen.blit(self.color_sample,[350, SCREEN_H + 85])
		tmptext = "Map Offset: ["+str(self.level.bg_offset[0])+", "+str(self.level.bg_offset[1])+"]"
		tmptext = self.font.render(tmptext,1,(250,250,250))
		self.screen.blit(tmptext, [50, SCREEN_H + 70])
		tmptext = "Current Color: "+self.selected_color
		tmptext = self.font.render(tmptext,1,(250,250,250))
		self.screen.blit(tmptext, [50, SCREEN_H + 85])
		if len(self.status_alert) > 2:
			tmptext = self.font.render(self.status_alert,1,(255,240,240))
			self.screen.blit(tmptext, [500, SCREEN_H + 85])
		if self.typing_status != "none":
			tmptext = self.typing_status + self.typing_word
			tmptext = self.font.render(tmptext,1,(250,250,250))
			self.screen.blit(tmptext, [50, SCREEN_H - 20])
		if self.holdshift == True:
			tmptext = "DRAWING BLOCK AT [ "+str(self.tempcoord[0])+", "+str(self.tempcoord[1])+" ]"
			tmptext = self.font.render(tmptext,1,(250,250,250))
			self.screen.blit(tmptext, [600, SCREEN_H + 40])
		
	def load_map(self,map_number):
		print "Loading new map from the same level"
		#if int(map_number) < 0 or int(map_number) > 20:
		#	return
		#self.map_selection = int(map_number)
		#self.mlevel = self.mloader.parseMap(self.map_list[self.map_selection])
		#print str(self.map_list[self.map_selection])+" loaded. Length of ground list = "+str(len(self.mlevel.ground))
		#self.player.setlevel(self.mlevel)
		#self.level.setBG(self.mlevel.bg)
		#self.player.setPosition([100,100],[100,100])
		
	def update(self):
		self.parseKeys()
		self.level.update()
		self.moved = False
		
	def saveFile(self):
		#take all the level data and plop it into an xml file
		print "saving self.level_name : "+self.level_name+".xml"
		tmpname = "levels/"+self.level_name + ".xml"
		tmpname = data.filepath(tmpname)
		FILE = open(tmpname, "w")
		FILE.write("<game>\n")
		mapline = "<map title=\""+"test 1"+"\" background=\""+self.mlevel.bg_name+"\" maxy=\"770\" height=\"770\" width=\""+str(self.mlevel.w)+"\">"
		FILE.write(mapline+"\n")
		count = 0
		for gitem in self.mlevel.ground:
			gattr = self.mlevel.groundattr[count]
			tmpstr = "<ground x=\""+str(gitem.x)+"\" y=\""+str(gitem.y)+"\" w=\""+str(gitem.width)+"\" h=\""+str(gitem.height)+"\" "
			if gattr[0] == "image":
				tmpstr += "color=\"image\" image=\""+gattr[2]+"\" />"
			else: #color
				tmpcolor = ""
				for col in gattr[0]:
					col = str(col)
					if len(col) == 1:
						col = "00"+col
					elif len(col) == 2:
						col = "0"+col
					tmpcolor = tmpcolor + col + ","
				tmpcolor = tmpcolor[:-1]
				tmpstr += "color=\""+tmpcolor+"\" />"
			FILE.write(tmpstr + "\n")
			count += 1
		FILE.write("</map>\n")
		FILE.write("</game>\n")
		FILE.close()
		return os.path.exists(tmpname)
		
