#!/usr/bin/python
# -*- coding: utf-8 -*-

from spells import Effect, TimedEffect
from spells import magic_missile, drain, shield, poison, recharge
from characters import Boss, Wizard
from strategies import SelectSpellByPredefinedOrder

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


class SelectSpellByPredefinedOrder(object):
	def __init__(self, spells=[]):
		self.spells = list(reversed(spells))
		
	def select_spell(self, game_state=None):
		spell = self.spells.pop()
		return spell


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
		
	while True:
		print '\n-- Player turn --'
		print_recap(gs)
		for effect in list(gs.spells):
			print effect.name
			effect.apply(gs)
			if not boss.is_alive():
				print 'boss is dead.'
				return

		spell = wizard.select_spell(game_state=gs)
		if type(spell) is TimedEffect:
			print 'Player casts %s' % spell.name
			spell.cast(gs)
			gs.spells.append(spell)
			if not boss.is_alive():
				print 'boss is dead.'
				return
		else:
			print 'Player uses instantily %s' % spell.name
			spell.apply(gs)
			if not boss.is_alive():
				print 'boss is dead.'
				return

		print '\n-- Boss turn --'
		print_recap(gs)
		for effect in list(gs.spells):
			print effect.name
			effect.apply(gs)
			if not boss.is_alive():
				print 'boss is dead.'
				return

		boss.attack(wizard)
		if not wizard.is_alive():
			print 'wizard is dead.'
			return

mock_order = [poison(), magic_missile(), recharge(), shield(), drain(), poison(), magic_missile()]

# For example, suppose the player has 10 hit points and 250 mana,
wizard = Wizard(hit_points=10, mana=250, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
# and that the boss has 13 hit points and 8 damage:
boss = Boss(hit_points=13, damage=8)

combat(wizard, boss)
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

assert not boss.is_alive() and wizard.is_alive()

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

mock_order = [recharge(), shield(), drain(), poison(), magic_missile()]
wizard = Wizard(hit_points=10, mana=250, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
boss = Boss(hit_points=14, damage=8)
print '\n\n\n'
combat(wizard,boss)
assert not boss.is_alive() and wizard.is_alive()

# You start with 50 hit points and 500 mana points.
# The boss's actual stats are in your puzzle input.
# What is the least amount of mana you can spend and still win the fight?
# (Do not include mana recharge effects as "spending" negative mana.)

