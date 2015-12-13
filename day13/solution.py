import re
from itertools import permutations
from operator import itemgetter

# --- Day 13: Knights of the Dinner Table ---

# In years past, the holiday feast with your family hasn't gone so well.
# Not everyone gets along! This year, you resolve, will be different.
# You're going to find the optimal seating arrangement and avoid all those awkward conversations.

# You start by writing up a list of everyone invited and the amount their happiness
# would increase or decrease if they were to find themselves sitting next to each other person.
# You have a circular table that will be just big enough to fit everyone comfortably,
# and so each person will have exactly two neighbors.

# For example, suppose you have only four attendees planned, and you calculate their
# potential happiness as follows:

test_input = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

eval_template = re.compile('(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).')
def eval_input(input):
	"""Returns a representation of the model as a tuple
	(person_a, person_b, happiness_change)
	"""
	elements = eval_template.match(input).groups()
	sign = { 'lose': '-', 'gain': '+' }
	return (elements[0], elements[-1], int(sign[elements[1]] + elements[2]))

assert eval_input(test_input.splitlines()[0]) == ('Alice', 'Bob', 54)
assert eval_input(test_input.splitlines()[1]) == ('Alice', 'Carol', -79)

member_template = re.compile('(\w+) would .*')
def get_members(input):
	results = member_template.findall(input)
	return set(results)

assert get_members(test_input) == set(['Alice', 'Bob', 'Carol', 'David'])

# Then, if you seat Alice next to David, Alice would lose 2 happiness units
# (because David talks so much), but David would gain 46 happiness units
# (because Alice is such a good listener), for a total change of 44.

def evaluate_arrangement(arragement, happiness):
	results = []
	total_happiness = 0
	tot = len(arragement)
	for i in range(0, tot):
		left = arragement[i-1]
		me = arragement[i]
		right = arragement[(i+1)%tot]

		left_happiness = happiness['%s-%s'%(me, left)]
		right_happiness = happiness['%s-%s'%(me, right)]
		total_happiness+=(left_happiness+right_happiness)
		results.append( (left_happiness, me, right_happiness) )
	return results + [total_happiness]

def find_optimal_arrangement(input):
	model = [eval_input(i) for i in input.splitlines()]
	happiness_dict = dict([ ( '%s-%s'%(p1, p2), h ) for (p1, p2, h) in model ])
	arrangements = permutations(get_members(input))
	results = [evaluate_arrangement(a, happiness_dict) for a in arrangements]
	return max(results, key=itemgetter(-1))

# If you continue around the table, you could then seat Bob next to Alice
# (Bob gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob
# (Carol gains 60, Bob loses 7) and David (Carol gains 55, David gains 41).
# The arrangement looks like this:

#      +41 +46
# +55   David    -2
# Carol       Alice
# +60    Bob    +54
#      -7  +83

# After trying every other seating arrangement in this hypothetical scenario,
# you find that this one is the most optimal, with a total change in happiness of 330.

test_arrangement = find_optimal_arrangement(test_input)
assert test_arrangement[-1] == 330


# What is the total change in happiness for the optimal seating arrangement of the actual guest list?

with open('input.txt', 'r') as f: input = f.read()

arrangement =  find_optimal_arrangement(input)

# --- Part Two ---

# In all the commotion, you realize that you forgot to seat yourself. At this point,
# you're pretty apathetic toward the whole thing, and your happiness wouldn't really go up
# or down regardless of who you sit next to. You assume everyone else would be just
# as ambivalent about sitting next to you, too.

# So, add yourself to the list, and give all happiness relationships that involve you a score of 0.

# What is the total change in happiness for the optimal seating arrangement that actually includes yourself?

def optimally_add_member(arrangement, member):
	members = arrangement[0:-1]
	tot = len(members)

	solutions = []

	compute_happiness = lambda s: sum([l+r for l, _, r in s ])

	for i in range(0, tot):
		members_copy = list(members)
		left = list(members[i-1])
		left[-1] = 0
		members_copy[i-1] = tuple(left)
		right = list(members[i])
		right[0] = 0
		members_copy[i] = tuple(right)
		members_copy.insert(i, (0, 'X', 0))

		solutions.append(members_copy)

	optimal = max(solutions, key=compute_happiness)

	return optimal + [compute_happiness(optimal)]

# print optimally_add_member(test_arrangement, None)
print arrangement
print optimally_add_member(arrangement, None)
