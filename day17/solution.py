from itertools import combinations, permutations

# --- Day 17: No Such Thing as Too Much ---

# The elves bought too much eggnog again - 150 liters this time.
# To fit it all into your refrigerator, you'll need to move it into smaller containers.
# You take an inventory of the capacities of the available containers.

# For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters.
# def make_unikque(xs):
# 	for n in range(0, len(xs)):
# 		yield (str(n), xs[n])

test_sizes = [20, 15, 10, 5, 5]
# If you need to store 25 liters, there are four ways to do it:

# 15 and 10
# 20 and 5 (the first 5)
# 20 and 5 (the second 5)
# 15, 5, and 5

def ways_to_store(liters, sizes):
	for n in range(len(sizes)+1):
		ways = [x for x in combinations(sizes, n) if sum(x) == liters]
		for w in ways:
			yield w



test_result = list(ways_to_store(25, test_sizes))
print test_result
assert len(test_result) == 4


# Filling all containers entirely, how many different combinations of containers
# can exactly fit all 150 liters of eggnog?

with open('input.txt', 'r') as f: input = f.read().splitlines()
sizes = [int(s) for s in input]

result_1 = list(ways_to_store(150, sizes))
print len(result_1)

