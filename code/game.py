import pygame,sys
from settings import *
from player import Player
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from sprite import Sprite,Bullet
from monster import Coffin,Cactus
from healthdisplay import HealthDisplay


class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = vector()
		self.display_surface=pygame.display.get_surface()
		self.bg=pygame.image.load("../graphics/other/bg.png").convert()

	def customize_draw(self,player):
		#change the offset vector
		self.offset.x=player.rect.centerx-WINDOW_WIDTH/2
		self.offset.y=player.rect.centery-WINDOW_HEIGHT/2

		self.display_surface.blit(self.bg,-self.offset)

		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
			#offset_pos=sprite.rect.topleft-self.offset
			offset_rect=sprite.image.get_rect(center=(sprite.rect.center))
			offset_rect.center-=self.offset
			self.display_surface.blit(sprite.image,offset_rect)

class Game:
	def __init__(self):
		pygame.init()
		self.clock=pygame.time.Clock()
		self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption("Western")
		self.bullet_surf=pygame.image.load("../graphics/other/particle.png").convert_alpha()

		self.all_sprites=AllSprites()
		self.obstacle_sprite=pygame.sprite.Group()
		self.bullets=pygame.sprite.Group()
		self.monsters=pygame.sprite.Group()

		self.music=pygame.mixer.Sound("../sound/music.mp3")
		self.music.play(loops=-1)

		self.health_display=HealthDisplay()

		self.setup()


 


	def create_bullet(self,pos,direction):
		Bullet(pos,direction,self.bullet_surf,[self.all_sprites,self.bullets])

	def bullet_collision(self):
		#my solution for the exercise 
		for bullet in self.bullets.sprites():
			if bullet.rect.colliderect(self.player.hitbox):
				self.player.damage()
				bullet.kill()
			else:
				sprites=pygame.sprite.spritecollide(bullet,self.monsters,False,pygame.sprite.collide_mask)
				if sprites:
					bullet.kill()
					#this is for the bullet hitting two monsters 
					for sprite in sprites:
						sprite.damage()

		 # if pygame.sprite.spritecollide(self.player,self.bullets,True):
		 # 	self.player.damage()

		 #obstacle collision
		for obstacle in self.obstacle_sprite.sprites():
		 	pygame.sprite.spritecollide(obstacle,self.bullets,True)


	def setup(self):
		tmx_map=load_pygame("../data/map.tmx")
		#tiles
		for x,y,surf in tmx_map.get_layer_by_name("Fence").tiles():
			Sprite((x*64,y*64),surf,[self.all_sprites,self.obstacle_sprite])

		#objects
		for obj in tmx_map.get_layer_by_name("Object"):
			Sprite((obj.x,obj.y),obj.image,[self.all_sprites,self.obstacle_sprite])
		
		for obj in tmx_map.get_layer_by_name("Entities"):
			if obj.name=="Player":
				self.player=Player(
					pos=(obj.x,obj.y),
					groups=self.all_sprites,
					path=PATHS["player"],
					collision_sprites=self.obstacle_sprite,
					create_bullet=self.create_bullet)

			if obj.name=="Coffin":
				Coffin((obj.x,obj.y),[self.all_sprites,self.monsters],PATHS["coffin"],self.obstacle_sprite,self.player)

			if obj.name=="Cactus":
				Cactus((obj.x,obj.y),[self.all_sprites,self.monsters],PATHS["cactus"],self.obstacle_sprite,self.player,self.create_bullet)
		


	def run_game(self):
		while True:

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					sys.exit()


			dt=self.clock.tick()/1000

			self.display_surface.fill("black")
			#update groups
			self.all_sprites.update(dt)
			self.bullet_collision()
			#drawing groups
			self.all_sprites.customize_draw(self.player)
			self.health_display.display(self.display_surface,WINDOW_WIDTH,WINDOW_HEIGHT,self.player)
			pygame.display.update()
