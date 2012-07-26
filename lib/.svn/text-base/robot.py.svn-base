import pygame
from settings import *


#animations list for player. 
#0 - still
#1 - walk
#2 - run
#3 - jump

class Robot(pygame.sprite.Sprite):
	def __init__(self,image,animations,xCenter,yCenter,rinfo,player,mlevel,mappy):
		print "new robot AHH"
		pygame.sprite.Sprite.__init__(self)
		self.screen = pygame.display.get_surface().get_rect()
		self.animations = animations
		self.animation_index = 0
		self.animation_counter = 0
		self.animation_speed = 20 #how many ticks before going to next frame of animation
		self.animation_ticker = 0 #counter for frame length
		self.animation_frame_index = 0
		self.facing = "right"
		self.robot_name = rinfo[0]
		self.robot_movement = rinfo[1]
		self.image = image
		self.rect = self.image.get_rect()
		self.x = 0
		self.y = 0
		self.on_ground = False
		self.mapx = xCenter
		self.mapy = yCenter
		self.dx = 0
		self.dy = 0
		if self.robot_movement != "flying":
			self.gravity= 1
		else :
			self.gravity = 0
		self.mlevel = mlevel
		self.mappy = mappy
		self.player = player
		# Timer to space out events in the AI
		self.aitimer = 0

	def moveTowardsPlayer(self):
		if self.player.y < self.y and self.on_ground and self.aitimer == 10:
			if self.robot_movement != "flying":
				self.jump()
			else:
				self.dy -= ROBOT_MAX_ACC / 4
		if self.player.mapx < self.mapx + 100 and self.player.mapx > self.mapx - 200 and self.player.y > self.y and self.robot_movement == "flying" and self.y < 300: #dive
			#flying roboto with player below.. dive
			#print "DIVE player coord = ["+str(self.player.mapx)+","+str(self.player.mapy)+"]  vs robot ["+str(self.mapx)+","+str(self.mapy)+"]"
			self.dy += ROBOT_MAX_ACC / 4
		else :
			if self.robot_movement == "flying" and self.y > 100 :
				#not diving, go back to flight mode
				self.dy -= ROBOT_MAX_ACC /4
			elif self.robot_movement == "flying" and self.y < 20:
				self.dy += ROBOT_MAX_ACC / 4
			elif self.robot_movement == "flying":
				self.dy = 0
		if self.player.mapx > self.mapx:
			self.moveRight()
		elif self.player.mapx < self.mapx:
			self.moveLeft()

	def moveLeft(self):
		self.move((-ROBOT_MAX_ACC,0))

	def moveRight(self):
		self.move((ROBOT_MAX_ACC,0))

	def move(self,direction):
		if direction[0] > 0 and self.dx < ROBOT_MAX_SPEED:
			self.acc(direction)
			if self.dx > ROBOT_MAX_SPEED:
				self.dx = ROBOT_MAX_SPEED
		if direction[0] < 0 and self.dx > -ROBOT_MAX_SPEED:
			self.acc(direction)
			if self.dx < -ROBOT_MAX_SPEED:
				self.dx = -ROBOT_MAX_SPEED
		return
		
	def jump(self):
		if (self.on_ground):
			self.dy -= ROBOT_JUMP_ACC
			self.on_ground = False
			print self.dy

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
				
	def setlevel(self, mlevel):
		self.mlevel = mlevel

	def update(self,level=None):
		if self.gravity:
			self.dy += GRAVITY
		if self.dx > 0:
			self.facing = "right"
		if self.dx < 0:
			self.facing = "left"
		#print "ROBOT coord ["+str(self.x)+","+str(self.y)+"]  map coord ["+str(self.mapx)+","+str(self.mapy)+"]"
		self.moveTowardsPlayer()
		self.update_anim()
		self.check_collisions()
		#self.x += self.dx
		#self.y += self.dy
		self.mapx += self.dx
		self.mapy += self.dy
		self.y = self.mapy - self.mappy.bg_offset[1]
		self.x = self.mapx - self.mappy.bg_offset[0]
		#self.rect = self.rect.move(self.dx,self.dy)
		self.rect.y = self.y
		self.rect.x = self.x
		self.aitimer = (self.aitimer +1)%100

	def check_collisions(self):
		if self.y > PLAY_AREA_HEIGHT - self.rect.height / 2:
			self.y = PLAY_AREA_HEIGHT - self.rect.height / 2
			self.dy = 0
			self.on_ground = True
		feetrect = pygame.Rect(self.mapx + 10, (self.mapy + self.image.get_height() - 80), 10, 12)
		testcol = feetrect.collidelist(self.mlevel.ground)
		if testcol >= 0 :
			if self.dy > 0:
				self.dy = 0
				self.on_ground = True
				do_move = False
		else :
			self.y = self.mapy
		testcol = -1
		siderect = pygame.Rect(self.mapx + self.image.get_width() - 2, (self.mapy), 4, self.image.get_height() /2)
		testcol = siderect.collidelist(self.mlevel.ground)
		if testcol >= 0 :
			if self.dx > 0:
				self.dx = 0
				do_move = False
		siderect = pygame.Rect(self.mapx - 2, (self.mapy ), 4, self.rect.height /2)
		testcol = siderect.collidelist(self.mlevel.ground)
		if testcol >= 0 :
			if self.dx < 0:
				self.dx = 0
				do_move = False
				
	def update_anim(self):
		#switch animation frame
		self.animation_ticker += 1
		if self.animation_index != 0 and self.on_ground == False :
			#switch to jump(still for now) animation
			self.animation_index = 3
			if self.robot_movement == "flying": #default flying animation
				self.animation_index = 0
			self.animation_ticker = self.animation_speed
		if self.on_ground == True and self.animation_index != 0 and abs(self.dx) < 1 and self.robot_movement != "flying":
			#switch to still animation
			self.animation_index = 0
			self.animation_ticker = self.animation_speed
		if self.on_ground == True and abs(self.dx) < 5 and abs(self.dx) >= 1 and self.animation_index != 1:
			#switch to walking animation
			self.animation_index = 1
			if self.robot_movement == "flying":
				self.animation_index = 0
			self.animation_ticker = self.animation_speed
		if self.on_ground == True and abs(self.dx) >= 5 and self.animation_index != 2:
			#switch to running
			self.animation_index = 2
			if self.robot_movement == "flying":
				self.animation_index = 1
			self.animation_ticker = self.animation_speed
		#DONE checking for animation time
		
		if self.animation_ticker >= self.animation_speed - 1:
			#load next/first animation frame
			if self.animation_frame_index < len(self.animations[self.animation_index][1]):
				self.image = self.animations[self.animation_index][1][self.animation_frame_index]
			if self.animation_frame_index < (len(self.animations[self.animation_index][1]) -1):
				self.animation_frame_index += 1
				#print "ANIMATION FRAME INCREMENTED TO "+str(self.animation_frame_index)
			else:
				self.animation_frame_index = 0
			self.animation_ticker = 0
			self.animation_speed = self.animations[self.animation_index][0][0]
			if(self.facing == "left"):
				self.image = pygame.transform.flip(self.image, 1, 0)

		#DONE WITH UPDATE ANIM
