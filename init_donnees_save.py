import pickle

donnees_save = {
	"nb_joueurs":4,
	"objet_depart":0,
	"vie_depart":0,
	"taille_explosion_depart":1,
	"objets":[True,True,True,True,True,True,True,True,True,True,True],
	"freq_objets":"normale",
	"objets_spawners":[True,True,True,True,True,True,True,True,True,True,True],
	"secs_avt_spawners":0,
	"freq_spawners":"normale",
	"secs_avt_fin":0,
	"mort_subite":"non",
	"best_score":0
	"fullscreen":False
}

pickle.dump(donnees_save,open("donnees_save.xbl","wb"))