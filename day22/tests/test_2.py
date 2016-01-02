#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from game.spells import Effect, TimedEffect
from game.spells import magic_missile, drain, shield, poison, recharge
from game.characters import Boss, Wizard
from game.strategies import SelectSpellByPredefinedOrder
from game.game_state import GameState

def hit_armor_mana(wizard):
	return (wizard.hit_points, wizard.armor, wizard.mana)

# Now, suppose the same initial conditions, except that the boss has 14 hit points instead:
mock_order = [recharge(), shield(), drain(), poison(), magic_missile()]
wizard = Wizard(hit_points=10, mana=250, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
boss = Boss(hit_points=14, damage=8)
game_state = GameState(wizard, boss)

# -- Player turn --
# - Player has 10 hit points, 0 armor, 250 mana
assert hit_armor_mana(wizard) == (10, 0, 250)
# - Boss has 14 hit points
assert boss.hit_points == 14
# Player casts Recharge.
s = wizard.launch_spell(game_state)
assert s.name == 'Recharge'

# -- Boss turn --
# - Player has 10 hit points, 0 armor, 21 mana
assert hit_armor_mana(wizard) == (10, 0, 21)
# - Boss has 14 hit points
assert boss.hit_points == 14

fxs = game_state.apply_effects()
# Recharge provides 101 mana; its timer is now 4.
assert len(fxs) == 1
assert fxs['Recharge']['timer'] == 4

# Boss attacks for 8 damage!
boss.attack(wizard)

# -- Player turn --
# - Player has 2 hit points, 0 armor, 122 mana
assert hit_armor_mana(wizard) == (2, 0, 122)
# - Boss has 14 hit points
assert boss.hit_points == 14

fxs = game_state.apply_effects()
# Recharge provides 101 mana; its timer is now 3.
assert len(fxs) == 1
assert fxs['Recharge']['timer'] == 3

# Player casts Shield, increasing armor by 7.
f = wizard.launch_spell(game_state)
assert f.name == 'Shield'

# -- Boss turn --
# - Player has 2 hit points, 7 armor, 110 mana
assert hit_armor_mana(wizard) == (2, 7, 110)
# - Boss has 14 hit points
assert boss.hit_points == 14

fxs = game_state.apply_effects()

# Shield's timer is now 5.
assert fxs['Shield']['timer'] == 5
# Recharge provides 101 mana; its timer is now 2.
assert fxs['Recharge']['timer'] == 2
# Boss attacks for 8 - 7 = 1 damage!
boss.attack(wizard)

# -- Player turn --
# - Player has 1 hit point, 7 armor, 211 mana
assert hit_armor_mana(wizard) == (1, 7, 211)
# - Boss has 14 hit points
assert boss.hit_points == 14

game_state.apply_effects()
# Shield's timer is now 4.
# Recharge provides 101 mana; its timer is now 1.
# Player casts Drain, dealing 2 damage, and healing 2 hit points.
wizard.launch_spell(game_state)

# -- Boss turn --
# - Player has 3 hit points, 7 armor, 239 mana
assert hit_armor_mana(wizard) == (3, 7, 239)
# - Boss has 12 hit points
assert boss.hit_points == 12

fxs = game_state.apply_effects()
# Shield's timer is now 3.
# Recharge provides 101 mana; its timer is now 0.
# Recharge wears off.
assert len(game_state.spells) == 1
# Boss attacks for 8 - 7 = 1 damage!
boss.attack(wizard)

# -- Player turn --
# - Player has 2 hit points, 7 armor, 340 mana
assert hit_armor_mana(wizard) == (2, 7, 340)
# - Boss has 12 hit points
assert boss.hit_points == 12

game_state.apply_effects()
# Shield's timer is now 2.
# Player casts Poison.
s = wizard.launch_spell(game_state)
assert s.name == 'Poison'

# -- Boss turn --
# - Player has 2 hit points, 7 armor, 167 mana
assert hit_armor_mana(wizard) == (2, 7, 167)
# - Boss has 12 hit points
assert boss.hit_points == 12

game_state.apply_effects()
# Shield's timer is now 1.
# Poison deals 3 damage; its timer is now 5.
# Boss attacks for 8 - 7 = 1 damage!
boss.attack(wizard)

# -- Player turn --
# - Player has 1 hit point, 7 armor, 167 mana
assert hit_armor_mana(wizard) == (1, 7, 167)
# - Boss has 9 hit points
assert boss.hit_points == 9

fxs = game_state.apply_effects()
# Shield's timer is now 0.
# Shield wears off, decreasing armor by 7.
# Poison deals 3 damage; its timer is now 4.
wizard.launch_spell(game_state)
# Player casts Magic Missile, dealing 4 damage.

# -- Boss turn --
# - Player has 1 hit point, 0 armor, 114 mana
assert hit_armor_mana(wizard) == (1, 0, 114)
# - Boss has 2 hit points
assert boss.hit_points == 2

game_state.apply_effects()
# Poison deals 3 damage. This kills the boss, and the player wins.
assert not boss.is_alive()