"""@package AP@LZ_classificateur
Ce module contient le programme principal du classificateur d'activité d'AP@LZ
"""
__author__ = 'Rémi Carpentier'
__file__ = './AP@LZ_classificateur.py'
__name__ = 'AP@LZ_classificateur'
__version__ = '1.0'
#importer les bibliothèques nécessaires
import sqlite3
import copy
import msvcrt
import os
#importer les classes
from Arbre import Arbre
from Log import Log
from Activity import Activity
#importer les bibliothèques pour l'arbre de décision
from sklearn.feature_extraction import DictVectorizer
from sklearn import tree
#importer les bibliothèques nécessaires pour enregistrer et charger les données.
import pickle
import time
#Définir les fonctions
def apprendre():	
	# Initialiser les classes d'activités
	while(True):
		nb_classes = int(input("Quel est le nombre de classifications que vous désirez? ( >0)\t"))
		if nb_classes > 0:
			break
	mesClasses = [[] for k in range(nb_classes)]
	# Structure de donnée permettant de connaître quelle numéro
	# font partie de quelle classe
	numClasses = copy.deepcopy(mesClasses)
	arbreClasses = [None for k in range(nb_classes)]
	# Emmagasiner les données
	# 1- Séquencer les logs en "bout de log"/Activité
	activities = sectionner()
	# 2- Associer chaque activité à une classe
	print("\nNous avons trouvé ", len(activities), "activités. Veuillez entrer, pour"
		  " chaque activité, un numéro de classe où '0' est la première classe.\n")
	print("Pour chaque classe différente, incrémenter de 1.\n"
		  "'s' : Si vous ne connaissez pas la classe du \"bout de log\", "
		  "peser sur 's' pour afficher la séquence d'action du \"bout de log\".\n"
		  "'backspace' : Si vous avez fait une erreur, peser sur 'backspace' pour "
		  "recommencer la dernière entrée autant de fois que nécessaire.\n"
		  "'c' : Pour rentrer un numéro de classe de 2 chiffres et plus, "
		  "peser sur 'c'.")
	# 2- Entraîné mes listes/arbres/types d'activité
	# 	2.1 - Trouver pour chaque activité, quel classe lui est associé
	# 	Affichage et entrer des associations des classes et des "bouts de logs" par 
	#	l'utilisateur
	asso = associer(activities, nb_classes)
	# Rassembler les mêmes numéros ensembles
	for num in range(nb_classes):
		for nb in range(len(asso)):
			if asso[nb] == num:
				numClasses[num].append(nb)	
	# 	2.2 - Faire un arbre pour les mêmes numéros
	arbre = []
	arbreClassesSelonAction = []
	apparitionListe = []
	for pos in range(len(arbreClasses)):
		arborescence(activities, numClasses[pos], 0, arbre)
		if arbre[0]:
			arbreClasses[pos] = copy.deepcopy(Arbre(arbre, activities))
			arbre.clear()
	# 5- Créer l'arbre de décision
	arbre, noms = decision_tree(activities, asso, arbreClasses)
	return arbreClasses, activities, asso, arbre, noms
	
def arborescence(mesListes, mesNumeros, maPosition, monArbre):
	"""	Fonction qui prend des listes 
	
			@param	mesListes	Tableau contenant tous les objets.
					mesNuméros	Tableau contenant les numéros à associés.
					maPosition	Profondeur dans l'arbre
					monArbre	Liste vide que l'on transforme en arbre avec 
								les données reçues en paramètre.
			"""
	print(" ***** TOUR ", maPosition, "*****")
	mesChiffres = []
	indices = []
	mesNouveauxNumeros = []
	check = {}
	#1-Compter les différentes possibilitées
	# 1.1 Si on a plusieurs listes, on compte les différentes possibilitées
	if type(mesNumeros) == list:
		for monNumero in mesNumeros:
			if not mesListes[monNumero][maPosition] in mesChiffres:
				mesChiffres.append(mesListes[monNumero][maPosition])
	# 1.2 Si on a qu'un numéro, alors il n'y a rien à comparer
	#		On retourne la liste de mesNumeros
	elif type(mesNumeros) == int and type(mesListes[0]) == list:
		return mesListes[mesNumeros]
	elif type(mesNumeros) == int and type(mesListes[0]) == int:
		return mesListes
	#2-Rassembler les listes qui ont le même élément
	for chiffre in mesChiffres:
		for monNumero in mesNumeros:
			if mesListes[monNumero][maPosition] == chiffre and (maPosition+1) != len(mesListes[monNumero]):
				indices.append(monNumero)
			elif mesListes[monNumero][maPosition] == chiffre and chiffre not in check:
				check[chiffre] = [monNumero]
			elif mesListes[monNumero][maPosition] == chiffre and chiffre in check:
				check[chiffre].append(monNumero)
		if indices:
			mesNouveauxNumeros.append(indices.copy())
			indices.clear()
	#3- Insérer dans l'arbre
	# S'assurer que l'on insère pas plus loin que la longueur de l'arbre
	if len(monArbre) <= maPosition:
		monArbre.append([])
	# Insérer les noeuds (qui auront des branches)
	monArbre[maPosition].extend(mesNouveauxNumeros)
	# Insérer les feuilles (fin de l'arbre)
	for keys in check:
		monArbre[maPosition].append(check[keys])
	# 4 - Si on a des noeuds, on fait l'appel récursif pour chaque noeud
	if mesNouveauxNumeros:
		for i in mesNouveauxNumeros:
			arborescence(mesListes, i, maPosition + 1, monArbre)

def associer(activities, nb_classes):
	"""	Fonction servant à demander à l'utilisateur d'associer les activités à 
		une classe.
			
			@return	association	Tableau d'association où la position dans le 
								tableau est le numéro de l'activité et la 
								valeur, la classe propre de l'activité.
		"""
	num = 0
	association = []
	while(num < len(activities)):
		while(True):
			key = msvcrt.kbhit()
			if key:
				asso = str(msvcrt.getch())
				asso = asso[2:-1]
				if asso.isdigit():
					num_asso = int(asso)
					if 0 <= num_asso and num_asso < nb_classes:
						association.append(num_asso)
						num += 1
						break
					else:
						print("La classe que vous avez entrée n'est pas "
							  "valide, car le numéro dépasse le nombre de "
							  "classifications possibles.")
				else:
					if asso == "\\x08":
						association.pop(-1)
						os.system('clear')
						num -= 1
						break
					elif asso == "s":
						print(activities[num].sequence_action)
					elif asso == "c":
						num_asso = int(input())
						if num_asso < nb_classes:
							association.append(num_asso)
							num += 1
							break
						else:
							print("La classe que vous avez entrée n'est pas " 
								  "valide, car le numéro dépasse le nombre "
								  "de classifications possibles.")
			else:
				for i in ["/","-","|","\\","|"]:
					for j in association:
						print("%s-" %j, end="")
					print("\b", end="")
					print("%s\r" %i, end="")
	for j in association:
		print("%s-" %j, end="")
	print("\b")
	return association

def categoriser(activite, mesClasses):
	""" Fonction qui sert à catégoriser mes données du "test d'entrainement" 
		afin d'avoir des arbres qui ont appris.

			@param 	activite Un "bout de log"
					mesClasses Contient tous les types d'activités désirés
			@return	tab_comparaison.index(temp)	Le numéro de la classe à 
												laquelle on a associée 
												l'activité
			"""
	cmp = 0
	pos = 0
	tab_comparaison = [[] for k in range(len(mesClasses))]
	for uneClasse in mesClasses:
		for action in range(0, len(activite)):
			if pos < len(uneClasse) and activite[action] == uneClasse[pos]:
				cmp += 1
				pos += 1
			elif pos >= len(uneClasse):
				cmp = cmp/len(activite)
				tab_comparaison[mesClasses.index(uneClasse)].append(cmp)
				cmp = 0
				pos = 0
	temp = max(tab_comparaison)
	if tab_comparaison.count(temp) == 1:
		return tab_comparaison.index(temp)
	else:
		print("Cette activité a été mal classés : \n\t", activite)
		print("Voici les valeurs de comparaisons" +
			  "selon les numéros classes : ", tab_comparaison)
		return None

def classification(une_activite, mesArbresFinaux):
	""" Fonction qui sert à classifier une nouvelle activite parmi les arbres 
		déjà appris.

			@param 	une_activite	Un nouveau "bout de log"
					mesArbresFinaux	Contient tous les arbres appris de chaque classe
			@return	classification	Le numéro de la classe à laquelle on a classifié 
									l'activité, peut être plusieurs classes si la 
									comparaison a été équivalente plus d'une fois.
			"""
	per_cmp = [None for k in range(len(mesArbresFinaux))]

	for monArbreFinal in mesArbresFinaux:
		cmp = comparaison(une_activite, copy.deepcopy(monArbreFinal))

		per_cmp[mesArbresFinaux.index(monArbreFinal)] = cmp/len(une_activite)

	temp_max = max(per_cmp)
	if per_cmp.count(temp_max) == 1:
		classification = per_cmp.index(temp_max)
	else:
		classification = [num_classe for num_classe in range(len(per_cmp)) if per_cmp[num_classe] == temp_max]
	return classification

def comparaison(une_activite, monArbreFinal):
	""" Fonction qui sert à comparer une nouvelle activite parmi un seul arbre 
		déjà appris.

			@param 	une_activite	Un nouveau "bout de log"
					monArbreFinal	un des arbres déjà appris d'une des classes
			@return	cmp	Le nombre de comparaison ordonnée qui est apparue entre la
						nouvelle activitée et une branche de l'arbre final.
			"""
	pos = 0
	cmp = 0
	noeud_a_enlever = []
	for profondeur in monArbreFinal.arbre:
			for noeud in profondeur:
				if monArbreFinal.activities[noeud[0]][monArbreFinal.arbre.index(profondeur)] == une_activite[pos]:

					cmp += 1
					if pos < len(une_activite) - 1:
						pos += 1
					else:
						return cmp

					num_a_enlever = [x for x in profondeur if x != noeud]
					for num in num_a_enlever:
						noeud_a_enlever.extend(num)
					monArbreFinal = monArbreFinal.remove(noeud_a_enlever)
	return cmp

def decision_tree(activities, Y, arbreClasses):
	"""	Fonction qui crée l'arbre de décision avec la biliothèque
		scikit-learn selon la mesure de dispersion.
	
			@param	activities	La liste contenant les numéros et les valeurs.
					Y	Tableau des associations entre activités et classes.
					arbreClasses	Tableau contenant l'arbre type de chaque
									classe.
			@return arbre	L'arbre de décision.
					noms	Le nombre d'élément considéré par l'arbre de 
							décision.
			"""
	vec = DictVectorizer()

	tab = []
	while(True):
		commande = input("Désirez-vous utilisez la dispersion des activités (d)"
						 " ou la dispersion des arbres (r)?\t")
		if commande == "d":
			for act in activities:
				tab.append(copy.deepcopy(act.dispersion))
			
			resultats = vec.fit_transform(tab).toarray()
			noms = vec.get_feature_names()
			
			arbre = tree.DecisionTreeClassifier()
			arbre = arbre.fit(resultats, Y)
			break
		elif commande == "r":
			for arbreFinal in arbreClasses:
				tab.append(copy.deepcopy(arbreFinal.dispersion))
				
			W = []
			for i in range(len(arbreClasses)):
				W.append(i)
			
			resultats = vec.fit_transform(tab).toarray()
			noms = vec.get_feature_names()
			
			arbre = tree.DecisionTreeClassifier()
			arbre = arbre.fit(resultats, W)
			break
	
	return arbre, noms

def nouvelle_activite(une_activite, noms_attributs):
	"""	Fonction qui transforme une activité pour qu'elle soit utilisable par 
		l'arbre de décision.
	
			@param	une_activite	La nouvelle activité à classifier.
					noms_attributs	Nombre d'élément considéré par 
									l'arbre de décision.
			@return test	Tableau contenant les données sous forme de 
							nombre à virgule flotante.
					test_noms	Tableau contenant les noms des attributs.
			"""
	vec = DictVectorizer()
	for nom in noms_attributs:
		if not nom in une_activite.dispersion:
			une_activite.dispersion[nom] = 0
	test = vec.fit_transform(une_activite.dispersion).toarray()
	test_noms = vec.get_feature_names()
	return test, test_noms

def numero_a_valeur(arbre, activities):
	"""	Fonction remplace les numéros de l'arbre par leurs valeurs.
	
			@param	arbreClassesSelonNumero	Arbre contenant les numéros.
					activities	La liste contenant les numéros et les valeurs.
			@return arbre_val	L'arbre contenant les valeurs.
			"""
	arbre_val = copy.deepcopy(arbre)
	for profondeur in arbre_val:
		for noeud in profondeur:
			for list in noeud:
				arbre_val[arbre_val.index(profondeur)][profondeur.index(noeud)]\
				[noeud.index(list)] = activities[list][arbre_val.index(profondeur)]
	return arbre_val
	
def sectionner():
	"""	Fonction qui sépare les logs en Activité.
			
			@return	activities Un tableau contenant toutes les activités.
		"""
	# Connaître le nom du fichier bd à ouvrir
	nom_bd = input("Quel est le nom du fichier contenant la base de données?"
					" Ajoutez l'extension du fichier (.db)\t")
	# Connexion à la base de données
	conn = sqlite3.connect(nom_bd)
	# Création d'un pointeur sql
	c = conn.cursor()
	c1 = conn.cursor()
	# Sélectionner mes données
	c = conn.execute("SELECT * FROM logging")
	# Tableau qui va contenir la séquence d'action
	activity = []
	# Tableau qui va contenir toutes les activités
	activities = []
	# Tableau qui va contenir temporairement tous les logs
	tous_les_logs = []
	for log in c:
		#Créer le log et l'ajouter à mon tableau
		tous_les_logs.append(Log(log))
	# Pour chaque log, regarder si on a une condition d'arrêt
	for log in range(len(tous_les_logs)):
		# Ajouter l'action à l'activité
		activity.append(tous_les_logs[log])
		# Conditions d'arrêts
		if tous_les_logs[log].rclass_name == "footer_back_button" or \
		   tous_les_logs[log].rclass_name == "CalendarFullDateValue" or \
		   tous_les_logs[log].rclass_name == "appointment_details_delete_confirm_yes_button" or \
		   tous_les_logs[log].rclass_name == "appointment_details_realize_button":
			temp_activity = Activity(activity)
			activities.append(copy.deepcopy(temp_activity))
			activity.clear()
		#log+1 peut causer un bug si c'est le dernier log de la liste
		elif tous_les_logs[log].rclass_name == "footer_center_button" and \
			 tous_les_logs[log+1].activity_name == "ApalzActivity":
				temp_activity = Activity(activity)
				activities.append(copy.deepcopy(temp_activity))
				activity.clear()
		elif (tous_les_logs[log].timestamp - tous_les_logs[log-1].timestamp) >= 60000:
			temp_activity = Activity(activity)
			activities.append(copy.deepcopy(temp_activity))
			activity.clear()
	return activities
	
def valeur_a_numero(arbre, activities):
	"""	Fonction remplace les valeurs de l'arbre par leurs numéros.
	
			@param	arbreClassesSelonAction	Arbre contenant les valeurs.
					activities	La liste contenant les numéros et les valeurs.
			@return L'arbre contenant les numéros.
			"""
	activites = [x for x in range(len(activities)) if activities[x].sequence_action[0] == arbre[0][0][0]]
	arbre_num = []
	arborescence(activities, activites, 0, arbre_num)
	return arbre_num

# Classifier un nouveau "bout de log"
while(True):
	print(	"\t0 : apprentissage d'un nouvel arbre.\n"
			"\t","*"*10,"CLASSIFICATION SELON L'ARBRE DE DÉCISION SELON DISPERSION DE L'ACTIVITÉ","*"*10,"\n\n"
			"\t1 : Classifier une activitée de vos activités d'une de vos listes.\n"
			"\t2 : Classifier plusieurs activités d'une nouvelle base de données.\n"
			"\t","*"*10,"CLASSIFICATION SELON L'ARBRE DE DÉCISION SELON LA DISPERSION DE L'ARBRE","*"*10,"\n\n"
			"\t3 : Classifier une activitée de vos activités d'une de vos listes.\n"
			"\t4 : Classifier plusieurs activités d'une nouvelle base de données.\n"
			"\t","*"*10,"CLASSIFICATION SELON LA SÉQUENCE D'ACTION","*"*10,"\n\n"
			"\t5 : Classifier une activitée de vos activités d'une de vos listes.\n"
			"\t6 : Classifier plusieurs activités d'une nouvelle base de données.\n"
			"\t","*"*10,"ENREGISTREMENT/CHARGEMENT","*"*10,"\n\n"
			"\t7 : sauvegarder l'arbre de décision.\n"
			"\t8 : Charger un arbre de décision.\n"
			"\t9 : Quitter.\n")
	commande = input("Quel est la prochaine ligne de commande?\t")
	if commande == "0":
		arbreClasses, activities, association, arbre, noms = apprendre()
	elif commande == "1":
		while(True):
			num = int(input("Entrez le numéro de l'activité (entre 0 et " \
					  + str(len(activities)-1) + ") : "))
			if 0 <= num and num < len(activities):
				break
		activite = copy.deepcopy(activities[num])
		test, test_noms = nouvelle_activite(activite, noms)
		reponse = arbre.predict(test)
		print(reponse)
		print("\nPour Classifier selon une autre liste, quitter, puis appeler "
			  "la fonction x,y = nouvelle_activite(Activity, noms), puis "
			  "utiliser la fonction predict(x) pour obtenir la réponse.\n")
	elif commande == "2":
		temp_activities = sectionner()
		pred_activite = []
		pred_test = []
		pred_test_noms = []
		for act in temp_activities:
			test, test_noms = nouvelle_activite(act, noms)
			pred_activite.append(act)
			pred_test.append(test)
			pred_test_noms.append(test_noms)
		try:
			for i in range(len(pred_test)):
				reponse = arbre.predict(pred_test[i])
				print("Pour l'activité :\n", temp_activities[i].sequence_action, \
					  "\n***** La classification a été identifié à la classe ", \
					  reponse)
			continue
		except:
			print("L'arbre de décision est biaisé. Ceci est probablement dû "
				  "au fait que des boutons se sont ajoutés.\nDésirez-vous "
				  "entraîner un autre arbre de décision qui incluera les "
				  "boutons?")
			if not input("Pesez sur entrée pour continue\t"):
				erreur_disp = temp_activities[i].dispersion
				temp_erreur_disp = copy.deepcopy(erreur_disp)
				for act in activities:
					for key in erreur_disp:
						if key not in act.dispersion:
							act.dispersion[key] = 0
						else:
							del temp_erreur_disp[key]
					erreur_disp = copy.deepcopy(temp_erreur_disp)
				arbre, noms = decision_tree(activities, association, arbreClasses)
			else:
				break	
	elif commande == "3":
		while(True):
			num = int(input("Entrez le numéro de l'activité (entre 0 et " \
					  + str(len(activities)-1) + ") : "))
			if 0 <= num and num < len(activities):
				break
		activite = copy.deepcopy(activities[num])
		test, test_noms = nouvelle_activite(activite, noms)
		reponse = arbre.predict(test)
		print(reponse)
		print("\nPour Classifier selon une autre liste, quitter, puis appeler "
			  "la fonction x,y = nouvelle_activite(Activity, noms), puis "
			  "utiliser la fonction predict(x) pour obtenir la réponse.\n")
	elif commande == "4":
		temp_activities = sectionner()
		pred_activite = []
		pred_test = []
		pred_test_noms = []
		for act in temp_activities:
			test, test_noms = nouvelle_activite(act, noms)
			pred_activite.append(act)
			pred_test.append(test)
			pred_test_noms.append(test_noms)
		try:
			for i in range(len(pred_test)):
				reponse = arbre.predict(pred_test[i])
				print("Pour l'activité :\n", temp_activities[i].sequence_action, \
					  "\n***** La classification a été identifié à la classe ", \
					  reponse)
			continue
		except:
			print("L'arbre de décision est biaisé. Ceci est probablement dû "
				  "au fait que des boutons se sont ajoutés.\nDésirez-vous "
				  "entraîner un autre arbre de décision qui incluera les "
				  "boutons?")
			if not input("Pesez sur entrée pour continue\t"):
				erreur_disp = temp_activities[i].dispersion
				temp_erreur_disp = copy.deepcopy(erreur_disp)
				for arb in arbreClasses:
					for key in erreur_disp:
						if key not in arb.dispersion:
							arb.dispersion[key] = 0
						else:
							del temp_erreur_disp[key]
					erreur_disp = copy.deepcopy(temp_erreur_disp)
				arbre, noms = decision_tree(activities, association, arbreClasses)
			else:
				break	
	elif commande == "5":
		print("\n\nQuitter et appeler la fonction classification : "
			  "classification(Activity, [ Arbre ])\n\n")
	elif commande == "6":
		temp_activities = sectionner()
		for num in range(len(temp_activities)):
			reponse = classification(temp_activities[num], arbreClasses)
			print("L'activité numéro", num, "a été classé", reponse)
	elif commande == "7":
		temps = time.strftime("#%Y-%m-%d_%Hh%Mmin%Ssec")
		
		nom_fichier = "arbre_de_decision" + temps
		fichier_objet = open(nom_fichier, 'wb')
		pickle.dump(arbre, fichier_objet)
		fichier_objet.close()
		
		nom_fichier = "classe_arbre_finaux" + temps
		fichier_objet = open(nom_fichier, 'wb')
		pickle.dump(arbreClasses, fichier_objet)
		fichier_objet.close()
		
		nom_fichier = "activites" + temps
		fichier_objet = open(nom_fichier, 'wb')
		pickle.dump(activities, fichier_objet)
		fichier_objet.close()
		print("Sauvegarde réussi.\n")
		print("Un fichier contient l'arbre de décision tandis que l'autre "
			  "contient les structures d'arborescence servant à classifier "
			  "les nouvelles activititées selon l'ordre des logs. Il doit "
			  "être relié au fichier activité qui contient les informations "
			  "sur lesdites activités de ces structures.")
	elif commande == "8":
		nom_fichier = input("Quel est le nom du fichier contenant l'arbre de désicion?\t")
		temps = "#" + nom_fichier.partition("#")[2]
		
		fichier_objet = open(nom_fichier, 'rb')
		arbre_decision = pickle.load(fichier_objet)
		fichier_objet.close()
		
		fichier_objet = open("classe_arbre_finaux" + temps, 'rb')
		struc_arb = pickle.load(fichier_objet)
		fichier_objet.close()
		
		fichier_objet = open("activites" + temps, 'rb')
		info_activites = pickle.load(fichier_objet)
		fichier_objet.close()
		print("Chargement réussi.\n")
		print("Votre arbre de décision a été assigné à la variable 'arbre_decision'.\n"
			  "Les structures d'arborescences ont été assignées à la variable "
			  "'struc_arb'.\nLes activités ont été assignées à la variable "
			  "'info_activites'.")
	if commande == "9":
		break