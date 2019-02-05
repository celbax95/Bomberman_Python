import pygame
from pygame.locals import *

#images jeu

#Persos
persoS = []
persoB = []
persoV = []
persoBV = []

persoS.append(pygame.image.load("images_jeu/persos/perso1/perso1S.png").convert_alpha())
persoB.append(pygame.image.load("images_jeu/persos/perso1/perso1B.png").convert_alpha())
persoV.append(pygame.image.load("images_jeu/persos/perso1/perso1V.png").convert_alpha())
persoBV.append(pygame.image.load("images_jeu/persos/perso1/perso1BV.png").convert_alpha())

persoS.append(pygame.image.load("images_jeu/persos/perso2/perso2S.png").convert_alpha())
persoB.append(pygame.image.load("images_jeu/persos/perso2/perso2B.png").convert_alpha())
persoV.append(pygame.image.load("images_jeu/persos/perso2/perso2V.png").convert_alpha())
persoBV.append(pygame.image.load("images_jeu/persos/perso2/perso2BV.png").convert_alpha())

persoS.append(pygame.image.load("images_jeu/persos/perso3/perso3S.png").convert_alpha())
persoB.append(pygame.image.load("images_jeu/persos/perso3/perso3B.png").convert_alpha())
persoV.append(pygame.image.load("images_jeu/persos/perso3/perso3V.png").convert_alpha())
persoBV.append(pygame.image.load("images_jeu/persos/perso3/perso3BV.png").convert_alpha())

persoS.append(pygame.image.load("images_jeu/persos/perso4/perso4S.png").convert_alpha())
persoB.append(pygame.image.load("images_jeu/persos/perso4/perso4B.png").convert_alpha())
persoV.append(pygame.image.load("images_jeu/persos/perso4/perso4V.png").convert_alpha())
persoBV.append(pygame.image.load("images_jeu/persos/perso4/perso4BV.png").convert_alpha())

#Etats perso
perso_inverse = pygame.image.load("images_jeu/persos/etats/perso_inverse.png").convert_alpha()
perso_bloque = pygame.image.load("images_jeu/persos/etats/perso_bloque.png").convert_alpha()

#Backgrounds
backgroundp1 = pygame.image.load("images_jeu/backgrounds/backgroundp1.png").convert() #Image fond 4 joueurs
backgroundp2 = pygame.image.load("images_jeu/backgrounds/backgroundp2.png").convert() #Image fond 4 joueurs
backgroundp3 = pygame.image.load("images_jeu/backgrounds/backgroundp3.png").convert() #Image fond 4 joueurs
backgroundp4 = pygame.image.load("images_jeu/backgrounds/backgroundp4.png").convert() #Image fond 4 joueurs
backgroundp2s = pygame.image.load("images_jeu/backgrounds/backgroundp2s.png").convert() #Image fond 4 joueurs + spawners
backgroundp3s = pygame.image.load("images_jeu/backgrounds/backgroundp3s.png").convert() #Image fond 4 joueurs + spawners
backgroundp4s = pygame.image.load("images_jeu/backgrounds/backgroundp4s.png").convert() #Image fond 4 joueurs + spawners

#Decors
brick = pygame.image.load("images_jeu/brick.png").convert() #Image blocks
gagne = pygame.image.load("images_jeu/gagne.png").convert_alpha() #Image gagne
fin_temps = pygame.image.load("images_jeu/fin_temps.png").convert_alpha() #Image fin_temps
fin_solo = pygame.image.load("images_jeu/fin_solo.png").convert_alpha() #Image fin_solo

#Bombes
bombe = [pygame.image.load("images_jeu/bombes/bombe_0.png").convert_alpha(), pygame.image.load("images_jeu/bombes/bombe_1.png").convert_alpha()]
bombeGMB = [pygame.image.load("images_jeu/bombes/bombeGMB_0.png").convert_alpha(), pygame.image.load("images_jeu/bombes/bombeGMB_1.png").convert_alpha()]
bombeGME = [pygame.image.load("images_jeu/bombes/bombeGME_0.png").convert_alpha(), pygame.image.load("images_jeu/bombes/bombeGME_1.png").convert_alpha()]

#Explosions
explosion0 = [pygame.image.load("images_jeu/explosion/explosion/explosion0_0.png").convert_alpha(), 
pygame.image.load("images_jeu/explosion/explosion/explosion0_1.png").convert_alpha(),
pygame.image.load("images_jeu/explosion/explosion/boom.png").convert_alpha()
]
explosion1 = [pygame.image.load("images_jeu/explosion/explosion/explosion1_0.png").convert_alpha(), pygame.image.load("images_jeu/explosion/explosion/explosion1_1.png").convert_alpha()]
explosion2 = [pygame.image.load("images_jeu/explosion/explosion/explosion2_0.png").convert_alpha(), pygame.image.load("images_jeu/explosion/explosion/explosion2_1.png").convert_alpha()]

explosionGMB0 = [pygame.image.load("images_jeu/explosion/explosionGMB/explosionGMB0_0.png").convert_alpha(), 
pygame.image.load("images_jeu/explosion/explosionGMB/explosionGMB0_1.png").convert_alpha(),
pygame.image.load("images_jeu/explosion/explosionGMB/boom.png").convert_alpha()
]
explosionGMB1 = [pygame.image.load("images_jeu/explosion/explosionGMB/explosionGMB1_0.png").convert_alpha(), pygame.image.load("images_jeu/explosion/explosionGMB/explosionGMB1_1.png").convert_alpha()]
explosionGMB2 = [pygame.image.load("images_jeu/explosion/explosionGMB/explosionGMB2_0.png").convert_alpha(), pygame.image.load("images_jeu/explosion/explosionGMB/explosionGMB2_1.png").convert_alpha()]

explosionGME0 = [pygame.image.load("images_jeu/explosion/explosionGME/explosionGME0_0.png").convert_alpha(), 
pygame.image.load("images_jeu/explosion/explosionGME/explosionGME0_1.png").convert_alpha(),
pygame.image.load("images_jeu/explosion/explosionGME/boom.png").convert_alpha()
]
explosionGME1 = [pygame.image.load("images_jeu/explosion/explosionGME/explosionGME1_0.png").convert_alpha(), pygame.image.load("images_jeu/explosion/explosionGME/explosionGME1_1.png").convert_alpha()]
explosionGME2 = [pygame.image.load("images_jeu/explosion/explosionGME/explosionGME2_0.png").convert_alpha(), pygame.image.load("images_jeu/explosion/explosionGME/explosionGME2_1.png").convert_alpha()]


#items
explosion_plus = pygame.image.load("images_jeu/items/explosion_plus.png").convert_alpha()
blocks_5 = pygame.image.load("images_jeu/items/blocks_5.png").convert_alpha()
bombes_5 = pygame.image.load("images_jeu/items/bombes_5.png").convert_alpha()

random_bombes = pygame.image.load("images_jeu/items/random_bombes.png").convert_alpha()
armure = pygame.image.load("images_jeu/items/armure.png").convert_alpha()
random_blocks = pygame.image.load("images_jeu/items/random_blocks.png").convert_alpha()
inverse = pygame.image.load("images_jeu/items/inverse.png").convert_alpha()
bloque = pygame.image.load("images_jeu/items/bloque.png").convert_alpha()

teleport = pygame.image.load("images_jeu/items/teleport.png").convert_alpha()
GodMode_bombe = pygame.image.load("images_jeu/items/GodMode_bombe.png").convert_alpha()
GodMode_explosion = pygame.image.load("images_jeu/items/GodMode_explosion.png").convert_alpha()

item_actif = pygame.image.load("images_jeu/items/item_actif.png").convert_alpha()
item_none = pygame.image.load("images_jeu/items/item_none.png").convert_alpha()

############################################################################################################################################################

#images menu

background_menu = pygame.image.load("images_menu/background_menu.png").convert_alpha()

#pages
I_acceuil = pygame.image.load("images_menu/Vacceuil.png").convert_alpha()
I_jouer = pygame.image.load("images_menu/Vjouer.png").convert_alpha()
I_nb_joueurs = pygame.image.load("images_menu/Vnb_joueurs.png").convert_alpha()
I_parametres = pygame.image.load("images_menu/Vparametres.png").convert_alpha()
I_stats = pygame.image.load("images_menu/Vstats.png").convert_alpha()
I_objets = pygame.image.load("images_menu/Vobjets.png").convert_alpha()
I_spawners = pygame.image.load("images_menu/Vspawners.png").convert_alpha()
I_fin = pygame.image.load("images_menu/Vfin.png").convert_alpha()

#selecteurs
S_nb_joueurs = pygame.image.load("images_menu/selecteurs/Snb_joueurs.png").convert_alpha()
S_tableau_objets = pygame.image.load("images_menu/selecteurs/Stableau_objets.png").convert_alpha()
S_stats_vie = pygame.image.load("images_menu/selecteurs/Sstats_vie.png").convert_alpha()
S_freq_PNG = pygame.image.load("images_menu/selecteurs/Sfreq_PNG.png").convert_alpha()
S_fin_mort_subite = pygame.image.load("images_menu/selecteurs/Sfin_mort_subite.png").convert_alpha()

#bouton
B_reinitialiser_score = pygame.image.load("images_menu/B_reinitialiser_score.png").convert_alpha()

#aide
aide0 = pygame.image.load("images_menu/aide/aide0.png").convert_alpha()
aide1 = pygame.image.load("images_menu/aide/aide1.png").convert_alpha()
aide2 = pygame.image.load("images_menu/aide/aide2.png").convert_alpha()
aide3 = pygame.image.load("images_menu/aide/aide3.png").convert_alpha()
aide4 = pygame.image.load("images_menu/aide/aide4.png").convert_alpha()
aide5 = pygame.image.load("images_menu/aide/aide5.png").convert_alpha()
aide6 = pygame.image.load("images_menu/aide/aide6.png").convert_alpha()
S_fleche_gauche = pygame.image.load("images_menu/aide/S_fleche_gauche.png").convert_alpha()
S_fleche_droite = pygame.image.load("images_menu/aide/S_fleche_droite.png").convert_alpha()

#chargement
background_chargement = pygame.image.load("images_menu/chargement/background_chargement.png").convert_alpha()
barre_chargement = pygame.image.load("images_menu/chargement/barre_chargement.png").convert_alpha()
barre_chargement_fill = pygame.image.load("images_menu/chargement/barre_chargement_fill.png").convert_alpha()

#autres
S_min = pygame.image.load("images_menu/selecteurs/S_min.png").convert_alpha()