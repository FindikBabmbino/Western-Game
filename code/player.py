import pygame,sys
from pygame.math import Vector2 as vector
from os import walk
from entity import Entity

class Player(Entity):
	def __init__(self,pos,groups,path,collision_sprites,create_bullet):
		super().__init__(pos,groups,path,collision_sprites)
		self.create_bullet=create_bullet
		self.bullet_shot=False

	def get_status(self):
		#idle
		#my solution
		if self.direction.magnitude()==0:
			if self.status=="down" or self.status=="down_attack":self.status="down_idle"
			elif self.status=="up"or self.status=="up_attack":self.status="up_idle"
			elif self.status=="right"or self.status=="right_attack":self.status="right_idle"
			elif self.status=="left"or self.status=="left_attack":self.status="left_idle"
		#tutorial solution mine is more messy but it is mine so I'll keep it
		# if self.direction.magnitude()==0:
		# 	self.status=self.status.split("_")[0]+"_idle"

		#attacking
		if self.attack:
			self.status=self.status.split("_")[0]+"_attack"


	def input(self):
		keys=pygame.key.get_pressed()
		if not self.attack:
			if keys[pygame.K_w]:
				self.direction.y=-1
				self.status="up"
			elif keys[pygame.K_s]:
				self.direction.y=1
				self.status="down"

			else:
				self.direction.y=0

			if keys[pygame.K_d]:
				self.direction.x=1
				self.status="right"

			elif keys[pygame.K_a]:
				self.direction.x=-1
				self.status="left"

			else:
				self.direction.x=0

		if keys[pygame.K_SPACE]:
			self.attack=True
			self.direction=vector()
			self.frame_index=0
			self.bullet_shot=False

			match self.status.split("_")[0]:
				case "left":self.bullet_direction=vector(-1,0)
				case "right":self.bullet_direction=vector(1,0)
				case "up":self.bullet_direction=vector(0,-1)
				case "down":self.bullet_direction=vector(0,1)


	def animate(self,dt):
		current_animation=self.animations[self.status]
		self.frame_index+=7*dt

		if int(self.frame_index)==2 and self.attack and not self.bullet_shot:
			self.fire_sound.play()
			bullet_start_pos=self.rect.center+self.bullet_direction*80
			self.create_bullet(bullet_start_pos,self.bullet_direction)
			self.bullet_shot=True

		if self.frame_index>=len(current_animation):
			self.frame_index=0
			if self.attack:
				self.attack=False
		self.image=current_animation[int(self.frame_index)]
		self.mask=pygame.mask.from_surface(self.image)

	def check_death(self):
		if self.health<=0:
			pygame.quit()
			sys.exit()

	def update(self,dt):
		self.input()
		self.get_status()
		self.move(dt)
		self.animate(dt)
		self.vulnerability_timer()
		self.check_death()
		self.blink()