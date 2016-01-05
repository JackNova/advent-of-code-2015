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

mock_order = [poison(), recharge(), shield(), poison(), drain(), recharge(), poison(), magic_missile()]
wizard = Wizard(hit_points=50, mana=500, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
boss = Boss(hit_points=51, damage=9)

combat(wizard, boss, level='hard')
assert not boss.is_alive()
assert wizard.is_alive()

# SOLUTION
[((50, 0, 500), 51, frozenset([])),
('Poison', 173), ((40, 0, 327), 48, frozenset([('Poison', 5)])),
('Recharge', 402), ((30, 0, 199), 42, frozenset([('Poison', 3), ('Recharge', 4)])),
('Shield', 515), ((27, 7, 288), 36, frozenset([('Poison', 1), ('Shield', 5), ('Recharge', 2)])),
('Poison', 688), ((24, 7, 317), 30, frozenset([('Poison', 5), ('Shield', 3)])),
('Drain', 761), ((23, 7, 244), 22, frozenset([('Poison', 3), ('Shield', 1)])),
('Recharge', 990), ((13, 0, 116), 16, frozenset([('Recharge', 4), ('Poison', 1)])),
('Poison', 1163), ((3, 0, 145), 10, frozenset([('Poison', 5), ('Recharge', 2)])),
('Magic Missile', 1216), ((2, 0, 193), 0, frozenset([('Poison', 3), ('Recharge', 1)]))]