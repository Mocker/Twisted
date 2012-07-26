import pygame
from settings import *


#animations list for player. 
#0 - still
#1 - walk
#2 - run
#3 - jump

class Player(pygame.sprite.Sprite):
	def __init__(self,image,animations,xCenter,yCenter):
		print "new player doh"
		pygame.sprite.Sprite.__init__(self)
		self.screen = pygame.display.get_surface().get_rect()
		self.animations = animations
		self.animation_index = 0
		self.animation_counter = 0
		self.animation_speed = 10 #how many ticks before going to next frame of animation
		self.animation_ticker = 0 #counter for frame length
		self.animation_frame_index = 0
		self.image = image
		self.rect = self.image.get_rect()
		self.facing = "right"
		self.x = 0
		self.y = 0
		self.mapx = xCenter
		self.mapy = yCenter
		self.dx = 0
		self.dy = 0
		self.gravity= 1
		self.on_ground = False

	def moveLeft(self):
		self.move((-PLAYER_MAX_ACC,0))

	def moveRight(self):
		self.move((PLAYER_MAX_ACC,0))

	def jump(self):
		if (self.on_ground):
			self.dy = -PLAYER_JUMP_ACC
			self.on_ground = False
		#else:
			#self.dy = -PLAYER_AIR_JUMP_ACC
		

	def move(self,direction):
		if direction[0] > 0 and self.dx < PLAYER_MAX_SPEED:
			self.acc(direction)
			if self.dx > PLAYER_MAX_SPEED:
				self.dx = PLAYER_MAX_SPEED
		if direction[0] < 0 and self.dx > -PLAYER_MAX_SPEED:
			self.acc(direction)
			if self.dx < -PLAYER_MAX_SPEED:
				self.dx = -PLAYER_MAX_SPEED
		return
		
	def acc(self, direction):
		self.dx += direction[0]
		self.dy += direction[1]

	def dec(self,direction):
		if abs(self.dx) < direction[0]:
			self.dx = 0
		else:
			if self.dx > 0:
				self.dx -= direction[0]
			else:
				self.dx += direction[0]

		if abs(self.dy) < direction[1]:
			self.dy = 0
		else:
			if self.dy > 0:
				self.dy -= direction[1]
			else:
				self.dy += direction[1]
		
  	def get_orientation(self):
    		if (self.dx < 0):
      			orientation = LEFT
    		if (self.dx > 0):
      			orientation = RIGHT
    		try:
      			return orientation
    		except:
      			return self.orientation
				
	def setlevel(self, mlevel,level):
		self.mlevel = mlevel
		self.level = level
		
	def setPosition(self,screenpos,mappos):
		self.y = screenpos[1]
		self.rect.y = screenpos[1]
		dy = 0
		dx = 0
		self.x = screenpos[0]
		self.rect.x = screenpos[0]
		self.mapx = mappos[0]
		self.mapy = mappos[0]

	def update(self):
		if self.gravity:
			self.dy += GRAVITY
		if self.dx > 0:
			self.facing = "right"
		elif self.dx < 0:
			self.facing = "left"
		self.x += self.dx
		self.y += self.dy
		self.update_anim()
		do_move = False
		do_move = self.check_collisions()
		#print "MOVING: self.dx = "+str(self.dx)
		if do_move == True or 1:
			self.mapx += self.dx
			self.mapy += self.dy
			self.rect = self.rect.move(self.dx,self.dy)
			#print "Moving = true: mapx: "+str(self.mapx)+" and dx= "+str(self.dx)+" and selfx = "+str(self.rect.x)

	def check_collisions(self):
		do_move = True
		if self.y > PLAY_AREA_HEIGHT - self.rect.height / 2:
			self.y = PLAY_AREA_HEIGHT - self.rect.height / 2
			self.dy = 0
			self.on_ground = True
			self.do_move = False
		if self.x > SCREEN_W - self.rect.width :
			self.x = SCREEN_W - self.rect.width  - self.dx
			self.rect.x = SCREEN_W - self.rect.width - self.dx
			if self.mapx > (int(self.level.bg.get_width())-self.image.get_width() -150) and self.dx > 0:
				self.mapx = int(self.level.bg.get_width()) - self.image.get_width() -250
				self.dx = 0
		if self.mapx > int(self.level.bg.get_width()) -self.image.get_width() - 150:
			self.mapx = int(self.level.bg.get_width()) - self.image.get_width() - 250
				
		if self.x  < 0:
			self.x = 50
			self.rect.x = 50
			if self.mapx < 200 and self.dx < 0:
				self.mapx = self.rect.width + 10
				self.dx = 0
		
		if self.mapx < 200:
			self.mapx = self.rect.width + 10
			
		feetrect = pygame.Rect(self.mapx + (self.rect.width /4), (self.mapy + 80), self.rect.width /2, 10)
		testcol = feetrect.collidelist(self.mlevel.ground)
		if testcol >= 0 :
			#print "COLLIDE WITH GROUND : playery = "+str(self.mapy+(self.rect.height /2))+"   and ground y = "+str(self.mlevel.ground[testcol])
			#self.y = self.mlevel.ground[testcol].y + (self.rect.height ) -5
			if self.dy > 0:
				#print "going down"
				self.dy = 0
				#self.dy = -self.dy
				self.on_ground = True
				do_move = False
		else :
			#print "Not colliding: y= "+str(self.y)+" and mapy = "+str(self.mapy)
			self.y = self.mapy
		testcol = -1
		siderect = pygame.Rect(self.mapx + (self.rect.width - 60), (self.mapy - 180), 4, self.rect.height)
		testcol = siderect.collidelist(self.mlevel.ground)
		if testcol >= 0 :
			if self.dx > 0:
				self.dx = 0
				do_move = False
		siderect = pygame.Rect(self.mapx +60, (self.mapy - 180), 4, self.rect.height)
		testcol = siderect.collidelist(self.mlevel.ground)
		if testcol >= 0 :
			if self.dx < 0:
				self.dx = 0
				do_move = False
				
			 
		
		return do_move
				
	def update_anim(self):
		#switch animation frame
		self.animation_ticker += 1
		if self.animation_index != 0 and self.on_ground == False:
			#switch to jump(still for now) animation
			self.animation_index = 3
			self.animation_ticker = self.animation_speed
		if self.on_ground == True and self.animation_index != 0 and abs(self.dx) < 1 and self.animation_index < 4:
			#switch to still animation
			self.animation_index = 0
			self.animation_ticker = self.animation_speed
		if self.on_ground == True and abs(self.dx) < 5 and abs(self.dx) >= 1 and self.animation_index != 1:
			#switch to walking animation
			self.animation_index = 1
			self.animation_ticker = self.animation_speed
		if self.on_ground == True and abs(self.dx) >= 5 and self.animation_index != 2:
			#switch to running
			self.animation_index = 2
			self.animation_ticker = self.animation_speed
		#DONE checking for animation time
		
		if self.animation_ticker >= self.animation_speed - 1:
			#load next/first animation frame
			if self.animation_frame_index < len(self.animations[self.animation_index][1]):
				self.image = self.animations[self.animation_index][1][self.animation_frame_index]
			if self.animation_frame_index < (len(self.animations[self.animation_index][1]) -1):
				self.animation_frame_index += 1
				#print "ANIMATION FRAME INCREMENTED TO "+str(self.animation_frame_index)
			elif self.animation_frame_index != 2: #unless jumping which is one iteration
				self.animation_frame_index = 0
				if self.animation_index == 5: #fire animaiton - then fire
					print "BOom fired!"
					self.animation_index = 0
			self.animation_ticker = 0
			self.animation_speed = self.animations[self.animation_index][0][0]
			if(self.facing == "left"):
				self.image = pygame.transform.flip(self.image, 1, 0)

		#DONE WITH UPDATE ANIM
