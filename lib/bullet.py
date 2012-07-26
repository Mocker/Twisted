import pygame
from settings import *
import data

#bullet class to handle player and enemy projectiles

class Bullet(pygame.sprite.Sprite):
	def __init__(self,image,xCenter,yCenter,dx,dy,type,level):
		pygame.sprite.Sprite.__init__(self)
		self.screen = pygame.display.get_surface().get_rect()
		self.image = data.load_image(image)
		self.animation_ticker = 0
		self.frame_index = 0
		self.animation_speed = 20
		self.type = type
		self.rect = self.image.get_rect()
		self.mapx = xCenter
		self.mapy = yCenter
		self.dy = 0
		self.dx = dx
		self.level = level
	
	def update(self,level=None):
		self.mapx += self.dx
		#tmprect = self.image.get_rect()
		self.rect.x = self.mapx - self.level.bg_offset[0]
		self.rect.y = self.mapy - self.level.bg_offset[1]
		self.update_anim()
		
	def update_anim(self):
		self.animation_ticker +=1 
		if self.animation_ticker >= self.animation_speed:
			self.animation_ticker = 0
			if self.type == "briefcase":
				self.image = pygame.transform.rotate(self.image, 90)