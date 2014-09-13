"""@package Arbre
Ce module contient la classe Arbre.
"""
__author__ = 'Rémi Carpentier'
__file__ = './Arbre.py'
__name__ = 'Arbre'
__version__ = '1.0'
class Arbre(object):
	def __init__(self, arbre, activities):
		"""	Le constructeur
				@param	self
						arbre	Un arbre en profondeur contenant des noeuds qui 
								contiennent les numéros d'activités ayant les 
								mêmes éléments à ce noeud.
								"""
		def __calcule_min_profondeur__():
			"""	Fonction qui sert à calculer la profondeur minimum de l'arbre.
					@return	La profondeur minimum
					"""
			for profondeur in self.arbre:
				largeur = 0
				for noeud in profondeur:
					largeur += len(noeud)
				if largeur < len(self.arbre[0][0]):
					return self.arbre.index(profondeur)
		def __regroupement__():
			"""	Fonction qui sert à calculer le nombre d'activité qui ont les 
				mêmes boutons au sein de l'arbre pour évaluer l'importance d'un
				bouton.
					@return	regroupement
					"""
			regroupement = {}
			for profondeur in self.arbre:
				for noeud in profondeur:
					nb_act = len(noeud)
					bouton = activities[noeud[0]][self.arbre.index(profondeur)]
					if bouton not in regroupement:
						regroupement[bouton] = nb_act
					else:
						regroupement[bouton] += nb_act
			return regroupement
		
		def __dispersion__():
			"""	Fonction servant à calculer la dispersion de l'arbre, c.-à-d.
				le nombre de fois qu'un même élément de l'arbre	apparaît.
					@return dispersion La dispersion
					"""
			dispersion = {}
			for profondeur in self.arbre:
				for noeud in profondeur:
					if activities[noeud[0]].sequence_action[self.arbre.index(profondeur)] not in dispersion:
						dispersion[activities[noeud[0]].sequence_action[self.arbre.index(profondeur)]] = 1
					else:
						dispersion[activities[noeud[0]].sequence_action[self.arbre.index(profondeur)]] += 1
			return dispersion
			
		self.activites = {x:activities[x] for x in arbre[0][0]}
		self.activities = activities
		self.arbre = arbre
		self.dispersion = __dispersion__()
		self.dispersion_elements = [activities[x].dispersion for x in arbre[0][0]]
		self.min_profondeur = __calcule_min_profondeur__()
		self.max_profondeur = len(arbre)
		self.max_largeur = max([len(x) for x in arbre])
		self.regroupement = __regroupement__()
	def __repr__(self):
		"""	Fonction qui sert à imprimer.
				@param	self
				@return Tous les attributs de l'objet
				"""
		return 	"activites = %s\narbre = %s\ndispersion = %s\n" \
				%(self.activites, self.arbre, self.dispersion) + \
				"dispersion_elements = %s\nmin_profondeur = %s\n" \
				%(self.dispersion_elements, self.min_profondeur) + \
				"max_profondeur = %s\nmax_largeur = %s\n" \
				%(self.max_profondeur, self.max_largeur) + \
				"regroupement = %s\n" \
				%(self.regroupement)

	def __iter__(self):
		yield self

	def __getitem__(self, y):
		return self.arbre[y]
		
	def remove(self, numeros):
		"""	Fonction servant à retirer les noeuds jugées inintéressants
			parmi l'arbre.
				@param	numeros	Les numeros d'activites à retirer de l'arbre
						arbre	Un arbre
				@return	arbre	Le nouvel arbre sans les numéros qui était à enlever
				"""
		for profondeur in self.arbre:
			for noeud in profondeur:
				for num in numeros:
					if num in noeud:
						noeud.remove(num)
			for i in range(profondeur.count([])):
				profondeur.remove([])
		for i in range(self.arbre.count([])):
			self.arbre.remove([])
		return self
		
	def apparition(self):
		"""	Fonction servant à identifier le nombre d'élément différent et le 
			nombre de fois qu'ils apparaissent.
				@param	self
				@return Le nombre d'apparition unique dans l'arbre
				"""
		apparition = {}
		for profondeur in self.arbre:
			for noeud in profondeur:
				if noeud[0] not in apparition:
					apparition[noeud[0]] = 1
				else:
					apparition[noeud[0]] += 1
		return apparition
