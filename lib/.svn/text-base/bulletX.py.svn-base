import pygame
import data
from settings import *


class Bullet(pygame.sprite.Sprite):
	def __init__(self,image,xCenter,yCenter,dx,dy,type,level=None):
		#new enemy bullet/ player projectile
		pygame.sprite.Sprite.__init__(self)
		self.image = data.load_image(image)
		self.rect = self.image.get_rect()
		self.animation_ticker = 0
		self.animation_speed = 15
		self.animation_index = 0
		self.animation_frame_index = 0
		self.mapx = xCenter
		self.mapy = yCenter
		self.dy = dy
		self.dx = dx
		self.type = type
		self.level = level
		#self.rect.x = self.level.bg_offset[0] + xCenter
		#self.rect.y = self.level.bg_offset[1] + yCenter
		self.rect.x = xCenter
		self.rect.y = yCenter
		
		
	def update(self):
		self.update_anim()
		self.mapx = int(self.mapx) + int(self.dx)
		#self.mapy = int(self.mapx) + int(self.dy)
		self.dy = 0
		#self.rect.x = self.mapx - self.level.bg_offset[0]
		self.rect = self.rect.move(self.dx,self.dy)
		#self.rect.y = self.mapy
		#self.rect.x = self.mapx
		#self.rect.y = self.mapy

	def update_anim(self):
		self.animation_ticker += 1
		if self.animation_ticker >= self.animation_speed:
			if self.type == "briefcase":
				self.image = pygame.transform.rotate(self.image,90)
		
			self.animation_ticker = 0
		