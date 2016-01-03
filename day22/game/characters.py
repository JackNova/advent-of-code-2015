class Boss(object):
	def __init__(self, hit_points=100, damage=0):
		self.hit_points = hit_points
		self.damage = damage

	def attack(self, player):
		strength = self.damage - player.armor
		hit = strength > 0 and strength or 1
		player.hit_points -= hit

	def is_alive(self):
		return self.hit_points > 0


class Wizard(object):
	def __init__(self, mana=500, hit_points=100, armor=0, spell_selection_strategy=None):
		self.mana = mana
		self.alive = True
		self.hit_points = hit_points
		self.armor = armor
		self.spell_selection_strategy = spell_selection_strategy

	def select_spell(self, game_state=None):
		spell = self.spell_selection_strategy.select_spell(game_state=game_state)
		if not spell:
			self.alive = False
		else:
			return spell

	def is_alive(self):
		return self.alive and self.hit_points > 0 and self.mana > 0

	def launch_spell(self, game_state):
		spell = self.select_spell(game_state=game_state)
		spell.use(game_state)
		return spell