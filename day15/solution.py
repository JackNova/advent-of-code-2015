import re
import operator
from itertools import permutations


def prod(iterable):
	return reduce(operator.mul, iterable, 1)

# --- Day 15: Science for Hungry People ---

# Today, you set out on the task of perfecting your milk-dunking cookie recipe.
# All you have to do is find the right balance of ingredients.

# Your recipe leaves room for exactly 100 teaspoons of ingredients.
# You make a list of the remaining ingredients you could use to finish the recipe
# (your puzzle input) and their properties per teaspoon:

# capacity (how well it helps the cookie absorb milk)
# durability (how well it keeps the cookie intact when full of milk)
# flavor (how tasty it makes the cookie)
# texture (how it improves the feel of the cookie)
# calories (how many calories it adds to the cookie)
# You can only measure ingredients in whole-teaspoon amounts accurately,
# and you have to be accurate so you can reproduce your results in the future.

# The total score of a cookie can be found by adding up each of the properties
# (negative totals become 0) and then multiplying together everything except calories.


# For instance, suppose you have these two ingredients:

ingredients = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3""".splitlines()

eval_template = re.compile('(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')
def eval_input(input):
    """Returns a representation of the model as a tuple
    (name, capacity, durability, flavor, texture, calories)
    """
    elements = eval_template.match(input).groups()
    return ( elements[0], int(elements[1]), int(elements[2]), int(elements[3]), int(elements[4]), int(elements[5]) )

assert eval_input("Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8") == ('Butterscotch', -1, -2, 6, 3, 8)

# Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon
# (because the amounts of each ingredient must add up to 100)
# would result in a cookie with the following properties:

# A capacity of 44*-1 + 56*2 = 68
# A durability of 44*-2 + 56*3 = 80
# A flavor of 44*6 + 56*-2 = 152
# A texture of 44*3 + 56*-1 = 76

# Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now)
# results in a total score of 62842880, which happens to be the best score possible

def evaluate_recipe(recipe):
	""" the recipe should be of the form 
	[(quantity, ingredient), ...]
	example: [(44, butterscotch), ...]
	where the ingredient is of kind
	(name, capacity, durability, flavor, texture, calories)
	returns (value, total_calories)
	"""
	total_capacity = 0
	total_durability = 0
	total_flavor = 0
	total_texture = 0

	total_calories = 0

	for teaspoons, ingredient in recipe:
		name, capacity, durability, flavor, texture, calories = ingredient
		total_capacity += capacity * teaspoons
		total_durability += durability * teaspoons
		total_flavor += flavor * teaspoons
		total_texture += texture * teaspoons

		total_calories += calories * teaspoons

	gtz = [n if n>=0 else 0 for n in [total_capacity, total_durability, total_flavor, total_texture] ]
	value = prod(gtz)
	return ( value, total_calories )

butterscotch = eval_input("Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8")
cinnamon = eval_input("Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3")

test_recipe = [(44, butterscotch), (56, cinnamon)]

assert evaluate_recipe(test_recipe) == (62842880, 520)

def partitions(n,k,l=1):
    '''n is the integer to partition, k is the length of partitions, l is the min partition element size'''
    if k < 1:
        raise StopIteration
    if k == 1:
        if n >= l:
            yield (n,)
        raise StopIteration
    for i in range(l,n+1):
        for result in partitions(n-i,k-1,i):
            yield (i,)+result

def partitions_permutations(n, k):
	xs = partitions(n, k)
	for x in xs:
		for p in permutations(x):
			yield p

xs = list(partitions_permutations(100, 4))
assert len(xs) == 171672
assert len(set(xs)) == 156849

# given these ingredients. If any properties had produced a negative total,
# it would have instead become zero, causing the whole score to multiply to zero.

# Given the ingredients in your kitchen and their properties, what is the total
# score of the highest-scoring cookie you can make?

def bake(teaspoons, ingredients_str):
	ingredients = [eval_input(s) for s in ingredients_str]
	attempts = [( amounts, evaluate_recipe( zip(amounts, ingredients) ) ) for amounts in partitions_permutations(teaspoons, len(ingredients))]
	return max(attempts, key=lambda (amounts, (value, calories)): value)

result_amounts, (result_value, result_calories) = bake(100, ingredients)
assert result_amounts == (44, 56)
assert result_value == 62842880
assert result_calories == 520

with open('input.txt', 'r') as f: input = f.read().splitlines()

result_amounts, (result_value, result_calories) = bake(100, input)

print """The best recipe you can bake will have a value of %s and will be composed by the following
amounts of ingrediens (in order) %s. 
By the way, it will have %s calories""" % (result_value, result_amounts, result_calories)


# --- Part Two ---

# Your cookie recipe becomes wildly popular! Someone asks if you can make another recipe
# that has exactly 500 calories per cookie (so they can use it as a meal replacement).
# Keep the rest of your award-winning process the same (100 teaspoons, same ingredients, same scoring system).

# For example, given the ingredients above, if you had instead selected 40 teaspoons
# of butterscotch and 60 teaspoons of cinnamon (which still adds to 100), the total calorie
# count would be 40*8 + 60*3 = 500. The total score would go down, though: only 57600000,
# the best you can do in such trying circumstances.

# Given the ingredients in your kitchen and their properties, what is the total score of the
# highest-scoring cookie you can make with a calorie total of 500?

