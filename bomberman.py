import pygame #Import pygame
from pygame.locals import * #Import pygame
import time #import time
import pickle
import threading
from random import random

pygame.init() #initialisation pygame

F_clock = pygame.font.SysFont("Arial",30)
F_taille_explosion_depart = pygame.font.SysFont("Ebrima",65,bold=True)
F_secs_avt = pygame.font.SysFont("Ebrima",44,bold=True)
F_gagne = pygame.font.SysFont("Ebrima",47,bold=True)
F_score = pygame.font.SysFont("Ebrima",47,bold=True)
F_score_direct = pygame.font.SysFont("Arial",30)
F_meilleur_score = pygame.font.SysFont("Ebrima",35,bold=True)
F_chargement = pygame.font.SysFont("Ebrima",35,bold=True)

clock = pygame.time.Clock()

donnees_save = pickle.load(open("donnees_save.xbl","rb"))
if donnees_save["fullscreen"]:
	root = pygame.display.set_mode((750,750),pygame.FULLSCREEN)
else:
	root = pygame.display.set_mode((750,750),pygame.DOUBLEBUF) #Taille de la fenetre 750x750

from images import *

from donnees import * # Import du fichier .py contenat les constantes
from classes_fonctions import * # Import du fichier .py contenant les classes et fonctions

################################################################################################################
#initialisation des boucles

menu = True
page = "acceuil"
mouse_pressed = None
partie_en_cours = False
chargement = False
bomberman = True

################################################################################################################

while bomberman:

	while menu: #menu
		clock.tick(30)
		#pages (acceuil / jouer / nb_joueurs / parametres / stats / objets / spawners)
		root.blit(background_menu,(0,0))

		for event in pygame.event.get():
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				pygame.display.quit()
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				mouse_pressed = True
					
			if event.type == MOUSEBUTTONUP and event.button == 1:
				#menu
				if page == "acceuil":
					if action_bouton(event.pos,B_menu,0):#fullscreen
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						pygame.display.quit()
						pygame.display.init()
						if donnees_save["fullscreen"]:
							root = pygame.display.set_mode((750,750),pygame.DOUBLEBUF)
							donnees_save["fullscreen"] = False
						else:
							root = pygame.display.set_mode((750,750),pygame.FULLSCREEN)
							donnees_save["fullscreen"] = True
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
					if action_bouton(event.pos,B_menu,1):#jouer
						page = "jouer"
					if action_bouton(event.pos,B_menu,2):#aide
						page = "aide0"
					if action_bouton(event.pos,B_menu,3):#quitter
						pygame.display.quit()
				elif page == "jouer":
					if action_bouton(event.pos,B_jouer,0):#lancer la partie
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						chargement = True
						menu = False
					if action_bouton(event.pos,B_jouer,1):#nb de joueurs
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						page = "nb_joueurs"
					if action_bouton(event.pos,B_jouer,2):#parametres
						page = "parametres"
					if action_bouton(event.pos,B_jouer,3):#parametres par def
						donnees_save = reinitialiser_parametres()

					if action_bouton(event.pos,B_jouer,4):#retour
						page = "acceuil"
				elif page == "nb_joueurs":
					if action_bouton(event.pos,B_nb_joueurs,0):#1 joueur
						donnees_save["nb_joueurs"] = 1
					if action_bouton(event.pos,B_nb_joueurs,1):#2 joueurs
						donnees_save["nb_joueurs"] = 2
					if action_bouton(event.pos,B_nb_joueurs,2):#3 joueurs
						donnees_save["nb_joueurs"] = 3
					if action_bouton(event.pos,B_nb_joueurs,3):#4 joueurs
						donnees_save["nb_joueurs"] = 4
					if action_bouton(event.pos,B_nb_joueurs,4):#retour
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
						page = "jouer"
					if donnees_save["nb_joueurs"] == 1:#reinitialiser score
						if action_bouton(event.pos,B_nb_joueurs,5):
							donnees_save["best_score"] = 0
				elif page == "parametres":
					if action_bouton(event.pos,B_parametres,0):#stats debut de partie
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						page = "stats"
					if action_bouton(event.pos,B_parametres,1):#objets
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						page = "objets"
					if action_bouton(event.pos,B_parametres,2):#spawners
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						page = "spawners"
					if action_bouton(event.pos,B_parametres,3):#fin de partie
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						page = "fin"
					if action_bouton(event.pos,B_parametres,4):#retour
						page = "jouer"
				elif page == "stats":
					for i in range(11): #tableau items
						if action_bouton(event.pos,B_stats,i):
							if donnees_save["objet_depart"] == i:
								donnees_save["objet_depart"] = None
							else:
								donnees_save["objet_depart"] = i
					if action_bouton(event.pos,B_stats,11):#plus
						if donnees_save["taille_explosion_depart"] < 9:
							donnees_save["taille_explosion_depart"] += 1
					if action_bouton(event.pos,B_stats,12):#moins
						if donnees_save["taille_explosion_depart"] > 1:
							donnees_save["taille_explosion_depart"] -= 1
					if action_bouton(event.pos,B_stats,13):#vie 0
						donnees_save["vie_depart"] = 0
					if action_bouton(event.pos,B_stats,14):#vie 1
						donnees_save["vie_depart"] = 1
					if action_bouton(event.pos,B_stats,15):#reinitialiser
						donnees_save["objet_depart"],donnees_save["taille_explosion_depart"],donnees_save["vie_depart"] = reinitialiser_stats
					if action_bouton(event.pos,B_stats,16):#retour
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
						page = "parametres"
				elif page == "objets":
					for i in range(len(donnees_save["objets"])): #tableau items #len = 10 / range(0,11)
						if B_objets[i][0] <= event.pos[0] <= B_objets[i][0]+B_objets[i][2] and B_objets[i][1] <= event.pos[1] <= B_objets[i][1]+B_objets[i][3]:
							if donnees_save["objets"][i] == True:
								donnees_save["objets"][i] = False
							else:
								donnees_save["objets"][i] = True
					if action_bouton(event.pos,B_objets,11):#freq petite
						donnees_save["freq_objets"] = "petite"
					if action_bouton(event.pos,B_objets,12):#freq moyenne
						donnees_save["freq_objets"] = "normale"
					if action_bouton(event.pos,B_objets,13):#freq grande
						donnees_save["freq_objets"] = "grande"
					if action_bouton(event.pos,B_objets,14):#reinitialiser
						donnees_save["objets"] = reinitialiser_objets[0][:]
						donnees_save["freq_objets"] = reinitialiser_objets[1]
					if action_bouton(event.pos,B_objets,15):#retour
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
						page = "parametres"
				elif page == "spawners":
					for i in range(len(donnees_save["objets_spawners"])): #tableau items #len = 10 / range(0,11)
						if B_spawners[i][0] <= event.pos[0] <= B_spawners[i][0]+B_spawners[i][2] and B_spawners[i][1] <= event.pos[1] <= B_spawners[i][1]+B_spawners[i][3]:
							if donnees_save["objets_spawners"][i] == True:
								donnees_save["objets_spawners"][i] = False
							else:
								donnees_save["objets_spawners"][i] = True

					if action_bouton(event.pos,B_spawners,11): #plus
						if donnees_save["secs_avt_spawners"] < 900:
							donnees_save["secs_avt_spawners"] += 30
					if action_bouton(event.pos,B_spawners,12): #moins
						if donnees_save["secs_avt_spawners"] > 0:
							donnees_save["secs_avt_spawners"] -= 30
					if action_bouton(event.pos,B_spawners,13):#freq petite
						donnees_save["freq_spawners"] = "petite"
					if action_bouton(event.pos,B_spawners,14):#freq normale
						donnees_save["freq_spawners"] = "normale"
					if action_bouton(event.pos,B_spawners,15):#freq grande
						donnees_save["freq_spawners"] = "grande"
					if action_bouton(event.pos,B_spawners,16):#reinitialiser
						donnees_save["objets_spawners"] = reinitialiser_spawners[0]
						donnees_save["secs_avt_spawners"] = reinitialiser_spawners[1]
						donnees_save["freq_spawners"] = reinitialiser_spawners[2]
					if action_bouton(event.pos,B_spawners,17):#retour
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
						page = "parametres"
				elif page == "fin":
					if action_bouton(event.pos,B_fin,0):#plus
						if donnees_save["secs_avt_fin"] < 900:
							donnees_save["secs_avt_fin"] += 30
					if action_bouton(event.pos,B_fin,1):#moins
						if donnees_save["secs_avt_fin"] > 0:
							donnees_save["secs_avt_fin"] -= 30
					if action_bouton(event.pos,B_fin,2):#mort subite non
						donnees_save["mort_subite"] = False
					if action_bouton(event.pos,B_fin,3):#mort subite oui
						donnees_save["mort_subite"] = True
					if action_bouton(event.pos,B_fin,4):#reinitialiser
						donnees_save["secs_avt_fin"],donnees_save["mort_subite"] = reinitialiser_fin
					if action_bouton(event.pos,B_fin,5):#retour
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
						page = "parametres"
				#aide
				elif page == "aide0":
					if click_f(event.pos,"droite"):
						page = "aide1"
				elif page == "aide1":
					if click_f(event.pos,"droite"):
						page = "aide2"
					if click_f(event.pos,"gauche"):
						page = "aide0"
				elif page == "aide2":
					if click_f(event.pos,"droite"):
						page = "aide3"
					if click_f(event.pos,"gauche"):
						page = "aide1"
				elif page == "aide3":
					if click_f(event.pos,"droite"):
						page = "aide4"
					if click_f(event.pos,"gauche"):
						page = "aide2"
				elif page == "aide4":
					if click_f(event.pos,"droite"):
						page = "aide5"
					if click_f(event.pos,"gauche"):
						page = "aide3"
				elif page == "aide5":
					if click_f(event.pos,"droite"):
						page = "aide6"
					if click_f(event.pos,"gauche"):
						page = "aide4"
				elif page == "aide6":
					if click_f(event.pos,"gauche"):
						page = "aide5"
				if page == "aide0" or page == "aide1" or page == "aide2" or page == "aide3" or page == "aide4" or page == "aide5" or page == "aide6":
					if action_bouton(event.pos,B_aide,0):
						page = "acceuil"


				mouse_pressed = False
		
		if mouse_pressed:
			#menu
			if page == "acceuil":
				liste_boutons = B_menu[:]
			elif page == "jouer":
				liste_boutons = B_jouer[:]
			elif page == "nb_joueurs":
				if donnees_save["nb_joueurs"] == 1:
					liste_boutons = B_nb_joueurs[:]
				elif donnees_save["nb_joueurs"] > 1:
					liste_boutons = B_nb_joueurs[:len(B_nb_joueurs)-1]
			elif page == "parametres":
				liste_boutons = B_parametres[:]
			elif page == "stats":
				liste_boutons = B_stats[:]
			elif page == "objets":
				liste_boutons = B_objets[:]
			elif page == "spawners":
				liste_boutons = B_spawners[:]
			elif page == "fin":
				liste_boutons = B_fin[:]
			elif page == "aide0" or page == "aide1" or page == "aide2" or page == "aide3" or page == "aide4" or page == "aide5" or page == "aide6":
				liste_boutons = B_aide[:]
			#aide

			for i in range(len(liste_boutons)):
				if liste_boutons[i][0] <= pygame.mouse.get_pos()[0] <= liste_boutons[i][0]+liste_boutons[i][2] and liste_boutons[i][1] <= pygame.mouse.get_pos()[1] <= liste_boutons[i][1]+liste_boutons[i][3]:
					pygame.draw.rect(root,couleur_select,liste_boutons[i])
			
			if page == "aide0":
				temp_f_d = click_f(event.pos,"droite")
			elif page == "aide6":
				temp_f_g = click_f(event.pos,"gauche")
			elif page == "aide1" or page == "aide2" or page == "aide3" or page == "aide4" or page == "aide5":
				temp_f_d = click_f(event.pos,"droite")
				temp_f_g = click_f(event.pos,"gauche")

		#menu		
		if page == "acceuil":
			root.blit(I_acceuil,(0,0))
		elif page == "jouer":
			root.blit(I_jouer,(0,0))
		elif page == "nb_joueurs":
			if donnees_save["nb_joueurs"] == 1:
				root.blit(S_nb_joueurs,B_nb_joueurs[0])
				root.blit(B_reinitialiser_score,B_nb_joueurs[-1])
				L_meilleur_score = F_meilleur_score.render("Meilleur score : {}".format(donnees_save["best_score"]),1,(0,0,0))
				if donnees_save["best_score"] < 10:
					root.blit(L_meilleur_score,(233,488))
				elif donnees_save["best_score"] < 100:
					root.blit(L_meilleur_score,(223,488))
				elif donnees_save["best_score"] > 100:
					if donnees_save["best_score"] >= 1000:
						donnees_save["best_score"] = 999
					root.blit(L_meilleur_score,(213,488))
			if donnees_save["nb_joueurs"] == 2:
				root.blit(S_nb_joueurs,B_nb_joueurs[1])
			if donnees_save["nb_joueurs"] == 3:
				root.blit(S_nb_joueurs,B_nb_joueurs[2])
			if donnees_save["nb_joueurs"] == 4:
				root.blit(S_nb_joueurs,B_nb_joueurs[3])
			root.blit(I_nb_joueurs,(0,0))
		elif page == "parametres":
			root.blit(I_parametres,(0,0))
		elif page == "stats":
			if donnees_save["objet_depart"] in range(11):
				root.blit(S_tableau_objets,B_stats[donnees_save["objet_depart"]])
			if donnees_save["vie_depart"] == 0:
				root.blit(S_stats_vie,B_stats[13])
			elif donnees_save["vie_depart"] == 1:
				root.blit(S_stats_vie,B_stats[14])
			root.blit(I_stats,(0,0))
			L_taille_explosion_depart = F_taille_explosion_depart.render(str(donnees_save["taille_explosion_depart"]), 1, (0,0,0))
			root.blit(L_taille_explosion_depart,(542,480))
		elif page == "objets":
			for i in range(len(donnees_save["objets"])):
				if donnees_save["objets"][i] == True:
					root.blit(S_tableau_objets,(B_objets[i]))
			if donnees_save["freq_objets"] == "petite":
				root.blit(S_freq_PNG,B_objets[11])
			elif donnees_save["freq_objets"] == "normale":
				root.blit(S_freq_PNG,B_objets[12])
			elif donnees_save["freq_objets"] == "grande":
				root.blit(S_freq_PNG,B_objets[13])
			root.blit(I_objets,(0,0))
		elif page == "spawners":
			for i in range(len(donnees_save["objets_spawners"])):
				if donnees_save["objets_spawners"][i] == True:
					root.blit(S_tableau_objets,(B_spawners[i]))
			if donnees_save["freq_spawners"] == "petite":
				root.blit(S_freq_PNG,B_spawners[13])
			elif donnees_save["freq_spawners"] == "normale":
				root.blit(S_freq_PNG,B_spawners[14])
			elif donnees_save["freq_spawners"] == "grande":
				root.blit(S_freq_PNG,B_spawners[15])
			root.blit(I_spawners,(0,0))

			afficher_mins_avt_spawners = int(donnees_save["secs_avt_spawners"]/60)
			afficher_secs_avt_spawners = donnees_save["secs_avt_spawners"]%60
			L_mins_avt_spawners = F_secs_avt.render(str(afficher_mins_avt_spawners), 1, (0,0,0))
			if afficher_mins_avt_spawners < 10:
				if afficher_secs_avt_spawners < 10:
					afficher_secs_avt_spawners = str(afficher_secs_avt_spawners) + "0"
				L_secs_avt_spawners = F_secs_avt.render(str(afficher_secs_avt_spawners), 1, (0,0,0))
				root.blit(L_mins_avt_spawners,(425,373))
				root.blit(L_secs_avt_spawners,(497,373))
				root.blit(S_min,(458,402))

			else:
				if afficher_secs_avt_spawners < 10:
					afficher_secs_avt_spawners = str(afficher_secs_avt_spawners) + "0"
				L_secs_avt_spawners = F_secs_avt.render(str(afficher_secs_avt_spawners), 1, (0,0,0))
				root.blit(L_mins_avt_spawners,(414,373))
				root.blit(L_secs_avt_spawners,(507,373))
				root.blit(S_min,(468,402))


		elif page == "fin":
			if donnees_save["mort_subite"] == False:
				root.blit(S_fin_mort_subite,B_fin[2])
			elif donnees_save["mort_subite"] == True:
				root.blit(S_fin_mort_subite,B_fin[3])
			root.blit(I_fin,(0,0))

			afficher_mins_avt_fin = int(donnees_save["secs_avt_fin"]/60)
			afficher_secs_avt_fin = donnees_save["secs_avt_fin"]%60
			L_mins_avt_fin = F_secs_avt.render(str(afficher_mins_avt_fin), 1, (0,0,0))
			if afficher_mins_avt_fin < 10:
				if afficher_secs_avt_fin < 10:
					afficher_secs_avt_fin = str(afficher_secs_avt_fin) + "0"
				L_secs_avt_fin = F_secs_avt.render(str(afficher_secs_avt_fin), 1, (0,0,0))
				root.blit(L_mins_avt_fin,(271,352))
				root.blit(L_secs_avt_fin,(341,352))
				root.blit(S_min,(302,381))

			else:
				if afficher_secs_avt_fin < 10:
					afficher_secs_avt_fin = str(afficher_secs_avt_fin) + "0"
				L_secs_avt_fin = F_secs_avt.render(str(afficher_secs_avt_fin), 1, (0,0,0))
				root.blit(L_mins_avt_fin,(258,352))
				root.blit(L_secs_avt_fin,(351,352))
				root.blit(S_min,(312,381))
		#aide
		elif page == "aide0":
			root.blit(aide0,(0,0))
		elif page == "aide1":
			root.blit(aide1,(0,0))
		elif page == "aide2":
			root.blit(aide2,(0,0))
		elif page == "aide3":
			root.blit(aide3,(0,0))
		elif page == "aide4":
			root.blit(aide4,(0,0))
		elif page == "aide5":
			root.blit(aide5,(0,0))
		elif page == "aide6":
			root.blit(aide6,(0,0))
		if page == "aide0" or page == "aide1" or page == "aide2" or page == "aide3" or page == "aide4" or page == "aide5" or page == "aide6":
			if temp_f_d:
				root.blit(S_fleche_droite,(602,634))
			elif temp_f_g:
				root.blit(S_fleche_gauche,(14,634))
			temp_f_d = False
			temp_f_g = False

		#rafraichissement de l'ecran
		pygame.display.flip()

################################################################################################################
	nb_joueurs = pickle.load(open("donnees_save.xbl","rb"))["nb_joueurs"]
	
	while nb_joueurs != 1 and partie_en_cours: #partie a > 1joueurs
		clock.tick(60)
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				pygame.display.quit()
			if event.type == KEYDOWN:
				for i in range(len(perso)):
					if pygame.time.get_ticks() > perso[i].inverse+cooldown_inverse:
						#Normaux
						if i == 0:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = K_w,K_s,K_a,K_d,K_LCTRL,K_q
						if i == 1:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = K_UP,K_DOWN,K_LEFT,K_RIGHT,K_RCTRL,K_RSHIFT
						if i == 2:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = K_i,K_k,K_j,K_l,K_b,K_u
						if i == 3:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = 0x108,0x105,0x104,0x106,0x100,0x107
					else:
						#Inversés ( if not pygame.time.get_ticks() > perso[i].inverse+cooldown_inverse )
						if i == 0:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = K_s,K_w,K_d,K_a,K_q,K_LCTRL
						if i == 1:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = K_DOWN,K_UP,K_RIGHT,K_LEFT,K_RSHIFT,K_RCTRL
						if i == 2:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = K_k,K_i,K_l,K_j,K_u,K_b
						if i == 3:
							haut,bas,gauche,droite,drop_bombe,utilise_objet = 0x105,0x108,0x106,0x104,0x107,0x100

					if perso[i].active and pygame.time.get_ticks() > perso[i].bloque+cooldown_bloque:
						if not end_game:
							if event.key == haut:
								perso[i].deplacement("haut",all_bombes)
							elif event.key == bas:
								perso[i].deplacement("bas",all_bombes)
							elif event.key == gauche:
								perso[i].deplacement("gauche",all_bombes)
							elif event.key == droite:
								perso[i].deplacement("droite",all_bombes)
							elif event.key == drop_bombe:
								perso[i].bomb()
							elif event.key == utilise_objet:
								perso[i].objet()
							elif event.key == K_y:
								while len(blocks) > 0:
									Items.spawn_item(blocks[0])
									del blocks[0]
							#elif event.key == K_t:
							#	perso,blocks,items,spawners,background = lancer_4joueurs()
					if event.key == K_ESCAPE:
						page = "acceuil"
						menu = True
						partie_en_cours = False

		#Spawners
		for i in range(len(spawners)):
			spawners[i].spawn()

		#maj des items
		for n in range(len(perso)):
			if perso[n].active:
				for i in range(len(items)):
					Items.on_item(n,i)

		#gestion bombes
		all_bombes = MS_bombes.bombes
		for i in range(len(perso)):
			all_bombes += perso[i].bombes

#re-collage des éléments
		#background
		root.blit(background,(0,0))
		
		#Objet_tenu
		for i in range(len(perso)):
			if perso[i].objet_actif:
				if len(perso) == 4:
					root.blit(item_actif,pos_4p_objet_tenuS[i])
				if len(perso) == 3:
					root.blit(item_actif,pos_3p_objet_tenuS[i])
				if len(perso) == 2:
					root.blit(item_actif,pos_2p_objet_tenuS[i])

			if perso[i].objet_tenu is not None:
				if perso[i].objet_tenu == 1:
					temp_type = blocks_5
				elif perso[i].objet_tenu == 2:
					temp_type = bombes_5

				elif perso[i].objet_tenu == 4:
					temp_type = random_bombes
				elif perso[i].objet_tenu == 5:
					temp_type = random_blocks
				elif perso[i].objet_tenu == 6:
					temp_type = inverse
				elif perso[i].objet_tenu == 7:
					temp_type = bloque

				elif perso[i].objet_tenu == 8:
					temp_type = teleport
				elif perso[i].objet_tenu == 9:
					temp_type = GodMode_bombe
				elif perso[i].objet_tenu == 10:
					temp_type = GodMode_explosion
			
				if len(perso) == 4:
					root.blit(temp_type,pos_4p_objet_tenu[i])
				if len(perso) == 3:
					root.blit(temp_type,pos_3p_objet_tenu[i])
				if len(perso) == 2:
					root.blit(temp_type,pos_2p_objet_tenu[i])

		#Items
		for i in range(0,len(items)): 
			if items[i].active:
				if items[i].type == 0:
					temp_type = explosion_plus
				elif items[i].type == 1:
					temp_type = blocks_5
				elif items[i].type == 2:
					temp_type = bombes_5
				elif items[i].type == 3:
					temp_type = armure

				elif items[i].type == 4:
					temp_type = random_bombes
				elif items[i].type == 5:
					temp_type = random_blocks
				elif items[i].type == 6:
					temp_type = inverse
				elif items[i].type == 7:
					temp_type = bloque

				elif items[i].type == 8:
					temp_type = teleport
				elif items[i].type == 9:
					temp_type = GodMode_bombe
				elif items[i].type == 10:
					temp_type = GodMode_explosion

				root.blit(temp_type,(items[i].pos_x,items[i].pos_y))

		#Briques
		for i in range(len(blocks)):
			root.blit(brick,grille[blocks[i]])

		#Persos
		for i in range(len(perso)):
			if perso[i].active:
				now = pygame.time.get_ticks()
				if perso[i].vie >= 2 and now-perso[i].last_bombing >= perso[i].cooldown:
					perso[i].skin = persoBV[i]

				elif perso[i].vie >= 2:
					perso[i].skin = persoV[i]

				elif now-perso[i].last_bombing >= perso[i].cooldown:
					perso[i].skin = persoB[i]

				else:
					perso[i].skin = persoS[i]
				root.blit(perso[i].skin,(perso[i].pos_x,perso[i].pos_y))

				if not pygame.time.get_ticks() > perso[i].inverse+cooldown_inverse:
					root.blit(perso_inverse,(perso[i].pos_x,perso[i].pos_y))

				if not pygame.time.get_ticks() > perso[i].bloque+cooldown_bloque:
					perso[i].inverse = -cooldown_inverse
					root.blit(perso_bloque,(perso[i].pos_x,perso[i].pos_y))

		#Bombes
		for i in range(0,len(all_bombes)):
			if all_bombes[i].active:
				if all_bombes[i].animation > 1:
					all_bombes[i].animation = 0
				
				if all_bombes[i].GodMode_bombe:
					root.blit(bombeGMB[all_bombes[i].animation],(all_bombes[i].pos_x, all_bombes[i].pos_y))
				elif all_bombes[i].GodMode_explosion:
					root.blit(bombeGME[all_bombes[i].animation],(all_bombes[i].pos_x, all_bombes[i].pos_y))
				else:
					root.blit(bombe[all_bombes[i].animation],(all_bombes[i].pos_x, all_bombes[i].pos_y))
				
				if pygame.time.get_ticks() > all_bombes[i].last_animation+all_bombes[i].delay_animation:
					all_bombes[i].delay_animation = (all_bombes[i].delay_animation+60)*0.6
					all_bombes[i].animation += 1
					all_bombes[i].last_animation = pygame.time.get_ticks()

				all_bombes[i].explode()

		#Explosions
		for i in range(0,len(explosions)):
			if pygame.time.get_ticks()-explosions[i].time_create >= explosion_time:
				explosions[i].active = False
			if explosions[i].active:
				if explosions[i].animation > 1:
					explosions[i].animation = 0
		
				if explosions[i].orientation == 0:
					if pygame.time.get_ticks()<explosions[i].time_create+200:
						explosions[i].animation = 2
					if explosions[i].GodMode_bombe:
						root.blit(explosionGMB0[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					elif explosions[i].GodMode_explosion:
						root.blit(explosionGME0[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					else:
						root.blit(explosion0[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))

				elif explosions[i].orientation == 1:
					if explosions[i].GodMode_bombe:
						root.blit(explosionGMB1[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					elif explosions[i].GodMode_explosion:
						root.blit(explosionGME1[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					else:
						root.blit(explosion1[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))

				elif explosions[i].orientation == 2:
					if explosions[i].GodMode_bombe:
						root.blit(explosionGMB2[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					elif explosions[i].GodMode_explosion:
						root.blit(explosionGME2[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					else:
						root.blit(explosion2[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
				
				if pygame.time.get_ticks() > explosions[i].last_animation+explosions[i].delay_animation:
					explosions[i].animation += 1
					explosions[i].last_animation = pygame.time.get_ticks()
		while 1:
			for i in range(0,len(explosions)):
				if explosions[i].active == False:
					del explosions[i]
					break
			break

		#Destruction explosion
		for i in range(len(explosions)):
			if explosions[i].active:
				#Mort perso
				for n in range(len(perso)):
					if perso[n].last_damage <= pygame.time.get_ticks()-cooldown_damage:
						if (perso[n].pos_x,perso[n].pos_y) == (explosions[i].pos_x,explosions[i].pos_y):
							perso[n].last_damage = pygame.time.get_ticks()
							if perso[n].objet_tenu == (9) or perso[n].objet_tenu == (10) and perso[n].objet_actif == True:
								perso[n].cooldown = 900
								perso[n].taille_explosion = 2
							perso[n].objet_tenu = None
							perso[n].objet_actif = False
							perso[n].vie -= 1
							if perso[n].vie <= 0:
								perso[n].active = False
				#Destruction Items
				for n in range(len(items)):
					if (items[n].pos_x,items[n].pos_y) == (explosions[i].pos_x,explosions[i].pos_y):
						if pygame.time.get_ticks() - items[n].time_pose >= items[n].resistance:
							items[n].active = False

		if not end_game:
			time_sec,time_min = get_time()

		L_temps = F_clock.render("{}:{}".format(time_min,time_sec),1,(0,0,0))
		root.blit(L_temps,(338,642))

		perso_actifs = 0
		for i in range(len(perso)):
			if perso[i].active:
				perso_actifs += 1
				perso_gagne = i + 1
		if perso_actifs <= 1:
			root.blit(gagne,(0,0))
			L_gagne = F_gagne.render(str(perso_gagne),1,(63,63,63))
			L_gagne_ombre = F_gagne.render(str(perso_gagne),1,(0,0,0))
			root.blit(L_gagne_ombre,(229,261))
			root.blit(L_gagne,(230,262))
			end_game = True

		if time_end > 0:
			if not mort_subite:
				if time_end is not False:
					if pygame.time.get_ticks() > time_end:
						root.blit(fin_temps,(0,0))
						end_game = True
	
			elif mort_subite:
				if not end_game:
					temp_now = pygame.time.get_ticks()
					if temp_now > MS_bombes.lancement+MS_bombes.debut:
						if temp_now > MS_bombes.last+MS_bombes.intervalle:
							MS_bombes.MS_bombes()
							if MS_bombes.intervalle > 200:
								MS_bombes.intervalle -= 100
							MS_bombes.last = now

		#rafraichissement de l'ecran
		pygame.display.flip()

################################################################################################################################################

	while nb_joueurs == 1 and partie_en_cours: #partie a 1joueurs
		clock.tick(60)
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				pygame.display.quit()
			if event.type == KEYDOWN:
				if pygame.time.get_ticks() > perso[0].inverse+cooldown_inverse:
					#Normaux
					haut,bas,gauche,droite,utilise_objet = K_w,K_s,K_a,K_d,K_q
				else:
					#Inversés ( if not pygame.time.get_ticks() > perso[i].inverse+cooldown_inverse )
					haut,bas,gauche,droite,utilise_objet = K_s,K_w,K_d,K_a,K_LCTRL

				if perso[0].active and pygame.time.get_ticks() > perso[0].bloque+cooldown_bloque:
					if not end_game:
						if event.key == haut:
							perso[0].deplacement("haut",all_bombes)
						elif event.key == bas:
							perso[0].deplacement("bas",all_bombes)
						elif event.key == gauche:
							perso[0].deplacement("gauche",all_bombes)
						elif event.key == droite:
							perso[0].deplacement("droite",all_bombes)
						#elif event.key == K_y:
						#	while len(blocks) > 0:
						#		Items.spawn_item(blocks[0])
						#		del blocks[0]
						#elif event.key == K_t:
						#	perso,blocks,items,spawners,background = lancer_4joueurs()
				if event.key == utilise_objet:
					perso[0].objet()
				if event.key == K_ESCAPE:
					if end_game:
						donnees_save = pickle.load(open("donnees_save.xbl","rb"))
						donnees_save["best_score"] = Solo.score
						pickle.dump(donnees_save,open("donnees_save.xbl","wb"))
					page = "acceuil"
					menu = True
					partie_en_cours = False
		
		#gestion bombess
		all_bombes = Solo.bombes

		#Briques
		for i in range(len(blocks)):
			root.blit(brick,grille[blocks[i]])

		#maj des items
		if perso[0].active:
			for i in range(len(items)):
				Items.on_item(0,i)

		#re-collage des éléments
		#background
		root.blit(background,(0,0))

		#objet tenu
		if perso[0].objet_tenu == 8:
			root.blit(teleport,pos_1p_objet_tenu)

		#score direct
		if Solo.score <= best_score:
			L_score_direct = F_score_direct.render(str(Solo.score),1,(0,0,0))
		else:
			L_score_direct = F_score_direct.render(str(Solo.score),1,(43,175,37))
		pos_score_y = 667
		if Solo.score < 10:
			pos_score_x = 636
		elif Solo.score < 100:
			pos_score_x = 626
		elif Solo.score < 1000:
			pos_score_x = 616
		elif Solo.score == 1000:
			Solo.score = 999
		root.blit(L_score_direct,(pos_score_x,pos_score_y))

		#Items
		for i in range(0,len(items)):
			if items[i].active:
				root.blit(armure,(items[i].pos_x,items[i].pos_y))

		#Briques
		for i in range(len(blocks)):
			root.blit(brick,grille[blocks[i]])

		#Persos
		if perso[0].active:
			now = pygame.time.get_ticks()
			if perso[0].vie >= 2:
				perso[0].skin = persoV[0]

			else:
				perso[0].skin = persoS[0]
			root.blit(perso[0].skin,(perso[0].pos_x,perso[0].pos_y))

			if not pygame.time.get_ticks() > perso[0].inverse+cooldown_inverse:
				root.blit(perso_inverse,(perso[0].pos_x,perso[0].pos_y))

			if not pygame.time.get_ticks() > perso[0].bloque+cooldown_bloque:
				perso[0].inverse = -cooldown_inverse
				root.blit(perso_bloque,(perso[0].pos_x,perso[0].pos_y))

		#Bombes
		for i in range(0,len(all_bombes)):
			if all_bombes[i].active:
				if all_bombes[i].animation > 1:
					all_bombes[i].animation = 0
				
				root.blit(bombe[all_bombes[i].animation],(all_bombes[i].pos_x, all_bombes[i].pos_y))
				
				if pygame.time.get_ticks() > all_bombes[i].last_animation+all_bombes[i].delay_animation:
					all_bombes[i].delay_animation = (all_bombes[i].delay_animation+60)*0.6
					all_bombes[i].animation += 1
					all_bombes[i].last_animation = pygame.time.get_ticks()

				all_bombes[i].explode()

		#Explosions
		for i in range(0,len(explosions)):
			if pygame.time.get_ticks()-explosions[i].time_create >= explosion_time:
				explosions[i].active = False
			if explosions[i].active:
				if explosions[i].animation > 1:
					explosions[i].animation = 0
		
				if explosions[i].orientation == 0:
					if pygame.time.get_ticks()<explosions[i].time_create+200:
						explosions[i].animation = 2
					if explosions[i].GodMode_bombe:
						root.blit(explosionGMB0[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					elif explosions[i].GodMode_explosion:
						root.blit(explosionGME0[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					else:
						root.blit(explosion0[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))

				elif explosions[i].orientation == 1:
					if explosions[i].GodMode_bombe:
						root.blit(explosionGMB1[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					elif explosions[i].GodMode_explosion:
						root.blit(explosionGME1[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					else:
						root.blit(explosion1[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))

				elif explosions[i].orientation == 2:
					if explosions[i].GodMode_bombe:
						root.blit(explosionGMB2[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					elif explosions[i].GodMode_explosion:
						root.blit(explosionGME2[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
					else:
						root.blit(explosion2[explosions[i].animation],(explosions[i].pos_x,explosions[i].pos_y))
				
				if pygame.time.get_ticks() > explosions[i].last_animation+explosions[i].delay_animation:
					explosions[i].animation += 1
					explosions[i].last_animation = pygame.time.get_ticks()
		while 1:
			for i in range(0,len(explosions)):
				if explosions[i].active == False:
					del explosions[i]
					break
			break
		
		#Destruction explosion
		for i in range(len(explosions)):
			if explosions[i].active:
				#Mort perso
				if perso[0].last_damage <= pygame.time.get_ticks()-cooldown_damage:
					if (perso[0].pos_x,perso[0].pos_y) == (explosions[i].pos_x,explosions[i].pos_y):
						perso[0].last_damage = pygame.time.get_ticks()
						perso[0].vie -= 1
						if perso[0].vie <= 0:
							perso[0].active = False
				#Destruction Items
				for n in range(len(items)):
					if (items[n].pos_x,items[n].pos_y) == (explosions[i].pos_x,explosions[i].pos_y):
						if pygame.time.get_ticks() - items[n].time_pose >= items[n].resistance:
							items[n].active = False
		
		if not end_game:
			time_sec,time_min = get_time()

		L_temps = F_clock.render("{}:{}".format(time_min,time_sec),1,(0,0,0))
		root.blit(L_temps,(338,642))

		if not end_game:
			temp_now = pygame.time.get_ticks()
			if temp_now > Solo.lancement+Solo.debut:
				if temp_now > Solo.last+Solo.intervalle:
					if temp_now > perso[0].inverse+cooldown_inverse and temp_now > perso[0].bloque+cooldown_bloque:
						temp_random = random()
						if temp_random < 0.01:
							Items.inverse()
							if Solo.intervalle == 200:
								Solo.intervalle += 500
							elif Solo.intervalle < 1000:
									Solo.intervalle + 300
							Solo.intervalle += 500
						elif temp_random < 0.02:
							Items.bloque()
							if Solo.intervalle == 200:
								Solo.intervalle += 500
							elif Solo.intervalle < 1000:
								Solo.intervalle + 300

					if random() < 0.05:
						Solo.spawn_vie()
					Solo.solo_bombes()
					Solo.last = now
					Solo.score += 1
					if Solo.taille < 5:
						if Solo.intervalle > 300:
							Solo.intervalle -= 100
						if Solo.intervalle == 300:
							if Solo.tour == 5:
								Solo.taille += 1
								Solo.tour = 0
								Solo.intervalle = 1500
								Solo.last += Solo.pause
							else:
								Solo.tour += 1
							if Solo.taille == 5:
								perso[0].objet_tenu = 8
					else:
						if Solo.intervalle > 700:
							Solo.intervalle -= 100
						elif Solo.intervalle > 250:
							Solo.intervalle -= 50

		if not perso[0].active:
			end_game = True

		if end_game:
			pos_score_y = 313
			if score_joueur < Solo.score:
				score_joueur += 2
				if score_joueur+1 == Solo.score:
					score_joueur += 1
			if Solo.score < 10:
				pos_score_x = 281
			elif Solo.score < 100:
				pos_score_x = 268
			elif Solo.score < 1000:
				pos_score_x = 254
			elif Solo.score >= 1000:
				pos_score_x = 217
				score_joueur = "OMG !!"

			if score_joueur <= best_score:
				L_score = F_score.render("Score : {}".format(score_joueur),1,(63,63,63))
			else:
				L_score = F_score.render("Score : {}".format(score_joueur),1,(43,175,37))
			L_score_ombre = F_score.render("Score : {}".format(score_joueur),1,(0,0,0))

			root.blit(fin_solo,(0,0))
			root.blit(L_score_ombre,(pos_score_x-1,pos_score_y-1))
			root.blit(L_score,(pos_score_x,pos_score_y))

		#rafraichissement de l'ecran
		pygame.display.flip()
	
	initialisation = True
	while chargement:
		for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				pygame.quit()

		if initialisation:
			donnees_save = pickle.load(open("donnees_save.xbl","rb"))
			#statut_objets
			temp_actif = False
			for i in range(len(donnees_save["objets"])):
				if donnees_save["objets"][i] == True:
					temp_actif = True
			if temp_actif == True:
				if donnees_save["freq_objets"] == "petite":
					statut_objets = "Petite quantitée"
				if donnees_save["freq_objets"] == "normale":
					statut_objets = "Quantitée normale"
				if donnees_save["freq_objets"] == "grande":
					statut_objets = "Grande quantitée"
			else:
				statut_objets = "Désactivés"

			#Spawners
			temp_actif = False
			for i in range(len(donnees_save["objets_spawners"])):
				if donnees_save["objets_spawners"][i] == True:
					temp_actif = True
			if temp_actif == True:
				if donnees_save["freq_spawners"] == "petite":
					statut_spawners = "Petite activitée"
				if donnees_save["freq_spawners"] == "normale":
					statut_spawners = "Activitée normale"
				if donnees_save["freq_spawners"] == "grande":
					statut_spawners = "Grande activitée"
			else:
				statut_spawners = "Désactivés"

			#duree partie
			temp_secs = donnees_save["secs_avt_fin"]%60
			if temp_secs < 10:
				temp_secs = str(temp_secs) + "0"

			#duree partie
			if donnees_save["secs_avt_fin"] >= 60:
				temp_duree_partie = str(int(donnees_save["secs_avt_fin"]/60))+" min "+str(temp_secs)
			elif donnees_save["secs_avt_fin"] < 60:
				temp_duree_partie = str(temp_secs) + " sec"
			else:
				temp_duree_partie = "Infinie"

			#mort subite
			if donnees_save["mort_subite"]:
				status_mort_subite = "Activée"
			else:
				status_mort_subite = "Desactivée"

			L_nb_joueurs = F_chargement.render("-Nombre de joueurs : {}".format(donnees_save["nb_joueurs"]),1,(0,0,0))
			L_vies = F_chargement.render("-Vie(s) : {}".format(donnees_save["vie_depart"]),1,(0,0,0))
			L_objets = F_chargement.render("-Objets : {}".format(statut_objets),1,(0,0,0))
			L_spawners = F_chargement.render("-Spawners : {}".format(statut_spawners),1,(0,0,0))
			L_duree_partie = F_chargement.render("-Durée de la partie : {}".format(temp_duree_partie),1,(0,0,0))
			L_mort_subite = F_chargement.render("-Mort subite : {}".format(status_mort_subite),1,(0,0,0))

			start = pygame.time.get_ticks()
			temps_de_charge = 3000

			initialisation = False

		if pygame.time.get_ticks() < start+temps_de_charge:
			barre_chargement_x = start+temps_de_charge - pygame.time.get_ticks()
			barre_chargement_x = 540-540*barre_chargement_x/temps_de_charge
		else:
			if donnees_save["nb_joueurs"] == 1:
				perso,blocks,items,background,end_game,score_joueur,best_score = lancer_partie_1joueur()
			else:
				perso,blocks,items,spawners,background,end_game,time_end,mort_subite = lancer_partie()
			partie_en_cours = True
			chargement = False

		#collage

		root.blit(background_chargement,(0,0))
		root.blit(barre_chargement_fill,(105+barre_chargement_x,675))
		root.blit(barre_chargement,(100,668))

		if donnees_save["nb_joueurs"] != 1:
			root.blit(L_nb_joueurs,(140,160))
			root.blit(L_vies,(140,240))
			root.blit(L_objets,(140,320))
			root.blit(L_spawners,(140,400))
			root.blit(L_duree_partie,(140,480))
			root.blit(L_mort_subite,(140,560))
		else:
			L_meilleur_score = F_meilleur_score.render("Meilleur score : {}".format(donnees_save["best_score"]),1,(0,0,0))
			if donnees_save["best_score"] < 10:
				root.blit(L_meilleur_score,(230,400))
			elif donnees_save["best_score"] < 100:
				root.blit(L_meilleur_score,(220,400))
			elif donnees_save["best_score"] > 100:
				if donnees_save["best_score"] >= 1000:
					donnees_save["best_score"] = 999
				root.blit(L_meilleur_score,(210,400))
			root.blit(L_nb_joueurs,(170,320))

		#rafrechissement de l'ecran
		pygame.display.flip()
