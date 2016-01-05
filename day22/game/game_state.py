class GameState(object):
	def __init__(self, wizard, boss, level='easy'):
		self.wizard = wizard
		self.boss = boss
		self.spells = []
		self.level = level

	def apply_effects(self, before_who):
		if self.level == 'hard' and before_who=='before_wizard':
			self.wizard.hit_points -= 1

		result = {}
		for x in list(self.spells):
			if self.boss.is_alive():
				x.apply(self)
				result[x.name] = x.__dict__
		return result

def combat(wizard, boss, level='easy'):
	gs = GameState(wizard, boss, level=level)
		
	while True:
		gs.apply_effects('before_wizard')
		if not boss.is_alive():
			return gs
		
		wizard.launch_spell(gs)
		if not boss.is_alive():
			return gs

		gs.apply_effects('before_boss')
		if not boss.is_alive():
			return gs

		boss.attack(wizard)
		if not wizard.is_alive():
			return gs