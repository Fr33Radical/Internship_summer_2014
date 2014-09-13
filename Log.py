"""@package Log
Ce module contient la classe Log.
"""
__author__ = 'Rémi Carpentier'
__file__ = './Log.py'
__name__ = 'Log'
__version__ = '1.0'
class Log(object):
	def __init__(self, log):
		"""	Le constructeur
			@param	self
					log	Une donnée
					"""
		self._id = log[0]
		self.timestamp = log[1]
		self.activity_name = log[2]
		self.click_type = log[3]
		self.rclass_id = log[4]
		self.rclass_name = log[5]
		self.relativeX = log[6]
		self.relativeY = log[7]
		self.x = log[8]
		self.y = log[9]
	def __repr__(self): 
		"""	Fonction qui sert à imprimer
			@param	self
			@return Tous les attributs de l'objet
			"""
		return "_id = %s\ntimestamp = %s\nactivity_name = %s\nclick_type = %s\n" \
		% (self._id, self.timestamp, self.activity_name, self.click_type) + \
		"rclass_id = %s\nrclass_name = %s\nrelativeX = %s\nrelativeY = %s\n" % (
		self.rclass_id, self.rclass_name, self.relativeX, self.relativeY)

