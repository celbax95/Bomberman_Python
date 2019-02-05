import pygame
from pygame.locals import *

pygame.init()

root = pygame.display.set_mode((500,500))

rouge = pygame.image.load("rouge.png").convert()
bleu = pygame.image.load("bleu.png").convert()
jaune = pygame.image.load("jaune.png").convert()
background = pygame.image.load("bg.png").convert()


class carré:

	def __init__(self,pos_x,pos_y,couleur):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.skin = couleur

	def haut(self):
		self.pos_y -= 20

	def bas(self):
		self.pos_y +=20

bRouge = carré(50,200,rouge)
bBleu = carré(150,200,bleu)
bJaune = carré(300,200,jaune)

pygame.key.set_repeat(150, 150)

while 1:
	pygame.event.pump()
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				pygame.quit()
			if event.type == KEYDOWN:
				if keys[pygame.K_w]:
					bRouge.haut()
				if keys[pygame.K_s]:
					bRouge.bas()

				if keys[pygame.K_i]:
					bBleu.haut()
				if keys[pygame.K_k]:
					bBleu.bas()

				if keys[pygame.K_UP]:
					bJaune.haut()
				if keys[pygame.K_DOWN]:
					bJaune.bas()
					
	root.blit(background, (0,0))
	root.blit(bRouge.skin, (bRouge.pos_x, bRouge.pos_y))
	root.blit(bBleu.skin, (bBleu.pos_x, bBleu.pos_y))
	root.blit(bJaune.skin, (bJaune.pos_x, bJaune.pos_y))
	pygame.display.flip()