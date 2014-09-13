"""@package Activity
Ce module contient la classe Activite.
"""
__author__ = 'Rémi Carpentier'
__file__ = './Activity.py'
__name__ = 'Activity'
__version__ = '1.0'
class Activity(object):
	"""La classe activite est une suite de log. Ce qui est équivalent à un "bout de log".
	   Elle contient de l'information sur l'activité.
	   """
	def __init__(self, liste_log):
		"""	Le constructeur
			@param	self
					liste_log	Une suite de log formant un "bout de log"
					"""
		def __dispersion(seq):
			"""	Fonction servant à calculer la dispersion de l'activité, c.-à-d.
				le nombre de fois qu'un même élément de la séquence d'action
				apparaîtra.
				@return dispersion La dispersion
				"""
			dispersion = {}
			for action in seq:
				if action not in dispersion:
					dispersion[action] = 1
				else:
					dispersion[action] += 1
			return dispersion

		self.liste_log = liste_log
		self.sequence_action = [log.rclass_name if log.rclass_name \
								else log.click_type for log in liste_log]
		self.intervalle_id = [min([log._id for log in liste_log]), \
							  max([log._id for log in liste_log])]
		self.temps_execution = liste_log[-1].timestamp - liste_log[0].timestamp
		self.dispersion = __dispersion(self.sequence_action)
		self.max_apparition = [key for key in self.dispersion if \
							   self.dispersion[key] == self.dispersion[max(self.dispersion)]]

	def __repr__(self): 
		"""	Fonction qui sert à imprimer
			@param	self
			@return Tous les attributs de l'objet
			"""
		return \
		"liste_log = %s\nsequence_action = %s\nintervalle_id = %s\n" \
		% (self.liste_log, self.sequence_action, self.intervalle_id) + \
		"temps_execution = %s\ndispersion = %s\nmax_apparition = %s\n" % (
		self.temps_execution, self.dispersion, self.max_apparition)

	def __len__(self):
		return len(self.liste_log)

	def __getitem__(self, y):
		return self.sequence_action[y]
		
	def remove(self, y):
		self.liste_log.remove(y)


