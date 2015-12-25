import re
from collections import defaultdict
from bfs import breadth_first_search
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
def parse_replacements(txt, invert=False):
	result = defaultdict(list)
	for k, v in replacement_template.findall(txt):
		if invert:
			result[v].append(k)
		else:
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

with open('input.txt') as f: input = f.read()

fucked_molecule = "CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF"
print len(set(generate_replacements(input, fucked_molecule)))

example_replacements = """
e => H
e => O
H => HO
H => OH
O => HH
"""

is_goal = lambda x: x == 'HOH'

def successors(available_replacements, invert=False):
	replacements = parse_replacements(available_replacements, invert=invert)
	max_replacements_key_length = max([len(x) for x in replacements.keys()])

	def result(starting_molocule):
		for chunk, i, j in chunks(starting_molocule, max_replacements_key_length):
			for replacement in replacements[chunk]:
				yield starting_molocule[:i] + replacement + starting_molocule[j:]

	return result

assert len(breadth_first_search('e', is_goal, successors(example_replacements))) == 3

assert len(breadth_first_search('e', lambda x: x=='HOHOHO', successors(example_replacements))) == 6

def heuristic_better_shorten(successor, path, initial_state):
	last_element_in_path = len(path) > 0 and path[len(path) - 1]
	if not last_element_in_path:
		return len(successor) < len(initial_state)
	else:
		return len(successor) < len(last_element_in_path)

def pick_next_strategy(frontier):
	longest_path = sorted(frontier, key=lambda x: -len(x[1]))
	candidate = longest_path[0]
	frontier.remove(candidate)
	return candidate

# without heuristic

result = breadth_first_search('HOHOHO', lambda x: x=='e', successors(example_replacements, invert=True))
print result
print len(result)

# with HEURISTIC
result = breadth_first_search('HOHOHO',
	lambda x: x=='e',
	successors(example_replacements, invert=True),
	heuristic=heuristic_better_shorten,
	pick_next=pick_next_strategy)
print result
print len(result)

# with HEURISTIC
result = breadth_first_search(fucked_molecule,
	lambda x: x=='e',
	successors(input, invert=True),
	# heuristic=heuristic_better_shorten,
	pick_next=pick_next_strategy)
print result
print len(result)




chopped = 'CRnCaSiRnPMgYFArCaPRnCaRnFArArCaCaCaCaPTiRnPRnFArCaFArCaFArThCaPRnCaCaFArCaCaF'

# result = breadth_first_search(fucked_molecule, lambda x: x=='e', successors(input, invert=True))
# print result
# print len(result)

# def chop_down(txt, available_replacements):
# 	replacements = parse_replacements(available_replacements, invert=True)
# 	for k, v in replacements.iteritems():
# 		txt = txt.replace(k, v[0])
# 	print txt

# chop_down('CRnCaSiRnBFArSiRnSiRnFArBFYFArCaCaCaPRnCaRnFArArCaCaCaCaCaCaSiRnFYFArPBCaCaSiRnFArTiRnPRnCaFArCaCaCaCaFArCaCaCaCaFArThSiRnFYFArCaSiRnBFArCaPTiRnCaCaCaCaCaFArPTiBSiRnFYFArCaCaCaCaF', input)

