#!/usr/bin/python
# -*- coding: utf-8 -*-

from game.spells import Effect, TimedEffect
from game.spells import magic_missile, drain, shield, poison, recharge
from game.spells import get_spell_by_name
from game.characters import Boss, Wizard
from game.game_state import GameState
from search import lowest_cost_search

# --- Day 22: Wizard Simulator 20XX ---

# You start with 50 hit points and 500 mana points.
# The boss's actual stats are in your puzzle input.
# What is the least amount of mana you can spend and still win the fight?
# (Do not include mana recharge effects as "spending" negative mana.)


boss_damage = 9

# here = frozenset(here) | frozenset(['light'])
# state = (here, frozenset())

# return lowest_cost_search(state, bsuccessors2, is_goal, bcost)

def part_1():
	wizard = Wizard(hit_points=50, mana=500)
	boss = Boss(hit_points=51, damage=boss_damage)
	gs = represent(GameState(wizard, boss))
	return lowest_cost_search(gs, successors, is_goal, action_cost)

def part_2():
	wizard = Wizard(hit_points=50, mana=500)
	boss = Boss(hit_points=51, damage=boss_damage)
	gs = represent(GameState(wizard, boss))
	return lowest_cost_search(gs, successors_2, is_goal, action_cost)


# STATE REPRESENTATION
def represent(game_state):
	wizard = (game_state.wizard.hit_points, game_state.wizard.armor, game_state.wizard.mana)
	boss = game_state.boss.hit_points
	spells = [(s.name, s.timer) for s in game_state.spells]
	return (wizard, boss, frozenset(spells))

def successors(game_state):
	"""Return a dict of {state:action} pairs.  A state is a (wizard, boss, timed_effects) tuple,
	wizard: (hit_points, armor, mana); boss: (hit_points)"""
	result = {}
	w, b, in_use_spells_state = game_state
	spells_in_use = [name for name, timer in in_use_spells_state if timer > 1]
	# apply_effects gets callend once before launch spell is called
	# this clears up spells that have just timer=1 left
	spells = [magic_missile, drain, shield, poison, recharge]
	available_spells = [s for s in spells if s().name not in spells_in_use]

	for available_spell in available_spells:
		boss = Boss(damage=boss_damage, hit_points=b)
		h,a,m = w
		wizard = Wizard(mana=m,
			hit_points=h,
			armor=a)
		gs = GameState(wizard, boss)

		candidate_spell = available_spell()

		# restore timed spells
		for name, timer in in_use_spells_state:
			gs.spells.append(get_spell_by_name(name)(timer))
			
		gs.apply_effects()
		if not boss.is_alive():
			result[represent(gs)] = None # boss is killed by existing spells
		else:
			wizard.launch_spell(gs, spell=candidate_spell)
			if not wizard.is_alive():
				continue
			if not boss.is_alive(): # boss killed by spell
				result[represent(gs)] = candidate_spell.name
			else:
				gs.apply_effects()
				if not boss.is_alive(): # boss killed by timed effect
					result[represent(gs)] = candidate_spell.name
				else:
					boss.attack(wizard)

					if wizard.is_alive():
						result[represent(gs)] = candidate_spell.name

	return result

def is_goal(game_state):
	_, boss_hit_points, spells = game_state
	return boss_hit_points <= 0

def action_cost(action):
	if not action:
		return 0

	spell = get_spell_by_name(action)()
	return spell.cost


# print part_1()

# --- Part Two ---

# On the next run through the game, you increase the difficulty to hard.
# At the start of each player turn (before any other effects apply), you lose 1 hit point.
# If this brings you to or below 0 hit points, you lose.

# With the same starting stats for you and the boss,
# what is the least amount of mana you can spend and still win the fight?

def successors_2(game_state):
	"""Return a dict of {state:action} pairs.  A state is a (wizard, boss, timed_effects) tuple,
	wizard: (hit_points, armor, mana); boss: (hit_points)"""
	result = {}
	w, b, in_use_spells_state = game_state
	spells_in_use = [name for name, timer in in_use_spells_state if timer > 1]
	# apply_effects gets callend once before launch spell is called
	# this clears up spells that have just timer=1 left
	spells = [magic_missile, drain, shield, poison, recharge]
	available_spells = [s for s in spells if s().name not in spells_in_use]

	# print game_state

	for available_spell in available_spells:
		boss = Boss(damage=boss_damage, hit_points=b)
		h,a,m = w
		wizard = Wizard(mana=m,
			hit_points=h,
			armor=a)
		gs = GameState(wizard, boss, level='hard')

		candidate_spell = available_spell()
		# print 'candidate_spell: %s' % candidate_spell.name

		# restore timed spells
		for name, timer in in_use_spells_state:
			gs.spells.append(get_spell_by_name(name)(timer))
			
		gs.apply_effects()
		if not wizard.is_alive():
			# can't happen at easy level
			# print 'wizard is dead by hard level 1'
			# print represent(gs)
			continue

		if not boss.is_alive():
			# if boss dies by existing effects it is not necessary to add
			# a new spell
			result[represent(gs)] = None # boss is killed by existing spells
		else:
			# here boss is alive
			wizard.launch_spell(gs, spell=candidate_spell)
			if not wizard.is_alive():
				# print 'wizard is dead launching spell'
				# print represent(gs)
				continue
			if not boss.is_alive(): # boss killed by spell
				result[represent(gs)] = candidate_spell.name
			else:
				gs.apply_effects()
				if not wizard.is_alive():
					# print 'wizard is dead by hard level 2'
					# print represent(gs)
					continue
				if not boss.is_alive(): # boss killed by timed effect
					result[represent(gs)] = candidate_spell.name
				else:
					boss.attack(wizard)

					if wizard.is_alive():
						# if wizard is alive I log the launched spell
						# or else I don't care about this state
						result[represent(gs)] = candidate_spell.name

	return result

print part_1()