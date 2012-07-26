#!/usr/bin/python

import os
import data
import pygame
import player
import robot
import animations
import map
import levels
import bulletX
from settings import *
from pygame import *
from pygame.image import *
from pygame.locals import *
from animations import *
from map import *

reload(data)
reload(player)
reload(robot)
reload(animations)
reload(map)
reload(levels)
reload(bulletX)

class gameController:

	#controls the title screen
	def parseKeyDown(self, ekey, gamestate, game_selection=None):
		if self.typing_status != "none": #accepting keyboard input
			if ekey == 13: #press enter..
				print "do something with what you typed!"
				if self.typing_status == "~: " and len(self.typing_word) > 5 and self.typing_word[:4] == "goto":
					#load new map
					tmpstr = self.typing_word[5:]
					print "here we load this map - "+tmpstr
					if int(tmpstr) < len(self.map_list) and int(tmpstr) >= 0:
						self.load_map(int(tmpstr))
				else :
					print "Didnt match anything. Word:3 = "+self.typing_word[:4]
				self.typing_status = "none"
				self.typing_word = ""
			elif ekey == 8: #backspace
				if len(self.typing_word) > 0:
					self.typing_word = self.typing_word[:-1]
			elif ekey < 256:
				self.typing_word += chr(ekey)
		elif ekey == 96: #` key.. open console
			self.typing_status = "~: "
			self.typing_word = ""
		elif self.level_status == "play" and ekey == 112: #p - pause?
			self.pause_screen = pygame.Surface([self.screen.get_width(),self.screen.get_height()])
			self.pause_screen.fill((10,10,10))
			self.pause_screen.set_alpha(200)
			self.level_status = "pause"
		elif self.level_status == "pause" and ekey == 112: #p - unpause?
			self.pause_screen = None
			self.level_status = "play"
		elif self.player.animation_index < 4 and ekey == 304 and self.player.on_ground == True: #s-all conditions go! throw
			print "throw time!"
			self.player.animation_index = 5
			self.player.animation_frame_index = 0
			self.player.animation_counter = 0
			self.player.dx = 0
		elif self.player.animation_index < 4 and ekey == 115 and self.player.on_ground == True: #s-all conditions go! block
			print "block time!"
			self.player.animation_index = 4
			self.player.animation_frame_index = 0
			self.player.animation_counter = 0
			self.player.dx = 0
			

		return "game"
	
	def parseKeyUp(self, ekey, gamestate):
		if self.player.animation_index > 3 and (ekey == 115 or ekey == 304): #s - unblock
			self.player.animation_index = 0
			self.player.animation_frame_index = 0
			self.player.animation_counter = 0
		return "game"
			
	def parseKeys(self):
		if self.level_status == "pause":
			return
		keys = pygame.key.get_pressed()
		inputs = []
		if keys[K_LEFT] and self.player.animation_index < 4:
			self.player.moveLeft()
			self.moved = True
		if keys[K_RIGHT] and self.player.animation_index < 4:
			self.player.moveRight()
			self.moved = True
		if keys[K_UP] and self.player.animation_index < 4:
			self.player.jump()

	def __init__(self, screeen,selection,map_selection=0):
		print "stupid init"
		#animations.load_animations()
		#print "Length of ANIMATIONS_PLAYER = "+str(len(ANIMATIONS_PLAYER))
		self.screen = screeen #point to main display object, though it should be passed to the render function
		self.background = pygame.image.load(data.filepath("bigbackground.jpg"))
		self.selected_level = selection
		self.level_name = self.selected_level
		self.level_status = "play" #use this to define pause, victory (go to next level) or um.. defeat
		self.font = pygame.font.Font(data.filepath("visitor1.ttf"), 18)
		self.player = player.Player(data.load_image("bizniezwalkin.png"),animations.load_player(),100,100)
		self.players = pygame.sprite.Group()
		self.players.add(self.players,self.player)
		self.map_selection = map_selection
		self.level = map.Mappy(screeen, data.load_image("bigbackground.jpg"))
		self.moved = False
		self.typing_status = "none"
		self.typing_word = ""
		if self.selected_level != "none":
			lvlpath = "levels/"+self.selected_level+".xml"
			self.mloader = levels.MapLoader(data.filepath(lvlpath))
		else:
			self.mloader = levels.MapLoader(data.filepath("levels/testlevel.xml"))
		self.map_list = self.mloader.parseMap("list maps")
		print "Loaded map list : "+self.map_list[0]
		self.mlevel = self.mloader.parseMap(self.map_list[self.map_selection])
		print str(self.map_list[self.map_selection])+" loaded. Length of ground list = "+str(len(self.mlevel.ground))
		self.player.setlevel(self.mlevel,self.level)
		self.level.setBG(self.mlevel.bg)
		self.obj_types = animations.info_objects()
		self.obj_list = self.mlevel.objects
		self.load_obj_rect()
		print "Loaded object list - "+str(len(self.obj_list))+" objects loaded"
		self.robot_flyer = robot.Robot(data.load_image("robot.png"),animations.load_robot_flying(),100,100,animations.info_robot_flying(),self.player,self.mlevel,self.level)
		self.robot_chase1 = robot.Robot(data.load_image("robot.png"),animations.load_robot_chase1(),60,100,animations.info_robot_chase1(),self.player,self.mlevel,self.level)
		self.robots = pygame.sprite.Group()
		self.robots.add(self.robots,self.robot_flyer)
		self.robots.add(self.robots,self.robot_chase1)
		
	def function(self):
		return "game"

	def render(self, escreen):
		#render data onto display surface
		#self.screen.blit(self.background, (0,0))
		self.level.render()
		if self.level_status == "play":
			self.players.update()
			self.robots.update()
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
		for item in self.obj_list:
			if int(item[0]) > int(self.level.bg_offset[0]) and int(item[0]) < int(self.level.bg_offset[0]) + SCREEN_W  :
				itype = item[2]
				if itype < len(self.obj_types):
					tmpx = int(item[0]) - int(self.level.bg_offset[0])
					tmpy = int(item[1]) - int(self.level.bg_offset[1])
					self.screen.blit(self.obj_types[itype][1],[int(tmpx),int(tmpy)])
		self.players.draw(self.screen)
		self.robots.draw(self.screen)
		
		if self.level_status == "pause":
			self.screen.blit(self.pause_screen,[0,0])
			tmptext = self.font.render("PAUSED (press p to continue)",1,(250,250,250))
			self.screen.blit(tmptext, [(SCREEN_W /2) - 25, SCREEN_H /2])
		
		if self.typing_status != "none":
			tmptext = self.typing_status+self.typing_word
			tmptext = self.font.render(tmptext,1,(250,250,250))
			self.screen.blit(tmptext, [50, 50])
		
	def load_map(self,map_number):
		print "Loading new map from the same level"
		if int(map_number) < 0 or int(map_number) > 20:
			return
		self.map_selection = int(map_number)
		self.mlevel = self.mloader.parseMap(self.map_list[self.map_selection])
		print str(self.map_list[self.map_selection])+" loaded. Length of ground list = "+str(len(self.mlevel.ground))
		self.player.setlevel(self.mlevel,self.level)
		self.level.setBG(self.mlevel.bg)
		self.player.setPosition([100,100],[100,100])
		self.obj_list = self.mlevel.objects
		self.load_obj_rect()

	def update(self):
		self.parseKeys()
		if self.level_status == "pause":
			return
		if self.moved == False:
			self.player.dec((PLAYER_MAX_ACC,0))
		if self.player.animation_index == 5 and self.player.animation_frame_index > 1 and self.player.animation_ticker > self.player.animation_speed - 3:
			tmpdx = -3
			if self.player.facing == "right":
				tmpdx = 3
			print "created briefcase at ["+str(self.player.mapx)+","+str(self.player.mapy)+"]"
			tmprect = self.player.image.get_rect()
			self.robots.add(self.robots, bulletX.Bullet("objects/briefcase.png",self.player.x,self.player.y,tmpdx,0,"briefcase",self.level))
		self.players.update()
		self.robots.update()
		self.level.update(self.player)
		self.check_object_collision()
		self.moved = False
		
	def load_obj_rect(self):
		#load array of rects based on current obj_list
		self.obj_rects = []
		for obj in self.obj_list:
			otype = self.obj_types[obj[2]]
			ow = otype[1].get_width()
			oh = otype[1].get_height()
			orect = pygame.Rect(int(obj[0]),int(obj[1]),ow,oh)
			self.obj_rects.append(orect)
		
	def check_object_collision(self):
		#check to see if the player hit any of the map objects and take.. appropriate steps
		prect = pygame.Rect(self.player.mapx,self.player.mapy,self.player.image.get_width(),self.player.image.get_height())
		col = prect.collidelistall(self.obj_rects)
		if len(col) < 1 :
			return
		for colobj in col:
			#collided with self.obj_list[colrect]
			if len(self.obj_list) - 1 < colobj: #error.. obj_list is missing items taht are in obj_rects
				print "ERROR: the obj_list came up short - "+str(self.obj_list)
				return
			if len(self.obj_list[colobj]) < 3: #should not be less than 3.. error
				print "collided with object "+str(self.obj_list[colobj])
				return
			if self.obj_list[colobj][2] == 0:
				print "zomg phone booth" #collided with phone booth oh noes.. next level
				self.next_level()
			else:
				#print "Collided with object type: "+str(self.obj_list[colobj][2])
				sushi = "yum"
				
	def next_level(self):
		#check to see about moving to next level
		#if this is the last level.. you win! .. by getting booted to entrance screen
		if(self.map_selection >= len(self.map_list) - 1):
			#last lvl
			self.level_status = "exit"
		else :
			self.load_map(self.map_selection + 1)
		