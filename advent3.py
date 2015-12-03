# Santa is delivering presents to an infinite two-dimensional grid of houses.

# He begins by delivering a present to the house at his starting location,
# and then an elf at the North Pole calls him via radio and tells him where to move next.
# Moves are always exactly one house to the north (^), south (v), east (>), or west (<).
# After each move, he delivers another present to the house at his new location.

# However, the elf back at the north pole has had a little too much eggnog, and so
# his directions are a little off, and Santa ends up visiting some houses more than once.
# How many houses receive at least one present?

with open('input/input3.txt') as f: input = f.read()

def symbol_to_vector(symbol):
	# (0, 0) assumed top right
	options = { # (x, y) tuple represent the move vector
		'>': (1, 0),
		'^': (0, -1),
		'<': (-1, 0),
		'v': (0, 1)
	}
	return options[symbol]

def walk(symbol, from_p=(0, 0)):
	return tuple(map(sum, zip(from_p, symbol_to_vector(symbol))))

assert symbol_to_vector('^') == (0, -1)
assert symbol_to_vector('>') == (1, 0)
assert symbol_to_vector('<') == (-1, 0)
assert symbol_to_vector('v') == (0, 1)

position = (0, 0)

assert walk('>', from_p=position) == (1, 0)
assert walk('>', from_p=(1, 0)) == (2, 0)
assert walk('^', from_p=(7, 11)) == (7, 10)
assert walk('v', from_p=(7, 11)) == (7, 12)
	

def walk_path(path):
	visited_houses = [(0,0)]
	previous = (0, 0)
	for symbol in list(path):
		x = walk(symbol, from_p=previous)
		visited_houses.append(x)
		previous = x
	return visited_houses


# For example:

# > delivers presents to 2 houses: one at the starting location, and one to the east.

assert len(set(walk_path('>'))) == 2

# ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.

assert len(set(walk_path('^>v<'))) == 4

# ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

assert len(set(walk_path('^v^v^v^v^v'))) == 2

print len(set(walk_path(input)))


