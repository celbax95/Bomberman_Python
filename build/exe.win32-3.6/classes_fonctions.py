import pygame
from pygame.locals import *
from random import random,randrange,choice
import time
import pickle
from math import *

from images import *

from donnees import * # Import du fichier .py contenat les constantes

#################################################################################################
#MENU

def action_bouton(event_pos,liste_boutons,bouton):
	if liste_boutons[bouton][0] <= event_pos[0] <= liste_boutons[bouton][0]+liste_boutons[bouton][2] and liste_boutons[bouton][1] <= event_pos[1] <= liste_boutons[bouton][1]+liste_boutons[bouton][3]:
		return True
	else:
		return False

def reinitialiser_parametres():
	donnees_save = pickle.load(open("donnees_save.xbl","rb"))
	donnees_save["objet_depart"],donnees_save["taille_explosion_depart"],donnees_save["vie_depart"] = reinitialiser_stats
	donnees_save["objets"] = reinitialiser_objets[0][:]
	donnees_save["freq_objets"] = reinitialiser_objets[1]
	donnees_save["objets_spawners"] = reinitialiser_spawners[0]
	donnees_save["secs_avt_spawners"] = reinitialiser_spawners[1]
	donnees_save["freq_spawners"] = reinitialiser_spawners[2]
	donnees_save["secs_avt_fin"],donnees_save["mort_subite"] = reinitialiser_fin
	pickle.dump(donnees_save,open("donnees_save.xbl","wb"))

#AIDE
def click_f(event_pos,direction):
	if direction == "droite":
		if 681 <= event_pos[0] <= 736 and 634 <= event_pos[1] <= 740:
			if event_pos[0]-681 <= -1.03774*(abs(event_pos[1]-687))+55:
				return True
		elif fleche_aide_d[0] <= event_pos[0] <= fleche_aide_d[0]+fleche_aide_d[2] and fleche_aide_d[1] <= event_pos[1] <= fleche_aide_d[1]+fleche_aide_d[3]:
			return True
	if direction == "gauche":
		if 14 <= event_pos[0] <= 69 and 634 <= event_pos[1] <= 740:
			if event_pos[0]-69 >= 1.03774*(abs(event_pos[1]-687))-55:
				return True
		elif fleche_aide_g[0] <= event_pos[0] <= fleche_aide_g[0]+fleche_aide_g[2] and fleche_aide_g[1] <= event_pos[1] <= fleche_aide_g[1]+fleche_aide_g[3]:
			return True
	return False

#################################################################################################
#JEU

class Persos:
	"""Classe contenant :
	-Les 4 personnages, leurs coordonnées (x et y) ainsi que l'affectation du skin
	-Les methodes de déplacement pour chacuns des persos"""

	def __init__(self,pos_x,pos_y):

		donnees_save = pickle.load(open("donnees_save.xbl","rb"))

		self.pos_x = pos_x #position x de l'instance créee
		self.pos_y = pos_y #position y de l'instance créee
		self.skin = None
		self.last_damage = pygame.time.get_ticks()
		if nb_joueurs != 1:
			self.vie = donnees_save["vie_depart"]+1
		else:
			self.vie = 2
		self.active = True
		
		self.last_bombing = pygame.time.get_ticks()
		self.cooldown = 900
		self.bombes = []
		self.nb_bombes = -1
		self.taille_explosion = donnees_save["taille_explosion_depart"]
		
		self.objet_tenu = None
		if nb_joueurs != 1:
			if donnees_save["objet_depart"] == 0:
				self.taille_explosion += 1
			elif donnees_save["objet_depart"] == 3:
				if self.vie < 2:
					self.vie = 2
			else:
				self.objet_tenu = donnees_save["objet_depart"]
		else:
			self.objet_tenu = None

		self.charges = 5
		self.objet_actif = False
		self.inverse = -cooldown_inverse
		self.bloque = -cooldown_bloque
		self.GodMode_bombe_spe = False

	def deplacement(self,direction,all_bombes):
		global blocks
		dep_x = 0
		dep_y = 0
		collision = 0
		if direction == "haut":
			dep_y = -50
			if self.pos_y <= 50:
				collision = 1
		elif direction == "bas":
			dep_y = 50
			if self.pos_y >= ROOT_Y-200:
				collision = 1
		elif direction == "gauche":
			dep_x = -50
			if self.pos_x <= 50:
				collision = 1
		elif direction == "droite":
			dep_x = 50
			if self.pos_x >= ROOT_X-100:
				collision = 1

		if collision == 0:
			for i in range(0,len(murs_gris)):
				murs_gris_x, murs_gris_y = grille[murs_gris[i]]
				if self.pos_x + dep_x == murs_gris_x:
					if self.pos_y + dep_y == murs_gris_y:
						collision = 1
		if collision == 0:
			for i in range(0,len(blocks)):
				blocks_x,blocks_y = grille[blocks[i]]
				if self.pos_x + dep_x == blocks_x:
					if self.pos_y + dep_y == blocks_y:
						collision = 1
		if collision == 0:
			for i in range(0,len(all_bombes)):
				if all_bombes[i].active:
					if self.pos_x+dep_x == all_bombes[i].pos_x:
						if self.pos_y+dep_y == all_bombes[i].pos_y:
							collision = 1
		if collision == 0:
			if self.objet_actif and self.objet_tenu == (1):
				Items.block_5(perso.index(self))
			elif self.objet_actif and self.objet_tenu == (2):
				Items.bombes_5(perso.index(self))
			elif self.GodMode_bombe_spe:
				if self.charges > 0:
					self.bomb()
					self.charges -= 1
				else:
					self.GodMode_bombe_spe = False

			self.pos_y += dep_y
			self.pos_x += dep_x

	def bomb(self):
		now = pygame.time.get_ticks()
		if now-self.last_bombing >= self.cooldown:

			temp_GMB = None
			temp_GME = None

			if self.objet_tenu == (9) and self.objet_actif == True:
				temp_GMB = True
			elif self.objet_tenu == (10) and self.objet_actif == True:
				temp_GME = True

			if len(self.bombes) >= 20:
				if self.nb_bombes >= 19:
					self.nb_bombes = -1
				self.nb_bombes += 1
				self.bombes[self.nb_bombes] = Bombes(self.pos_x,self.pos_y,self.taille_explosion,GodMode_bombe=temp_GMB,GodMode_explosion=temp_GME)
			elif len(self.bombes) < 20:
				self.bombes.append(Bombes(self.pos_x,self.pos_y,self.taille_explosion,GodMode_bombe=temp_GMB,GodMode_explosion=temp_GME))
				self.nb_bombes += 1
			self.last_bombing = now

	def objet(self):
		if self.objet_tenu == (1):
			self.objet_actif = True
		elif self.objet_tenu == (2):
			self.objet_actif = True
		elif self.objet_tenu == (4):
			Items.random_bombes(perso.index(self))
		elif self.objet_tenu == (5):
			Items.random_blocks(perso.index(self))
		elif self.objet_tenu == (6):
			Items.inverse(perso.index(self))
		elif self.objet_tenu == (7):
			Items.bloque(perso.index(self))
		elif self.objet_tenu == (8):
			Items.teleport(perso.index(self))
		elif self.objet_tenu == (9):
			if not self.objet_actif:
				Items.GodMode_bombe(perso.index(self))
			else:
				self.GodMode_bombe_spe = True
				self.charges = 3
		elif self.objet_tenu == (10):
			Items.GodMode_explosion(perso.index(self))

###########################################################################################

class Bombes():
	"""Classe contenant la methode de création des bombes ainsi que leur explosion"""

	def __init__(self,pos_x,pos_y,taille_explosion=1,time_to_explode=time_to_explode,GodMode_bombe=False,GodMode_explosion=False):
		self.time_pose = pygame.time.get_ticks()
		self.active = True
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.taille_explosion = taille_explosion
		self.time_to_explode = time_to_explode

		self.GodMode_bombe = GodMode_bombe
		self.GodMode_explosion = GodMode_explosion

		self.delay_animation = 500
		self.last_animation = -self.delay_animation
		self.animation = -1

	def explode(self):
		global nb_explosions,explosions
		if pygame.time.get_ticks() - self.time_pose >= self.time_to_explode:
			self.active = False
			if len(explosions) >= 300:
				if nb_explosions >=299:
					nb_explosions = -1
				nb_explosions += 1
				explosions[nb_explosions] = Explosions(self.pos_x,self.pos_y,self.taille_explosion,GodMode_bombe=self.GodMode_bombe,GodMode_explosion=self.GodMode_explosion)
			elif len(explosions) < 300:
				explosions.append(Explosions(self.pos_x,self.pos_y,self.taille_explosion,GodMode_bombe=self.GodMode_bombe,GodMode_explosion=self.GodMode_explosion))
				nb_explosions += 1

###########################################################################################

class Explosions():
	"Classe contenant la direction hortizontale, verticale, ou centrale de l'explosion"

	def __init__(self,pos_x,pos_y,taille_explosion,orientation=0,GodMode_explosion=False,GodMode_bombe=False):
		self.time_create = pygame.time.get_ticks()

		self.active = True
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.taille_explosion = taille_explosion
		self.orientation = orientation #0 milieu ; 1 horizontal ; 2 vertical

		if GodMode_bombe:
			self.collision_murs_gris = True
		if GodMode_explosion:
			self.collision_murs_gris = False
		else:
			self.collision_murs_gris = True

		self.GodMode_bombe = GodMode_bombe
		self.GodMode_explosion = GodMode_explosion
		self.liste_explosion = []

		if self.orientation == 0:
			self.creer_explosion()

		self.delay_animation = 100
		self.last_animation = -self.delay_animation
		self.animation = 0

	def get_taille_explosion_max(self,direction,temp_pos_x,temp_pos_y):
		if direction == 0:
			return temp_pos_y > self.pos_y-self.taille_explosion*50
		elif direction == 1:
			return temp_pos_y < self.pos_y+self.taille_explosion*50
		elif direction == 2:
			return temp_pos_x > self.pos_x-self.taille_explosion*50
		elif direction == 3:
			return temp_pos_x < self.pos_x+self.taille_explosion*50

	def add_explosion(self,temp_pos_x,temp_pos_y,orientation):
		global nb_explosions
		if len(explosions) >= 300:
			if nb_explosions >= 299:
				nb_explosions = -1
			nb_explosions += 1
			explosions[nb_explosions] = Explosions(temp_pos_x,temp_pos_y,None,orientation,GodMode_explosion=self.GodMode_explosion,GodMode_bombe=self.GodMode_bombe)
		elif len(explosions) < 300:
			explosions.append(Explosions(temp_pos_x,temp_pos_y,None,orientation,GodMode_explosion=self.GodMode_explosion,GodMode_bombe=self.GodMode_bombe))
			nb_explosions += 1


	def creer_explosion(self):
		global murs_gris, blocks, nb_explosions, explosions

		for direction in range(0,4): # 0=haut; 1=bas; 2=gauche; 3=droite
			collision = 0
			temp_pos_x = self.pos_x
			temp_pos_y = self.pos_y
			dep_x = 0
			dep_y = 0
			if direction == 0:
				dep_y = -50
				orientation = 2
			elif direction == 1:
				dep_y = 50
				orientation = 2
			elif direction == 2:
				dep_x = -50
				orientation = 1
			elif direction == 3:
				dep_x = 50
				orientation = 1

			while collision == 0 and self.get_taille_explosion_max(direction,temp_pos_x,temp_pos_y):
				temp_pos_x += dep_x
				temp_pos_y += dep_y
				if collision == 0:
					if direction == 0 and temp_pos_y-dep_y <= 50:
						collision = 1
					elif direction == 1 and temp_pos_y-dep_y >= ROOT_Y-200:
						collision =1
					elif direction == 2 and temp_pos_x-dep_x <= 50:
						collision =1
					elif direction == 3 and temp_pos_x-dep_x >= ROOT_X-100:
						collision =1

				if self.collision_murs_gris:
					if collision == 0:
						for i in range(0,len(murs_gris)):
							murs_gris_x, murs_gris_y = grille[murs_gris[i]]
							if temp_pos_x == murs_gris_x:
								if temp_pos_y == murs_gris_y:
									collision = 1

				if collision == 0:
					for i in range(0,len(blocks)):
						blocks_x,blocks_y = grille[blocks[i]]
						if temp_pos_x == blocks_x:
							if temp_pos_y == blocks_y:
								Explosions.add_explosion(self,temp_pos_x,temp_pos_y,orientation)
								if nb_joueurs != 1:
									Items.spawn_item(blocks[i])
								del blocks[i]
								collision = 1
								break

				if collision == 0:
					Explosions.add_explosion(self,temp_pos_x,temp_pos_y,orientation)

###########################################################################################

class Items():

	def __init__(self,pos_x,pos_y,type):
		self.time_pose = pygame.time.get_ticks()
		self.active = True
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.type = type
		self.resistance = 1000

	def on_item(n,i):
		if items[i].active:
			if perso[n].pos_x == items[i].pos_x and perso[n].pos_y == items[i].pos_y:
				if (perso[n].objet_tenu != 9 and not perso[n].objet_actif) or (perso[n].objet_tenu != 10 and not perso[n].objet_actif):
					if items[i].type == 0:
						if perso[n].taille_explosion < 4:
							perso[n].taille_explosion += 1
					elif items[i].type == 1:
						perso[n].objet_tenu = 1
						perso[n].charges = 2
					elif items[i].type == 2:
						perso[n].objet_tenu = 2
						perso[n].charges = 5
	
					elif items[i].type == 3:
						if perso[n].vie < 2:
							perso[n].vie += 1
					elif items[i].type == 4:
						perso[n].objet_tenu = 4
					elif items[i].type == 5:
						perso[n].objet_tenu = 5
					elif items[i].type == 6:
						perso[n].objet_tenu = 6
					elif items[i].type == 7:
						perso[n].objet_tenu = 7
	
					elif items[i].type == 8:
						perso[n].objet_tenu = 8
					elif items[i].type == 9:
						perso[n].objet_tenu = 9
					elif items[i].type == 10:
						perso[n].objet_tenu = 10

					perso[n].objet_actif = False
				items[i].active = False

	def spawn_item(pos): #pos = Tuple contenant pos_x et pos_y
		if random() < taux_drop_items[-1]:
			temp_random = random()
			for i in range(len(taux_drop_items)):
				if taux_drop_items[i] is not None:
						if temp_random < taux_drop_items[0]: #explo +
							Items.add_item(pos,(0))
						elif temp_random < taux_drop_items[1]: #briques_5
							Items.add_item(pos,(1))
						elif temp_random < taux_drop_items[2]: #bombes_5
							Items.add_item(pos,(2))
						elif temp_random < taux_drop_items[3]: #vie
							Items.add_item(pos,(3))
						elif temp_random < taux_drop_items[4]: #random_bombes
							if len([x for x in range(len(grille)) if x not in blocks if x not in murs_gris]) > 30:
								Items.add_item(pos,(4))	
						elif temp_random < taux_drop_items[5]: #random_briques
							if len([x for x in range(len(grille)) if x not in blocks if x not in murs_gris]) > 30:
								Items.add_item(pos,(5))	
						elif temp_random < taux_drop_items[6]: #inverse
							Items.add_item(pos,(6))	
						elif temp_random < taux_drop_items[7]: #bloque
							Items.add_item(pos,(7))
						elif temp_random < taux_drop_items[8]: #TP
							Items.add_item(pos,(8))	
						elif temp_random < taux_drop_items[9]: #GMB
							Items.add_item(pos,(9))	
						elif temp_random < taux_drop_items[10]: #GME
							Items.add_item(pos,(10))
				
	def add_item(pos,type): #pos = numero de grille
		global nb_items
		pos_x, pos_y = grille[pos]
		for i in range(len(items)):
			if (pos_x,pos_y) == (items[i].pos_x,items[i].pos_y):
				del items[i]
				break

		if len(items) >= items_max:
			if nb_items >= items_max-1:
				nb_items = -1
			nb_items += 1
			items[nb_items] = Items(pos_x,pos_y,type)
		elif len(items) < items_max:
			items.append(Items(pos_x,pos_y,type))
			nb_items += 1

	def block_5(numero_perso):
		global blocks
		blocks.append(grille.index((perso[numero_perso].pos_x,perso[numero_perso].pos_y)))
		blocks.sort()
		perso[numero_perso].charges -= 1
		perso[numero_perso].objet_actif = False
		if perso[numero_perso].charges <= 0:
			perso[numero_perso].objet_tenu = None

	def bombes_5(numero_perso):
		perso[numero_perso].cooldown = 1
		perso[numero_perso].bomb()
		perso[numero_perso].charges -= 1
		if perso[numero_perso].charges <= 0:
			perso[numero_perso].cooldown = 900
			perso[numero_perso].objet_actif = False
			perso[numero_perso].objet_tenu = None

	def random_bombes(numero_perso):
		#get position perso
		temp_pos = []
		for i in range(len(perso)):
			temp_pos.append(grille.index((perso[i].pos_x,perso[i].pos_y)))
		#placement des bombes
		for i in range(5):
			temp_emplacement_x,temp_emplacement_y = grille[choice([x for x in range(len(grille)) if x not in blocks if x not in murs_gris if x not in temp_pos])]
			if len(perso[numero_perso].bombes) >= 15:
				if perso[numero_perso].nb_bombes >= 14:
					perso[numero_perso].nb_bombes = -1
				perso[numero_perso].nb_bombes += 1
				perso[numero_perso].bombes[perso[numero_perso].nb_bombes] = Bombes(temp_emplacement_x,temp_emplacement_y,2,time_to_explode=randrange(2700,3000))
			elif len(perso[numero_perso].bombes) < 15:
				perso[numero_perso].bombes.append(Bombes(temp_emplacement_x,temp_emplacement_y,2,time_to_explode=randrange(2700,3000)))
				perso[numero_perso].nb_bombes += 1
			perso[numero_perso].objet_tenu = None

	def random_blocks(numero_perso):
		global blocks
		#get position perso
		temp_pos = []
		for i in range(len(perso)):
			temp_pos.append(grille.index((perso[i].pos_x,perso[i].pos_y)))
		#placement des blocks
		if len([x for x in range(len(grille)) if x not in blocks if x not in murs_gris]) > 35:
			for i in range(7):
				temp_emplacement_x,temp_emplacement_y = grille[choice([x for x in range(len(grille)) if x not in blocks if x not in murs_gris if x not in temp_pos])]
				blocks.append(grille.index((temp_emplacement_x,temp_emplacement_y)))
				blocks.sort()
			perso[numero_perso].objet_tenu = None

	def inverse(numero_perso=0):
		if nb_joueurs != 1:
			random_perso = choice([x for x in range(len(perso)) if x != numero_perso if perso[x].active])
			perso[random_perso].inverse = pygame.time.get_ticks()
			perso[numero_perso].objet_tenu = None
		else:
			perso[0].inverse = pygame.time.get_ticks()

	def bloque(numero_perso=0):
		if nb_joueurs != 1:
			perso[randrange(len(perso))].bloque = pygame.time.get_ticks()
			perso[numero_perso].objet_tenu = None
		else:
			perso[0].bloque = pygame.time.get_ticks()

	def teleport(numero_perso):
		perso[numero_perso].pos_x, perso[numero_perso].pos_y = grille[choice([x for x in range(len(grille)) if x not in blocks if x not in murs_gris])]
		perso[numero_perso].objet_tenu = None

	def GodMode_bombe(numero_perso):
		perso[numero_perso].objet_actif = True
		perso[numero_perso].vie = 0
		perso[numero_perso].cooldown = 10
		perso[numero_perso].taille_explosion = 3

	def GodMode_explosion(numero_perso):
		perso[numero_perso].objet_actif = True
		perso[numero_perso].vie = 0
		perso[numero_perso].cooldown = 700
		perso[numero_perso].taille_explosion = 13

###########################################################################################

class Spawners():

	spawners_actif = False

	def __init__(self,pos):
		self.cooldown = randrange(spawners_charge_min,spawners_charge_max)
		self.pos = grille.index(pos)
		self.last_spawn = pygame.time.get_ticks()
		self.init = True
		self.spawnable = spawners_activate
		Spawners.spawners_actif = False

	def spawn(self):
		if Spawners.spawners_actif:
			if not self.init:
				self.cooldown = randrange(spawners_charge_min,spawners_charge_max)
				self.init = True
			if pygame.time.get_ticks() > self.last_spawn+self.cooldown:
				self.last_spawn = pygame.time.get_ticks()
				self.spawn_item()
				self.init = False
		else:
			if pygame.time.get_ticks() > self.last_spawn+spawners_activate:
				Spawners.spawners_actif = True

	def spawn_item(self):
		if random() < taux_spawners[-1]:
			temp_random = random()
			for i in range(len(taux_spawners)):
				if taux_spawners[i] is not None:
						if temp_random < taux_spawners[0]: #explo +
							Items.add_item(self.pos,(0))
						elif temp_random < taux_spawners[1]: #briques_5
							Items.add_item(self.pos,(1))
						elif temp_random < taux_spawners[2]: #bombes_5
							Items.add_item(self.pos,(2))
						elif temp_random < taux_spawners[3]: #vie
							Items.add_item(self.pos,(3))
						elif temp_random < taux_spawners[4]: #random_bombes
							if len([x for x in range(len(grille)) if x not in blocks if x not in murs_gris]) > 30:
								Items.add_item(self.pos,(4))	
						elif temp_random < taux_spawners[5]: #random_briques
							if len([x for x in range(len(grille)) if x not in blocks if x not in murs_gris]) > 30:
								Items.add_item(self.pos,(5))	
						elif temp_random < taux_spawners[6]: #inverse
							Items.add_item(self.pos,(6))	
						elif temp_random < taux_spawners[7]: #bloque
							Items.add_item(self.pos,(7))
						elif temp_random < taux_spawners[8]: #TP
							Items.add_item(self.pos,(8))	
						elif temp_random < taux_spawners[9]: #GMB
							Items.add_item(self.pos,(9))	
						elif temp_random < taux_spawners[10]: #GME
							Items.add_item(self.pos,(10))

###########################################################################################

class MS_bombes():
	bombes = []
	nb_bombes = -1
	intervalle = 2000
	last = pygame.time.get_ticks()
	debut = 10000
	lancement = pygame.time.get_ticks()
	
	def reset(debut):
		MS_bombes.bombes = []
		MS_bombes.nb_bombes = -1
		MS_bombes.intervalle = 2000
		MS_bombes.last = pygame.time.get_ticks()
		MS_bombes.debut = debut*1000
		MS_bombes.lancement = pygame.time.get_ticks()

	def MS_bombes():
			#get position perso
			temp_pos = []
			for i in range(len(perso)):
				temp_pos.append(grille.index((perso[i].pos_x,perso[i].pos_y)))
			#placement des bombes
			temp_emplacement_x,temp_emplacement_y = grille[choice([x for x in range(len(grille)) if x not in blocks if x not in murs_gris if x not in temp_pos])]
			if len(MS_bombes.bombes) >= 100:
				if MS_bombes.nb_bombes >= 99:
					MS_bombes.nb_bombes = -1
				MS_bombes.nb_bombes += 1
				MS_bombes.bombes[MS_bombes.nb_bombes] = Bombes(temp_emplacement_x,temp_emplacement_y,3,time_to_explode=1700)
			elif len(MS_bombes.bombes) < 100:
				MS_bombes.bombes.append(Bombes(temp_emplacement_x,temp_emplacement_y,3,time_to_explode=1700))
				MS_bombes.nb_bombes += 1

###########################################################################################

class Solo():
	bombes = []
	nb_bombes = -1
	intervalle = 2000
	last = pygame.time.get_ticks()
	lancement = pygame.time.get_ticks()
	debut = 5000
	taille = 1
	tour = 0
	pause = 3000
	score = 0
	
	def reset():
		Solo.bombes = []
		Solo.nb_bombes = -1
		Solo.intervalle = 2000
		MS_bombes.last = pygame.time.get_ticks()
		Solo.lancement = pygame.time.get_ticks()
		Solo.taille = 1
		Solo.tour = 0
		Solo.score = 0
	
	def solo_bombes():
			#get position perso
			temp_pos = []
			temp_pos.append(grille.index((perso[0].pos_x,perso[0].pos_y)))
			#placement des bombes
			temp_emplacement_x,temp_emplacement_y = grille[choice([x for x in range(len(grille)) if x not in blocks if x not in murs_gris if x not in temp_pos])]
			if len(Solo.bombes) >= 150:
				if Solo.nb_bombes >= 149:
					Solo.nb_bombes = -1
				Solo.nb_bombes += 1
				Solo.bombes[Solo.nb_bombes] = Bombes(temp_emplacement_x,temp_emplacement_y,Solo.taille,time_to_explode=1700)
			elif len(Solo.bombes) < 150:
				Solo.bombes.append(Bombes(temp_emplacement_x,temp_emplacement_y,Solo.taille,time_to_explode=1700))
				Solo.nb_bombes += 1

	def spawn_vie():
		temp_pos = []
		temp_pos.append(grille.index((perso[0].pos_x,perso[0].pos_y)))
		temp_emplacement = choice([x for x in range(len(grille)) if x not in blocks if x not in murs_gris if x not in temp_pos])
		Items.add_item(temp_emplacement,3)

###########################################################################################
def get_time():
	global temps,time_min
	time_sec = int((time.time()-temps))

	if int(time_sec) < 10:
		time_sec = "0"+ str(time_sec)
	elif int(time_sec) >= 60:
		time_min = int(time_min) + 1
		temps = time.time()
		time_sec = 0

	time_min = int(time_min)
	if time_min == 0:
		time_min = "00"
	elif time_min < 10:
		time_min = "0"+ str(time_min)
	elif time_min >= 10:
		time_min = str(time_min)
	elif time_min > 99:
		time_min = 99

	return time_sec,time_min

def get_pourcentage(liste,type,freq):
	donnees_save = pickle.load(open("donnees_save.xbl","rb"))
	temp_taux_cumule = 0
	taux_total = 0
	
	for i in range(len(liste)-1):
		if donnees_save[type][i] == True:
			taux_total += liste[i]
	taux = [None,None,None,None,None,None,None,None,None,None,None,liste[-1]]
	for i in range(len(liste)-1):
		if donnees_save[type][i] == True:
			taux[i] = liste[i]/taux_total
	for i in range(len(taux)-1):
		if taux[i] is not None:
			temp_taux_cumule += taux[i]
			taux[i] = round(temp_taux_cumule,6)
		else:
			taux[i] = -1
	if donnees_save[freq] == "normale":
		taux[-1] = taux[-1]*(2/3)
	if donnees_save[freq] == "petite":
		taux[-1] = taux[-1]*(1/3)
	return taux

def lancer_partie():
	global perso,blocks,taux_drop_items,taux_spawners,spawners_activate,items,temps,time_min,nb_joueurs

	donnees_save = pickle.load(open("donnees_save.xbl","rb"))

	nb_joueurs = donnees_save["nb_joueurs"]

	if donnees_save["secs_avt_fin"] > 0:
		time_end = pygame.time.get_ticks() + donnees_save["secs_avt_fin"]*1000
	else:
		time_end = False

	temp_actif = False
	for i in range(len(donnees_save["objets_spawners"])):
		if donnees_save["objets_spawners"][i] == True:
			temp_actif = True

	if temp_actif == True:
		if donnees_save["nb_joueurs"] == 2:
			background = backgroundp2s
		elif donnees_save["nb_joueurs"] == 3:
			background = backgroundp3s
		elif donnees_save["nb_joueurs"] == 4:
			background = backgroundp4s
	else:
		if donnees_save["nb_joueurs"] == 2:
			background = backgroundp2
		elif donnees_save["nb_joueurs"] == 3:
			background = backgroundp3
		elif donnees_save["nb_joueurs"] == 4:
			background = backgroundp4

	temps = time.time()
	time_min = 0

	blocks = []
	blocks = blocksS[:]
	taux_drop_items = get_pourcentage(taux_drop_itemsS,"objets","freq_objets")
	taux_spawners = get_pourcentage(taux_spawnersS,"objets_spawners","freq_objets")
	items = []
	spawners = []
	spawners_activate = donnees_save["secs_avt_spawners"]*1000
	if spawners_activate == 0:
		spawners_activate = 1

	mort_subite = donnees_save["mort_subite"]
	MS_bombes.reset(donnees_save["secs_avt_fin"])

	#init des spawners
	if len(spawners) > 0:
		for i in range(len(spawners_locations)):
			spawners[i] = Spawners(spawners_locations[i])
	else:
		for i in range(len(spawners_locations)):
			spawners.append(Spawners(spawners_locations[i]))

	#création des classes
	perso = []
	if donnees_save["nb_joueurs"] >= 1:
		perso.append(Persos(50,50)) #perso1
	if donnees_save["nb_joueurs"] >= 2:
		perso.append(Persos(650,550)) #perso2
	if donnees_save["nb_joueurs"] >= 3:
		perso.append(Persos(650,50)) #perso3
	if donnees_save["nb_joueurs"] >= 4:
		perso.append(Persos(50,550)) #perso4

	return perso,blocks,items,spawners,background,False,time_end,mort_subite

###########################################################################################

def lancer_partie_1joueur():
	global perso,blocks,items,temps,time_min,nb_joueurs

	donnees_save = pickle.load(open("donnees_save.xbl","rb"))
	
	nb_joueurs = donnees_save["nb_joueurs"]

	background = backgroundp1

	Solo.reset()

	best_score = donnees_save["best_score"]

	temps = time.time()
	time_min = 0

	blocks = []
	blocks = blocks_solo[:]
	items = []

	#création des classes
	perso = [Persos(350,300)]

	return perso,blocks,items,background,False,0,best_score