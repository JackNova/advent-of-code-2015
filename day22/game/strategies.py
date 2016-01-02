class SelectSpellByPredefinedOrder(object):
	def __init__(self, spells=[]):
		self.spells = list(reversed(spells))
		
	def select_spell(self, game_state=None):
		spell = self.spells.pop()
		return spell

class OptimallySelectSpell(object):
	def __init__(self, available_spells=[]):
		super(OptimallySelectSpell, self).__init__()
		self.available_spells = available_spells

	def select_spell(self, game_state=None):
		pass