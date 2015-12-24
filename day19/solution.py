import re
from collections import defaultdict
# --- Day 19: Medicine for Rudolph ---

# Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly, and he needs medicine.

# Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph is going to need
# custom-made medicine. Unfortunately, Red-Nosed Reindeer chemistry isn't similar to regular
# reindeer chemistry, either.

# The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission plant,
# capable of constructing any Red-Nosed Reindeer molecule you need.
# It works by starting with some input molecule and then doing a series of replacements,
# one per step, until it has the right molecule.

# However, the machine has to be calibrated before it can be used.
# Calibration involves determining the number of molecules that
# can be generated in one step from a given starting point.

# For example, imagine a simpler machine that supports only the following replacements:

test_replacements = """
H => HO
H => OH
O => HH
"""

replacement_template = re.compile("(\w+) => (\w+)")
def parse_replacements(txt):
	result = defaultdict(list)
	for k, v in replacement_template.findall(txt):
		result[k].append(v)
	return result

assert parse_replacements(test_replacements) == {'H': ['HO', 'OH'], 'O': ['HH']}

# Given the replacements above and starting with HOH,

test_starting_molecule = 'HOH'

# the following molecules could be generated:

# HOOH (via H => HO on the first H).
# HOHO (via H => HO on the second H).
# OHOH (via H => OH on the first H).
# HOOH (via H => OH on the second H).
# HHHH (via O => HH).

def chunks(s, max_size):
	s_length = len(s)
	for i in range(len(s)):
		for j in range(max_size):
			if i+j+1 <= s_length:
				yield (s[i:i+j+1], i, i+j+1)

assert list(chunks('dario', 2)) == [('d', 0, 1), ('da', 0, 2), ('a', 1, 2), ('ar', 1, 3), ('r', 2, 3), ('ri', 2, 4), ('i', 3, 4), ('io', 3, 5), ('o', 4, 5)]

def generate_replacements(available_replacements, starting_molocule):
	replacements = parse_replacements(available_replacements)
	max_replacements_key_length = max([len(x) for x in replacements.keys()])
	for chunk, i, j in chunks(starting_molocule, max_replacements_key_length):
		for replacement in replacements[chunk]:
			yield starting_molocule[:i] + replacement + starting_molocule[j:]

assert set(generate_replacements(test_replacements, test_starting_molecule)) == set(['HHHH', 'HOOH', 'OHOH', 'HOHO'])

# So, in the example above, there are 4 distinct molecules
# (not five, because HOOH appears twice) after one replacement from HOH.

# Santa's favorite molecule, HOHOHO, can become 7 distinct molecules
# (over nine replacements: six from H, and three from O).

assert len(set(generate_replacements(test_replacements, 'HOHOHO'))) == 7

# The machine replaces without regard for the surrounding characters.
# For example, given the string H2O, the transition H => OO would result in OO2O.

# Your puzzle input describes all of the possible replacements and,
# at the bottom, the medicine molecule for which you need to calibrate the machine.
# How many distinct molecules can be created after all the different ways you can do
# one replacement on the medicine molecule?