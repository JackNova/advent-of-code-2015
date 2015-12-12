import re
from itertools import permutations

# --- Day 9: All in a Single Night ---

# Every year, Santa manages to deliver all of his presents in a single night.

# This year, however, he has some new locations to visit; his elves have
# provided him the distances between every pair of locations. He can start and
# end at any two (different) locations he wants, but he must visit each location exactly once.
# What is the shortest distance he can travel to achieve this?

# For example, given the following distances:

expression = re.compile('([a-zA-Z]+) to ([a-zA-Z]+) = (\d+)')

def parse(s):
	""" returns a tuple of kind (cityA, cityB, distance)
	"""
	m = expression.match(s)
	return tuple(m.groups())

def get_distances(input):
	"""Returns a dictionary of kind { cityA-cityB: distance }
	"""
	distances = [parse(x) for x in input]
	distances_d = {}
	for start, end, d in distances:
		distances_d['%s-%s'%(start, end)] = int(d)
		distances_d['%s-%s'%(end, start)] = int(d)
	return distances_d

def get_all_cities(input):
	distances = [parse(x) for x in input]
	cities = []
	for start, end, _ in distances:
		cities.append(start)
		cities.append(end)
	return set(cities)
	
def path_length(path, distances_d):
	result = 0
	for idx in range(len(path)-1):
		result += distances_d['%s-%s'%(path[idx], path[idx+1])]
	return result

def get_permutations_with_distances(cities, distances_d):
	distances_dd = [(cities, path_length(cities, distances_d)) for cities in permutations(set(cities))]
	return distances_dd

def solve(input):
	distances = get_distances(input)
	cities = get_all_cities(input)
	distances_dd = get_permutations_with_distances(cities, distances)
	for cities, d in distances_dd:
		s = ''
		for c in list(cities):
			s += '%s ->' % c
		print '%s = %s' % (s, d)

	sorted_distances = sorted(distances_dd, key=lambda x: x[-1])

	print sorted_distances[0]
	

test_input = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""".splitlines()

solve(test_input)

with open('input.txt', 'r') as f: input = f.read().splitlines()

solve(input)

# The possible routes are therefore:

# Dublin -> London -> Belfast = 982
# London -> Dublin -> Belfast = 605
# London -> Belfast -> Dublin = 659
# Dublin -> Belfast -> London = 659
# Belfast -> Dublin -> London = 605
# Belfast -> London -> Dublin = 982
# The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

# What is the distance of the shortest route?