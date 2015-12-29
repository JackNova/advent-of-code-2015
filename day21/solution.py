from itertools import combinations
# --- Day 21: RPG Simulator 20XX ---

# Little Henry Case got a new video game for Christmas.
# It's an RPG, and he's stuck on a boss.
# He needs to know what equipment to buy at the shop. He hands you the controller.

# In this game, the player (you) and the enemy (the boss) take turns attacking.
# The player always goes first.
# Each attack reduces the opponent's hit points by at least 1.
# The first character at or below 0 hit points loses.


class Player(object):
	def __init__(self, damage=0, armor=0, hit_points=100):
		self.damage = damage
		self.armor = armor
		self.hit_points = hit_points

	def attack(self, defender):
		# Damage dealt by an attacker each turn is equal to the attacker's
		# damage score minus the defender's armor score.
		# An attacker always does at least 1 damage.
		strength = self.damage - defender.armor
		defender.hit_points -= (strength > 0 and strength or 1)

	def buy(self, equipment):
		# You must buy exactly one weapon; no dual-wielding.
		# Armor is optional, but you can't use more than one.
		# You can buy 0-2 rings (at most one for each hand).
		# You must use any items you buy.
		# The shop only has one of each item, so you can't buy, for example, two rings of Damage +3.
		for name, cost, damage, armor in equipment:
			self.damage += damage
			self.armor += armor

	def reset_equipment(self):
		self.damage = 0
		self.armor = 0

# So, if the attacker has a damage score of 8, and the defender has an armor score of 3,
# the defender loses 5 hit points.
me = Player(damage=8)
boss = Player(armor=3)
me.attack(boss)

assert boss.hit_points == 100 - 5


# If the defender had an armor score of 300, the defender would still lose 1 hit point.
me = Player(damage=8)
boss = Player(armor=300)
me.attack(boss)

assert boss.hit_points == 100 - 1

# Your damage score and armor score both start at zero.
# They can be increased by buying items in exchange for gold.

# You start with no items and have as much gold as you need.
# Your total damage or armor is equal to the sum of those stats from all of your items.
# You have 100 hit points.

# Here is what the item shop is selling:

# Weapons:    Cost  Damage  Armor
weapons = [
('Dagger',    	8,    4,      0),
('Shortsword',  10,   5,      0),
('Warhammer',   25,   6,      0),
('Longsword',   40,   7,      0),
('Greataxe',    74,   8,      0)
]

# Armor:      Cost  Damage  Armor
armors = [
('Leather',      13,     0,       1),
('Chainmail',    31,     0,       2),
('Splintmail',   53,     0,       3),
('Bandedmail',   75,     0,       4),
('Platemail',   102,     0,       5)
]

# Rings:      Cost  Damage  Armor
rings = [
('Damage +1',    25,     1,       0),
('Damage +2',    50,     2,       0),
('Damage +3',   100,     3,       0),
('Defense +1',   20,     0,       1),
('Defense +2',   40,     0,       2),
('Defense +3',   80,     0,       3)
]

# You must buy exactly one weapon; no dual-wielding.
# Armor is optional, but you can't use more than one.
# You can buy 0-2 rings (at most one for each hand).
# You must use any items you buy.
# The shop only has one of each item, so you can't buy, for example, two rings of Damage +3.

def flatten(xs):
	for x in xs:
		for i in x:
			yield i

def equipment_generator(weapons, armors, rings):
	for weapon in weapons:
		for armor in armors + [('None', 0, 0, 0)]:
			for rgs in list(combinations(rings, 2)) + [[ring] for ring in rings] + [[('None', 0, 0, 0)]]:
				yield [weapon, armor] + list(rgs)

# For example, suppose you have 8 hit points, 5 damage, and 5 armor,
# and that the boss has 12 hit points, 7 damage, and 2 armor:

me = Player(hit_points=8, damage=5, armor=5)
boss = Player(hit_points=12, damage=7, armor=2)

# The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
me.attack(boss)
assert boss.hit_points == 9
# The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
boss.attack(me)
assert me.hit_points == 6
# The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
me.attack(boss)
assert boss.hit_points == 6
# The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
boss.attack(me)
assert me.hit_points == 4
# The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
me.attack(boss)
assert boss.hit_points == 3
# The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
boss.attack(me)
assert me.hit_points == 2
# The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.
me.attack(boss)
assert boss.hit_points == 0
# In this scenario, the player wins! (Barely.)

# You have 100 hit points.
# The boss's actual stats are in your puzzle input. What is the least amount
# of gold you can spend and still win the fight?

input = """
Hit Points: 100
Damage: 8
Armor: 2
"""

boss = Player(hit_points=100, damage=8, armor=2)
me = Player(hit_points=100)

def did_i_win_the_fight(boss):
	def inner(me):
		while True:
			me.attack(boss)
			if boss.hit_points<=0:
				return True
			boss.attack(me)
			if me.hit_points<=0:
				return False

	return inner

def filter_equipments(predicate=lambda equipment: True, equipments=[]):
	mock_player = Player(hit_points=100)
	for equipment in equipments:
		mock_player.buy(equipment)
		if predicate(mock_player):
			yield equipment

		mock_player.reset_equipment()

good_equipments = filter_equipments(predicate=did_i_win_the_fight(boss),
	equipments=equipment_generator(weapons, armors, rings))

for eq in good_equipments:
	print eq

