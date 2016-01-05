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
	spells_in_use = [name for name, timer in in_use_spells_state]
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


print part_1()