import pygame
from pygame.locals import *

#MENU
B_menu = [(691,0,59,53),(45,266,135,44),(45,335,107,44),(45,404,181,52)]
B_jouer = [(263,214,224,94),(251,352,248,94),(240,490,269,44),(240,578,268,94),(42,680,169,44)]
B_nb_joueurs = [(156,350,56,77),(283,350,56,77),(411,350,56,77),(538,350,56,77),(42,680,169,44),(293,680,373,41)]
B_parametres = [(199,232,350,94),(298,371,153,44),(259,460,228,44),(231,549,287,44),(42,680,169,44)]
B_stats = [(27,368,28,64),(58,368,28,64),(89,368,28,64),(120,368,28,64),(151,368,28,64),(182,368,28,64),(213,368,28,64),(244,368,28,64),
	(275,368,28,64),(306,368,28,64),(337,368,28,64),(608,479,66,42),(608,524,66,42),(148,565,40,40),(224,565,40,40),(455,663,285,44),(42,680,169,44)]
B_objets = [(206,270,28,64),(237,270,28,64),(268,270,28,64),(299,270,28,64),(330,270,28,64),(361,270,28,64),(392,270,28,64),(423,270,28,64),
	(454,270,28,64),(485,270,28,64),(516,270,28,64),(60,507,207,44),(271,507,207,44),(481,507,207,44),(343,652,285,44),(42,680,169,44) ]
B_spawners = [(206,229,28,64),(237,229,28,64),(268,229,28,64),(299,229,28,64),(330,229,28,64),(361,229,28,64),(392,229,28,64),(423,229,28,64),
	(454,229,28,64),(485,229,28,64),(516,229,28,64),(583,358,66,42),(583,403,66,42),(61,577,207,44),(272,577,207,44),(482,577,207,44),(424,680,285,44),(42,680,169,44)]
B_fin = [(427,337,66,42),(427,382,66,42),(258,552,104,44),(388,552,104,44),(396,665,285,44),(42,680,169,44)]

fleche_aide_d = (602,672,79,30)
fleche_aide_g = (69,672,79,30)
B_aide = [(8,12,169,44)]

reinitialiser_stats = (None,1,1)
reinitialiser_objets = ([True,True,True,True,True,True,True,True,True,True,True],"grande")
reinitialiser_spawners = ([False,False,True,True,True,False,True,True,True,False,False],60,"grande")
reinitialiser_fin = (300,False)

nb_joueurs = None
#temp
temp_f_d = False
temp_f_g = False

#couleur bouton select
couleur_select = (190,190,190)

#JEU
ROOT_X , ROOT_Y = (750,750) #Taille de la fenetre 750x750
temps = None
time_min = 0

time_to_explode = 1500
explosion_time = 500
nb_explosions = -1
explosions = []
perso = []
cooldown_damage = 500

items = []
nb_items = -1
items_max = 200 # normal = 15
cooldown_inverse = 8000
cooldown_bloque = 2500

spawners_activate = 60000
spawners_charge_min = 5000
spawners_charge_max = 6000
spawners = []

perso_gagne = None

pos_4p_objet_tenu = [(178,624),(522,690),(522,624),(178,690)]
pos_4p_objet_tenuS = [(175,621),(519,687),(519,621),(175,687)]
pos_3p_objet_tenu = [(178,643),(522,690),(522,624)]
pos_3p_objet_tenuS = [(175,640),(519,687),(519,621)]
pos_2p_objet_tenu = [(188,656),(512,656)]
pos_2p_objet_tenuS = [(185,653),(509,653)]
pos_1p_objet_tenu = (188,656)

grille = [
	(50,50),(100,50),(150,50),(200,50),(250,50),(300,50),(350,50),(400,50),(450,50),(500,50),(550,50),(600,50),(650,50), #13
	(50,100),(100,100),(150,100),(200,100),(250,100),(300,100),(350,100),(400,100),(450,100),(500,100),(550,100),(600,100),(650,100), #26
	(50,150),(100,150),(150,150),(200,150),(250,150),(300,150),(350,150),(400,150),(450,150),(500,150),(550,150),(600,150),(650,150), #39
	(50,200),(100,200),(150,200),(200,200),(250,200),(300,200),(350,200),(400,200),(450,200),(500,200),(550,200),(600,200),(650,200), #52
	(50,250),(100,250),(150,250),(200,250),(250,250),(300,250),(350,250),(400,250),(450,250),(500,250),(550,250),(600,250),(650,250), #65
	(50,300),(100,300),(150,300),(200,300),(250,300),(300,300),(350,300),(400,300),(450,300),(500,300),(550,300),(600,300),(650,300), #78
	(50,350),(100,350),(150,350),(200,350),(250,350),(300,350),(350,350),(400,350),(450,350),(500,350),(550,350),(600,350),(650,350), #91
	(50,400),(100,400),(150,400),(200,400),(250,400),(300,400),(350,400),(400,400),(450,400),(500,400),(550,400),(600,400),(650,400), #104
	(50,450),(100,450),(150,450),(200,450),(250,450),(300,450),(350,450),(400,450),(450,450),(500,450),(550,450),(600,450),(650,450), #117
	(50,500),(100,500),(150,500),(200,500),(250,500),(300,500),(350,500),(400,500),(450,500),(500,500),(550,500),(600,500),(650,500), #130
	(50,550),(100,550),(150,550),(200,550),(250,550),(300,550),(350,550),(400,550),(450,550),(500,550),(550,550),(600,550),(650,550), #143
]

murs_gris = [14,16,18,20,22,24,40,42,44,46,48,50,66,68,70,72,74,76,92,94,96,98,100,102,118,120,122,124,126,128]

blocksS = [
	2,3,4,5,6,7,8,9,10,
	15,17,19,21,23,
	26,27,28,29,30,31,32,33,34,35,36,37,38,
	39,41,43,47,49,51,
	52,53,54,55,56,57,58,59,60,61,62,63,64,
	65,67,75,77,
	78,79,80,81,82,83,84,85,86,87,88,89,90,
	91,93,95,99,101,103,
	104,105,106,107,108,109,110,111,112,113,114,115,116,
	119,121,123,125,127,
	132,133,134,135,136,137,138,139,140,
	]

#blocksS = [53,54,55,56,57,58,59,60,61,62,63,64,65,67,75,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,93,95,99,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,119,121,123,125,127,132,133,134,135,136,137,138,139,140,]

#blocksS = [2,15,28,47,99] #Blocks pour les tests

blocks_solo = [
	0,1,2,10,11,12,
	13,25,
	26,28,29,30,31,32,33,34,35,36,38,
	41,49,
	54,62,
	67,75,
	80,88,
	93,101,
	104,106,107,108,109,110,111,112,113,114,116,
	117,129,
	130,131,132,140,141,142,

	]

#Pourcentage spawn items

taux_drop_itemsS = [
0.36,#explo+
0.11,#blocks_5
0.11,#bombes_5
0.07,#vie
0.06,#random_bombes
0.06,#random_blocks
0.07,#inverse
0.10,#bloque
0.04,#TP
0.01,#GMB
0.01,#GME
0.75, #dernier de la liste = taux de drop pour n'importe quel item
]

spawners_locations = [(350,200), (250,300), (450,300), (350,400)]

#taux_spawnersS = [
#32,#bombes_5
#8,#vie
#32,#random_bombes
#3,#inverse
#17,#bloque
#8,#TP
#62, #dernier de la liste = taux de drop pour n'importe quel item
#]

taux_spawnersS = [
	0.36,#explo+
	0.11,#blocks_5
	0.11,#bombes_5
	0.07,#vie
	0.06,#random_bombes
	0.06,#random_blocks
	0.07,#inverse
	0.10,#bloque
	0.04,#TP
	0.01,#GMB
	0.01,#GME
	0.60, #dernier de la liste = taux de drop pour n'importe quel item
	]