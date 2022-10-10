import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import sin

class Entity(pygame.sprite.Sprite):

	def __init__(self,pos,groups,path,collision_sprites):
		super().__init__(groups)
		self.import_assets(path)
		self.frame_index=0
		self.status="down_idle"

		self.image=self.animations[self.status][self.frame_index]
		self.rect=self.image.get_rect(center=pos)

		self.pos=vector(self.rect.center)
		self.direction=vector()
		self.speed=200

		#collisions
		self.hitbox=self.rect.inflate(0,-self.rect.height/2)
		self.collision_sprites=collision_sprites
		self.mask=pygame.mask.from_surface(self.image)

		#attack
		self.attack=False

		self.health=3
		self.is_vulnerable=True
		self.hit_time=None

		self.fire_sound=pygame.mixer.Sound("../sound/bullet.wav")
		self.hit_sound=pygame.mixer.Sound("../sound/hit.mp3")


	def blink(self):
		if not self.is_vulnerable:
			if self.wave_value():
				mask=pygame.mask.from_surface(self.image)
				white_surf=mask.to_surface()
				white_surf.set_colorkey((0,0,0))
				self.image=white_surf

	def wave_value(self):
		value=sin(pygame.time.get_ticks())
		if value >=0:
			return True
		else:
			return False	

	def damage(self):
		if self.is_vulnerable:
			self.hit_sound.play()
			self.health-=1
			self.is_vulnerable=False
			self.hit_time=pygame.time.get_ticks()
			if self.health<=0:
				print("dead")

	def check_death(self):
		if self.health<=0:
			self.kill()

	def vulnerability_timer(self):
		if not self.is_vulnerable:
			current_time=pygame.time.get_ticks()
			if current_time-self.hit_time>400:
				self.is_vulnerable=True

	def import_assets(self,path):
		self.animations= {}
		for index,folder in enumerate(walk(path)):
			if index==0:
				for folder_name in folder[1]:
					self.animations[folder_name]=[]
			else:
				for file_name in sorted(folder[2],key=lambda string: int(string.split(".")[0])):
					path=folder[0].replace("\\","/")+"/"+file_name
					surf=pygame.image.load(path).convert_alpha()
					key=folder[0].split("\\")[1]
					self.animations[key].append(surf)

	def move(self,dt):
		#normaliza a vector->the lenght of a vector is going to be 1
		if self.direction.magnitude()!=0:
			self.direction=self.direction.normalize()

		#horizontal
		self.pos.x+=self.direction.x*self.speed*dt
		self.hitbox.centerx=round(self.pos.x)
		self.rect.centerx=self.hitbox.centerx
		self.collision("horizontal")

		#vertical
		self.pos.y+=self.direction.y*self.speed*dt
		self.hitbox.centery=round(self.pos.y)
		self.rect.centery=self.hitbox.centery
		self.collision("vertical")

	def collision(self,direction):

		for sprites in self.collision_sprites.sprites():
			if sprites.hitbox.colliderect(self.hitbox):
				if direction=="horizontal":
					if self.direction.x>0:
						self.hitbox.right=sprites.hitbox.left
					elif self.direction.x<0:
						self.hitbox.left=sprites.hitbox.right
					self.rect.centerx=self.hitbox.centerx
					self.pos.x=self.hitbox.centerx

				else:
					if self.direction.y<0:
						self.hitbox.top=sprites.hitbox.bottom
					elif self.direction.y>0:
						self.hitbox.bottom=sprites.hitbox.top
					self.rect.centery=self.hitbox.centery
					self.pos.y=self.hitbox.centery