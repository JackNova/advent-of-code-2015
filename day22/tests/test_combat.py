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

mock_order = [recharge(), shield(), drain(), poison(), magic_missile()]
wizard = Wizard(hit_points=10, mana=250, spell_selection_strategy=SelectSpellByPredefinedOrder(mock_order))
boss = Boss(hit_points=14, damage=8)

combat(wizard, boss)
assert hit_armor_mana(wizard) == (1, 0, 114)
assert not boss.is_alive()