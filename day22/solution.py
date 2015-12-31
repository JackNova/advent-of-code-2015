#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools

def compose(*functions):
	def compose2(f, g):
		return lambda x: f(g(x))
	return functools.reduce(compose2, functions, lambda x: x)

noop = lambda x : None

# --- Day 22: Wizard Simulator 20XX ---

# Little Henry Case decides that defeating bosses with swords and stuff is boring.
# Now he's playing the game with a wizard.
# Of course, he gets stuck on another boss and needs your help again.

# In this version, combat still proceeds with the player and the boss taking alternating turns.
# The player still goes first. Now, however, you don't get any equipment;
# instead, you must choose one of your spells to cast.
# The first character at or below 0 hit points loses.


# Since you're a wizard, you don't get to wear armor, and you can't attack normally.
# However, since you do magic damage, your opponent's armor is ignored,
# and so the boss effectively has zero armor as well. As before,
# if armor (from a spell, in this case) would reduce damage below 1, it becomes 1 instead
# - that is, the boss' attacks always deal at least 1 damage.

# On each of your turns, you must select one of your spells to cast.
# If you cannot afford to cast any spell, you lose.
# Spells cost mana; you start with 500 mana, but have no maximum limit.
# You must have enough mana to cast a spell, and its cost is immediately deducted when you cast it.
# Your spells are Magic Missile, Drain, Shield, Poison, and Recharge.

class Boss(object):
	def __init__(self, hit_points=100, damage=0):
		self.hit_points = hit_points
		self.damage = damage
		self.alive = True

	def attack(self, player):
		print 'Boss attacks for damage %s' % self.damage
		player.hit_points -= self.damage

	def is_alive(self):
		return self.alive


class Wizard(object):
	def __init__(self, mana=500, hit_points=100):
		self.mana = mana
		self.alive = True
		self.hit_points = hit_points
		self.armor = 0

	def cast_spell(self, game_state):
		spell = self.select_spell()
		if not spell:
			self.alive = False
		else:
			game_state.spells.append(spell)

	def is_alive(self):
		return self.alive

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
		print 'casts %s' % self.name
		self.on_apply(game_state)

class TimedEffect(Effect):
	def __init__(self, timer=1, on_end=noop, on_cast=noop, **kwargs):
		Effect.__init__(self, **kwargs)
		self.timer = timer
		self.on_end = on_end
		self.on_cast = on_cast

	def apply(self, game_state):
		Effect.on_apply(game_state)
		self.timer -= 1
		print 'its timer is now %s' % self.timer
		if timer <= 0:
			game_state.spells.remove(self)
			print '%s ends' % self.name
			self.on_end(game_state)

	def cast(self, game_state):
		self.on_cast(game_state)

def damage_opponent(amount):
	def f(game_state):
		print 'deals %s damage;' % amount
		game_state.opponent.hit_points -= amount
	return f

def heal_me(amount):
	def f(game_state):
		print 'hels me %s hit points' % amount
		game_state.me.hit_points+=amount
	return f

# Magic Missile costs 53 mana. It instantly does 4 damage.
magic_missile = Effect(on_apply=damage_opponent(4), cost=53)

# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
drain = Effect(cost=73, on_apply=compose(damage_opponent(4), heal_me(2)))

# Shield costs 113 mana. It starts an effect that lasts for 6 turns.
# While it is active, your armor is increased by 7.
def increase_armor(amount):
	def f(game_state):
		game_state.me.armor += 7
	return f

shield = TimedEffect(cost=113, timer=6, on_cast=increase_armor(7), on_end=increase_armor(-7))

# Poison costs 173 mana. It starts an effect that lasts for 6 turns.
# At the start of each turn while it is active, it deals the boss 3 damage.

poison = TimedEffect(cost=173, timer=6, on_apply=damage_opponent(3))

# Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
# At the start of each turn while it is active, it gives you 101 new mana.

def increase_mana(amount):
	def f(game_state):
		game_state.me.mana += amount
	return f

recharge = TimedEffect(cost=229, timer=5, on_apply=increase_mana(101))


# For example, suppose the player has 10 hit points and 250 mana,
me = Wizard(hit_points=10, mana=250)
# and that the boss has 13 hit points and 8 damage:
boss = Boss(hit_points=13, damage=8)

class GameState(object):
	def __init__(self, wizard, boss):
		self.wizard = wizard
		self.boss = boss
		self.spells = []

def combat(wizard, boss):
	gs = GameState(wizard, boss)

	def print_recap(gs):
		print '- Player has %s hit points, %s armor, %s mana' % (gs.wizard.hit_points, gs.wizard.armor, gs.wizard.mana)
		print '- Boss has %s hit points' % gs.boss.hit_points
		
	while wizard.is_alive() and boss.is_alive():
		print '-- Player turn --'
		for effect in gs.spells:
			# Poison deals 3 damage; its timer is now 5.
			print '%s deals %s damage; its timer is now %s' % (effect.name, effect.amount, effect.timer)
			effect.apply(gs)
		print_recap(gs)
		spell = wizard.select_spell()
		if type(spell) is TimedEffect:
			print 'Player casts %s\n\n' % spell.name
			gs.spells.append(spell)
		else:
			spell.apply(gs)

		print '-- Boss turn --'
		print_recap(gs)

		boss.attack(wizard)
		for effect in gs.spells:
			effect.apply(gs)

# -- Player turn --
# - Player has 10 hit points, 0 armor, 250 mana
# - Boss has 13 hit points
# Player casts Poison.

# -- Boss turn --
# - Player has 10 hit points, 0 armor, 77 mana
# - Boss has 13 hit points
# Poison deals 3 damage; its timer is now 5.
# Boss attacks for 8 damage.

# -- Player turn --
# - Player has 2 hit points, 0 armor, 77 mana
# - Boss has 10 hit points
# Poison deals 3 damage; its timer is now 4.
# Player casts Magic Missile, dealing 4 damage.

# -- Boss turn --
# - Player has 2 hit points, 0 armor, 24 mana
# - Boss has 3 hit points
# Poison deals 3 damage. This kills the boss, and the player wins.
# Now, suppose the same initial conditions, except that the boss has 14 hit points instead:

# -- Player turn --
# - Player has 10 hit points, 0 armor, 250 mana
# - Boss has 14 hit points
# Player casts Recharge.

# -- Boss turn --
# - Player has 10 hit points, 0 armor, 21 mana
# - Boss has 14 hit points
# Recharge provides 101 mana; its timer is now 4.
# Boss attacks for 8 damage!

# -- Player turn --
# - Player has 2 hit points, 0 armor, 122 mana
# - Boss has 14 hit points
# Recharge provides 101 mana; its timer is now 3.
# Player casts Shield, increasing armor by 7.

# -- Boss turn --
# - Player has 2 hit points, 7 armor, 110 mana
# - Boss has 14 hit points
# Shield's timer is now 5.
# Recharge provides 101 mana; its timer is now 2.
# Boss attacks for 8 - 7 = 1 damage!

# -- Player turn --
# - Player has 1 hit point, 7 armor, 211 mana
# - Boss has 14 hit points
# Shield's timer is now 4.
# Recharge provides 101 mana; its timer is now 1.
# Player casts Drain, dealing 2 damage, and healing 2 hit points.

# -- Boss turn --
# - Player has 3 hit points, 7 armor, 239 mana
# - Boss has 12 hit points
# Shield's timer is now 3.
# Recharge provides 101 mana; its timer is now 0.
# Recharge wears off.
# Boss attacks for 8 - 7 = 1 damage!

# -- Player turn --
# - Player has 2 hit points, 7 armor, 340 mana
# - Boss has 12 hit points
# Shield's timer is now 2.
# Player casts Poison.

# -- Boss turn --
# - Player has 2 hit points, 7 armor, 167 mana
# - Boss has 12 hit points
# Shield's timer is now 1.
# Poison deals 3 damage; its timer is now 5.
# Boss attacks for 8 - 7 = 1 damage!

# -- Player turn --
# - Player has 1 hit point, 7 armor, 167 mana
# - Boss has 9 hit points
# Shield's timer is now 0.
# Shield wears off, decreasing armor by 7.
# Poison deals 3 damage; its timer is now 4.
# Player casts Magic Missile, dealing 4 damage.

# -- Boss turn --
# - Player has 1 hit point, 0 armor, 114 mana
# - Boss has 2 hit points
# Poison deals 3 damage. This kills the boss, and the player wins.

# You start with 50 hit points and 500 mana points.
# The boss's actual stats are in your puzzle input.
# What is the least amount of mana you can spend and still win the fight?
# (Do not include mana recharge effects as "spending" negative mana.)

