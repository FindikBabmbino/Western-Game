import pygame
class HealthDisplay():
	def __init__(self):
		self.font=pygame.font.Font(None,50)

	def display(self,display_surf,width,height,player):
		health_text=(f"Health: {player.health}")
		text_surf=self.font.render(health_text,True,"Yellow")
		text_rect=text_surf.get_rect(center=(width/2-100,height-80))
		display_surf.blit(text_surf,text_rect)