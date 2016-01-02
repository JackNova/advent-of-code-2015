class GameState(object):
	def __init__(self, wizard, boss):
		self.wizard = wizard
		self.boss = boss
		self.spells = []

	def apply_effects(self):
		result = {}
		for x in list(self.spells):
			x.apply(self)
			result[x.name] = x.__dict__
		return result