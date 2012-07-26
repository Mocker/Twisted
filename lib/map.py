import pygame
from settings import *

#main map class, loads a map file, figures out what part to blit to the screen blah blah blah i'm sleepy


class Mappy:
	#bleh
	def __init__(self, screen, background):
		self.screen = screen
		self.bg = background.convert()
		self.dimensions = self.bg.get_rect()
		self.bg_offset = [0,0] #starting X to blit from 
		self.map_bottom = 768 #define bottom of screen.. beyond this point you fall to death
		self.tempset = [0,0]
		
	def setBG(self,background):
		self.bg = background.convert()
		self.dimensions = self.bg.get_rect()
	
	def update(self,player):
		px = player.mapx
		px_fake = player.rect.x
		py = player.mapy
		temp_offset = [0,0]
		if((px - px_fake) < PLAY_BOUNDRY_L):
			temp_offset = [0,0]
		elif(px > (self.dimensions.width - PLAY_BOUNDRY_R - player.rect.width)):
			temp_offset = self.dimensions.width - SCREEN_W - 50
		else:
			temp_offset = [px - px_fake - PLAY_BOUNDRY_L, 0]
		#print "Player x: "+str(px)+" -- current offset: "+str(self.bg_offset[0])+" and new temp offset: "+str(temp_offset[0])
		self.tempset = temp_offset
		
	def render(self):
		#if(self.tempset != self.bg_offset):
		self.bg_offset = self.tempset
		self.screen.blit(self.bg, [0,0], [self.bg_offset[0],0,SCREEN_W, SCREEN_H])