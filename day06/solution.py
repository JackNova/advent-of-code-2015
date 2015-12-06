# --- Day 6: Probably a Fire Hazard ---

import numpy as np
import re

# Because your neighbors keep defeating you in the holiday house decorating contest
# year after year, you've decided to deploy one million lights in a 1000x1000 grid.

lights = np.ones( (1000, 1000) ) * -1

print "starting matrix has size %s" % lights.size
print "some elements are \n %s" % lights[:3, :3]
assert sum(lights.flatten(1)) == -1000000

# Furthermore, because you've been especially nice this year, Santa has mailed
# you instructions on how to display the ideal lighting configuration.

# Lights in your grid are numbered from 0 to 999 in each direction;
# the lights at each corner are at 0,0, 0,999, 999,999, and 999,0.
# The instructions include whether to turn on, turn off, or toggle various
# inclusive ranges given as coordinate pairs. Each coordinate pair represents
# opposite corners of a rectangle, inclusive; a coordinate pair like 0,0
# through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

# To defeat your neighbors this year, all you have to do is set up your lights
# by doing the instructions Santa sent you in order.
def turn_on(M, start_row, end_row, start_col, end_col):
	M[start_row:end_row, start_col:end_col] = 1

def turn_off(M, start_row, end_row, start_col, end_col):
	M[start_row:end_row, start_col:end_col] = -1

def toggle_op(M, start_row, end_row, start_col, end_col):
	M[start_row:end_row, start_col:end_col] *= -1

def parse(s):
	on = re.compile('turn on (\d+),(\d+) through (\d+),(\d+)')
	off = re.compile('turn off (\d+),(\d+) through (\d+),(\d+)')
	toggle = re.compile('toggle (\d+),(\d+) through (\d+),(\d+)')

	m = on.match(s)
	if m:
		return (turn_on, int(m.group(1)), 1+int(m.group(3)), int(m.group(2)), 1+int(m.group(4)))

	m = off.match(s)
	if m:
		return (turn_off, int(m.group(1)), 1+int(m.group(3)), int(m.group(2)), 1+int(m.group(4)))

	m = toggle.match(s)
	if m:
		return (toggle_op, int(m.group(1)), 1+int(m.group(3)), int(m.group(2)), 1+int(m.group(4)))

def eval(exp, lights):
	(op, start_row, end_row, start_col, end_col) = parse(exp)
	op(lights, start_row, end_row, start_col, end_col)

# For example:

# turn on 0,0 through 999,999 would turn on (or leave on) every light.
instruction = "turn on 0,0 through 999,999"
eval(instruction, lights)
assert sum(lights.flatten(1)) == 10**6

# toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
# turning off the ones that were on, and turning on the ones that were off.
instruction = "toggle 0,0 through 999,0"
eval(instruction, lights)
assert sum([x for x in lights.flatten(1) if x>0]) == 10**6 - 1000 # 1+1-1 = 1

# turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
eval("turn off 499,499 through 500,500", lights)
assert sum([x for x in lights.flatten(1) if x>0]) == 10**6 - 1000 - 4

# After following the instructions, how many lights are lit?

lights = np.ones( (1000, 1000) ) * -1
with open('input.txt') as f: input = f.read().splitlines()
for exp in input:
	eval(exp, lights)
lit = [x for x in lights.flatten(1) if x>0]
print "there are %s lights lit" % len(lit)

# --- Part Two ---

# You just finish implementing your winning light pattern when you realize
# you mistranslated Santa's message from Ancient Nordic Elvish.

# The light grid you bought actually has individual brightness controls;
# each light can have a brightness of zero or more. The lights all start at zero.

# The phrase turn on actually means that you should increase the brightness of those lights by 1.

# The phrase turn off actually means that you should decrease the brightness of those lights by 1,
# to a minimum of zero.

# The phrase toggle actually means that you should increase the brightness of those lights by 2.

# What is the total brightness of all lights combined after following Santa's instructions?

# For example:

# turn on 0,0 through 0,0 would increase the total brightness by 1.
# toggle 0,0 through 999,999 would increase the total brightness by 2000000.


