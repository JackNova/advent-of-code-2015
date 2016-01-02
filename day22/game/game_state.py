class GameState(object):
	def __init__(self, wizard, boss):
		self.wizard = wizard
		self.boss = boss
		self.spells = []

	def apply_effects(self):
		result = {}
		for x in list(self.spells):
			if self.boss.is_alive():
				x.apply(self)
				result[x.name] = x.__dict__
		return result

def combat(wizard, boss):
	gs = GameState(wizard, boss)
		
	while True:
		gs.apply_effects()
		if not boss.is_alive():
			return gs
		
		wizard.launch_spell(gs)
		if not boss.is_alive():
			return gs

		gs.apply_effects()
		if not boss.is_alive():
			return gs

		boss.attack(wizard)
		if not wizard.is_alive():
			return gs