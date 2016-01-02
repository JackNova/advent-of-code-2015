#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from spells import Effect, TimedEffect
from spells import magic_missile, drain, shield, poison, recharge
from characters import Boss, Wizard
from strategies import SelectSpellByPredefinedOrder
from game_state import GameState

def hit_armor_mana(wizard):
	return (wizard.hit_points, wizard.armor, wizard.mana)

mock_order = [poison(), magic_missile(), recharge(), shield(), drain(), poison(), magic_missile()]

# For example, suppose the player has 10 hit points and 250 mana,
wizard = Wizard(hit_points=10, mana=250, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
# and that the boss has 13 hit points and 8 damage:
boss = Boss(hit_points=13, damage=8)

game_state = GameState(wizard, boss)

# -- Player turn --
# - Player has 10 hit points, 0 armor, 250 mana
assert hit_armor_mana(wizard) == (10, 0, 250)
# - Boss has 13 hit points
assert boss.hit_points == 13

# Player casts Poison.
s = wizard.launch_spell(game_state)
assert s.name == 'Poison'

# -- Boss turn --
# - Player has 10 hit points, 0 armor, 77 mana
assert hit_armor_mana(wizard) == (10, 0, 77)
# - Boss has 13 hit points
assert boss.hit_points == 13

fxs = game_state.apply_effects()
# Poison deals 3 damage; its timer is now 5.
assert len(fxs) == 1
assert boss.hit_points == 10
assert fxs['Poison']['timer'] == 5

# Boss attacks for 8 damage.
boss.attack(wizard)


# -- Player turn --
# - Player has 2 hit points, 0 armor, 77 mana
assert hit_armor_mana(wizard) == (2, 0, 77)
# - Boss has 10 hit points
assert boss.hit_points == 10

fxs = game_state.apply_effects()
# Poison deals 3 damage; its timer is now 4.
assert len(fxs) == 1
assert fxs['Poison']['timer'] == 4

# Player casts Magic Missile, dealing 4 damage.
s = wizard.launch_spell(game_state)
assert s.name == 'Magic Missile'

# -- Boss turn --
# - Player has 2 hit points, 0 armor, 24 mana
assert hit_armor_mana(wizard) == (2, 0, 24)
# - Boss has 3 hit points
assert boss.hit_points == 3

# Poison deals 3 damage. This kills the boss, and the player wins.
fxs = game_state.apply_effects()
assert len(fxs) == 1
assert not boss.is_alive()