#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from game.spells import magic_missile, drain, shield, poison, recharge
from game.characters import Boss, Wizard
from game.strategies import SelectSpellByPredefinedOrder
from game.game_state import combat

def hit_armor_mana(wizard):
	return (wizard.hit_points, wizard.armor, wizard.mana)

mock_order = [poison(), recharge(), magic_missile(), magic_missile(), poison(), shield(), magic_missile(), magic_missile()]
wizard = Wizard(hit_points=50, mana=500, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
boss = Boss(hit_points=51, damage=9)

combat(wizard, boss)
assert not boss.is_alive()
assert wizard.is_alive()

# SOLUTION
[((50, 0, 500), 51, frozenset([])),
('Poison', 173), ((41, 0, 327), 48, frozenset([('Poison', 5)])),
('Recharge', 402), ((32, 0, 199), 42, frozenset([('Poison', 3), ('Recharge', 4)])),
('Magic Missile', 455), ((23, 0, 348), 32, frozenset([('Poison', 1), ('Recharge', 2)])),
('Magic Missile', 508), ((14, 0, 497), 25, frozenset([])),
('Poison', 681), ((5, 0, 324), 22, frozenset([('Poison', 5)])),
('Shield', 794), ((3, 7, 211), 16, frozenset([('Poison', 3), ('Shield', 5)])),
('Magic Missile', 847), ((1, 7, 158), 6, frozenset([('Poison', 1), ('Shield', 3)])),
('Magic Missile', 900), ((1, 7, 105), -1, frozenset([('Shield', 2)]))]
