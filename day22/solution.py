#!/usr/bin/python
# -*- coding: utf-8 -*-

from spells import Effect, TimedEffect
from spells import magic_missile, drain, shield, poison, recharge
from characters import Boss, Wizard
from strategies import SelectSpellByPredefinedOrder
from game_state import GameState

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


	def select_spell(self, game_state=None):

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


# You start with 50 hit points and 500 mana points.
# The boss's actual stats are in your puzzle input.
# What is the least amount of mana you can spend and still win the fight?
# (Do not include mana recharge effects as "spending" negative mana.)

