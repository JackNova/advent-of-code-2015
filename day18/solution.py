# --- Day 18: Like a GIF For Your Yard ---

# After the million lights incident, the fire code has gotten stricter:
# now, at most ten thousand lights are allowed. You arrange them in a 100x100 grid.

# Never one to let you down, Santa again mails you instructions on the ideal lighting configuration.
# With so few lights, he says, you'll have to resort to animation.

# Start by setting your lights to the included initial configuration (your puzzle input).
# A # means "on", and a . means "off".

# Then, animate your grid in steps, where each step decides the next configuration
# based on the current one. Each light's next state (either on or off) depends on its current state and the current states of the eight lights adjacent to it (including diagonals). Lights on the edge of the grid might have fewer than eight neighbors; the missing ones always count as "off".

# For example, in a simplified 6x6 grid, the light marked A has the neighbors numbered 1 through 8,
# and the light marked B, which is on an edge, only has the neighbors marked 1 through 5:

# 1B5...
# 234...
# ......
# ..123.
# ..8A4.
# ..765.

def neighbors(cell, grid_size):
	width, height = grid_size
	row, col = cell
	top = [(row-1, col-1), (row-1, col), (row-1, col+1)]
	left = [(row, col-1)]
	right = [(row, col+1)]
	bottom = [(row+1, col-1), (row+1, col), (row+1, col+1)]

	def exists(cell):
		x, y = cell
		return x>=0 and x<height and y>=0 and y<width

	return [neighbor for neighbor in top + left + right + bottom if exists(neighbor)]

assert set(neighbors((0, 1), (6, 6))) == set([(0,0), (1,0), (1,1), (1,2), (0,2)])
assert set(neighbors((4, 3), (6, 6))) == set([(3,2), (3,3), (3,4), (4,2), (4,4), (5,2), (5,3), (5,4)])


# The state a light should have next is based on its current state (on or off)
# plus the number of neighbors that are on:

def will_be_turned_on(light, grid, grid_size=(6,6)):
	row, col = light
	width, height = grid_size
	state = grid[(row*width) + col]
	ns = neighbors(light, grid_size)

	neighbors_on = len(filter(lambda (r, c): grid[(r*width)+c] == '#', neighbors(light, grid_size)))
	# A light which is on stays on when 2 or 3 neighbors are on,
	# and turns off otherwise.
	if state is '#':
		return neighbors_on in [2, 3]
	# A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
	# All of the lights update simultaneously; they all consider the same current state before moving to the next.
	else:
		return neighbors_on == 3

# Here's a few steps from an example configuration of another 6x6 grid:

# Initial state:
initial_state = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

def evolve(state, size=(6, 6), keep_on=[]):
	state_s = state.replace('\n', '')
	result = ''
	width, height = size
	for x in range(height):
		for y in range(width):
			if (x, y) in keep_on:
				result += '#'
			elif will_be_turned_on( (x,y), state_s, grid_size=size ):
				result += '#'
			else:
				result += '.'
	return result


# After 1 step:
state_2 = """
..##..
..##.#
...##.
......
#.....
#.##..
"""

test_state_2 = evolve(initial_state)
assert test_state_2 == state_2.replace('\n', '')

# After 2 steps:
state_3 = """
..###.
......
..###.
......
.#....
.#....
"""

test_state_3 = evolve(test_state_2)
assert test_state_3 == state_3.replace('\n', '')

# After 3 steps:
state_4 = """
...#..
......
...#..
..##..
......
......
"""

test_state_4 = evolve(test_state_3)
assert test_state_4 == state_4.replace('\n', '')

# After 4 steps:
state_5 = """
......
......
..##..
..##..
......
......
"""

test_state_5 = evolve(test_state_4)
assert test_state_5 == state_5.replace('\n', '')

# After 4 steps, this example has four lights on.

s = initial_state
for _ in range(4):
	s = evolve(s)

print s
print len(filter(lambda x: x =='#', s))

with open('input.txt', 'r') as f: input = f.read()
s = input
# PART ONE
# for _ in range(100):
# 	s = evolve(s, size=(100, 100))

# print s
# print len(filter(lambda x: x=='#',s))

# In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?


# --- Part Two ---

# You flip the instructions over; Santa goes on to point out that this is all just an implementation of
# Conway's Game of Life. At least, it was, until you notice that something's wrong with the grid of lights
# you bought: four lights, one in each corner, are stuck on and can't be turned off.
# The example above will actually run like this:

initial_state = """
##.#.#
...##.
#....#
..#...
#.#..#
####.#
"""

after_one_step = """
#.##.#
####.#
...##.
......
#...#.
#.####
"""

assert evolve(initial_state, size=(6, 6), keep_on=[(0,0), (0,5), (5,5), (5,0)]) == after_one_step.replace('\n', '')

after_two_steps = """
#..#.#
#....#
.#.##.
...##.
.#..##
##.###
"""

assert evolve(after_one_step, size=(6, 6), keep_on=[(0,0), (0,5), (5,5), (5,0)]) == after_two_steps.replace('\n', '')

after_three_steps = """
#...##
####.#
..##.#
......
##....
####.#
"""

assert evolve(after_two_steps, size=(6, 6), keep_on=[(0,0), (0,5), (5,5), (5,0)]) == after_three_steps.replace('\n', '')

after_four_steps = """
#.####
#....#
...#..
.##...
#.....
#.#..#
"""

assert evolve(after_three_steps, size=(6, 6), keep_on=[(0,0), (0,5), (5,5), (5,0)]) == after_four_steps.replace('\n', '')

after_five_steps = """
##.###
.##..#
.##...
.##...
#.#...
##...#
"""

assert evolve(after_four_steps, size=(6, 6), keep_on=[(0,0), (0,5), (5,5), (5,0)]) == after_five_steps.replace('\n', '')

# After 5 steps, this example now has 17 lights on.

# In your grid of 100x100 lights, given your initial configuration, but with the four corners always
# in the on state, how many lights are on after 100 steps?

s = input
for _ in range(100):
	s = evolve(s, size=(100, 100), keep_on=[(0,0), (0,99), (99,99), (99,0)])

print s
print len(filter(lambda x: x=='#',s))
