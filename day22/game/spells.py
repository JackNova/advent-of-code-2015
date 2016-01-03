#!/usr/bin/python
# -*- coding: utf-8 -*-

def compose_execute_all(*functions):
	def inner(x):
		for f in functions:
			f(x)

	return inner

noop = lambda x : None

# Effects all work the same way.
# Effects apply at the start of both the player's turns and the boss' turns.
# Effects are created with a timer (the number of turns they last);
# at the start of each turn, after they apply any effect they have,
# their timer is decreased by one. If this decreases the timer to zero, the effect ends.
# You cannot cast a spell that would start an effect which is already active. However,
# effects can be started on the same turn they end.

class Effect(object):
	def __init__(self, name='', cost=0, on_apply=noop):
		self.name = name
		self.cost = cost
		self.on_apply = on_apply

	def apply(self, game_state):
		if type(self) is Effect:
			game_state.wizard.mana -= self.cost
		self.on_apply(game_state)

	def use(self, game_state):
		self.apply(game_state)


class TimedEffect(Effect):
	def __init__(self, timer=1, on_end=noop, on_cast=noop, **kwargs):
		super(TimedEffect, self).__init__(**kwargs)
		self.timer = timer
		self.on_end = on_end
		self.on_cast = on_cast

	def apply(self, game_state):
		super(TimedEffect, self).apply(game_state)
		self.timer -= 1
		if self.timer <= 0:
			game_state.spells.remove(self)
			self.on_end(game_state)

	def cast(self, game_state):
		game_state.wizard.mana -= self.cost
		self.on_cast(game_state)

	def use(self, game_state):
		self.cast(game_state)
		game_state.spells.append(self)

def damage_opponent(amount):
	def f(game_state):
		game_state.boss.hit_points -= amount
	return f

def heal_me(amount):
	def f(game_state):
		game_state.wizard.hit_points+=amount
	return f

# Magic Missile costs 53 mana. It instantly does 4 damage.
magic_missile = lambda : Effect(name='Magic Missile', on_apply=damage_opponent(4), cost=53)

# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
drain = lambda : Effect(name='Drain', cost=73, on_apply=compose_execute_all(damage_opponent(2), heal_me(2)))

# Shield costs 113 mana. It starts an effect that lasts for 6 turns.
# While it is active, your armor is increased by 7.
def increase_armor(amount):
	def f(game_state):
		game_state.wizard.armor += amount
	return f

shield = lambda timer=6 : TimedEffect(name='Shield', cost=113, timer=timer, on_cast=increase_armor(7), on_end=increase_armor(-7))

# Poison costs 173 mana. It starts an effect that lasts for 6 turns.
# At the start of each turn while it is active, it deals the boss 3 damage.

poison = lambda timer=6: TimedEffect(name='Poison', cost=173, timer=timer, on_apply=damage_opponent(3))

# Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
# At the start of each turn while it is active, it gives you 101 new mana.

def increase_mana(amount):
	def f(game_state):
		game_state.wizard.mana += amount
	return f

recharge = lambda timer=5 : TimedEffect(name='Recharge', cost=229, timer=timer, on_apply=increase_mana(101))

def get_spell_by_name(name):
	return {
		'Magic Missile': magic_missile,
		'Drain': drain,
		'Shield': shield,
		'Poison': poison,
		'Recharge': recharge
	}[name]