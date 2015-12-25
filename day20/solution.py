# --- Day 20: Infinite Elves and Infinite Houses ---

# To keep the Elves busy, Santa has them deliver some presents by hand,
# door-to-door. He sends them down a street with
# infinite houses numbered sequentially: 1, 2, 3, 4, 5, and so on.

# Each Elf is assigned a number, too, and delivers presents to houses based on that number:

# The first Elf (number 1) delivers presents to every house: 1, 2, 3, 4, 5, ....
# The second Elf (number 2) delivers presents to every second house: 2, 4, 6, 8, 10, ....
# Elf number 3 delivers presents to every third house: 3, 6, 9, 12, 15, ....
# There are infinitely many Elves, numbered starting with 1.
# Each Elf delivers presents equal to ten times his or her number at each house.

def presents(house_number):
	counter = house_number
	result = 0

	while counter > 0:
		if house_number % counter == 0:
			result += counter * 10
		counter -= 1

	return result


		


# So, the first nine houses on the street end up like this:

# House 1 got 10 presents.
assert presents(1) == 10
# House 2 got 30 presents.
assert presents(2) == 30
# House 3 got 40 presents.
assert presents(3) == 40
# House 4 got 70 presents.
assert presents(4) == 70
# House 5 got 60 presents.
assert presents(5) == 60
# House 6 got 120 presents.
assert presents(6) == 120
# House 7 got 80 presents.
assert presents(7) == 80
# House 8 got 150 presents.
assert presents(8) == 150
# House 9 got 130 presents.
assert presents(9) == 130

# The first house gets 10 presents: it is visited only by Elf 1,
# which delivers 1 * 10 = 10 presents.

# The fourth house gets 70 presents, because it is visited by
# Elves 1, 2, and 4, for a total of 10 + 20 + 40 = 70 presents.

# What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?

# Your puzzle input is 29000000.

input = 29000000