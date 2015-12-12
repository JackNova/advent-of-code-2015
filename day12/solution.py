import re
# --- Day 12: JSAbacusFramework.io ---

# Santa's Accounting-Elves need help balancing the books after a recent order.
# Unfortunately, their accounting software uses a peculiar storage format. That's where you come in.

# They have a JSON document which contains a variety of things:
# arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings.
# Your first job is to simply find all of the numbers throughout the document and add them together.

def sum_numbers(s):
	numbers_expression = re.compile('-?\d+')
	xs = numbers_expression.findall(s)
	return sum([int(x) for x in xs])

# For example:

# [1,2,3] and {"a":2,"b":4} both have a sum of 6.
assert sum_numbers('[1,2,3]') == 6
assert sum_numbers('{"a":2,"b":4}') == 6

# [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
assert sum_numbers('[[[3]]]') == 3
assert sum_numbers('{"a":{"b":4},"c":-1}') == 3

# {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
assert sum_numbers('{"a":[-1,1]}') == 0
assert sum_numbers('[-1,{"a":1}]') == 0

# [] and {} both have a sum of 0.
assert sum_numbers('[]') == 0
assert sum_numbers('{}') == 0

# You will not encounter any strings containing numbers.

# What is the sum of all numbers in the document?

with open('input.txt', 'r') as f: input = f.read()
print sum_numbers(input)

