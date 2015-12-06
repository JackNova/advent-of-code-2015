# --- Day 5: Doesn't He Have Intern-Elves For This? ---
from itertools import groupby
from operator import itemgetter

with open('input.txt') as f: input = f.read().splitlines()

print "First 5 instances of input records are %s" % input[0:5]
print "Records ends with %s" % input[-3:]

# Santa needs help figuring out which strings in his text file are naughty or nice.

# A nice string is one with all of the following properties:

# It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
def contains_at_least_3_vowels(s):
	return len([c for c in s if c in 'aeiou']) >= 3

assert contains_at_least_3_vowels('xazegov')
assert contains_at_least_3_vowels('aeiouaeiouaeiou')
assert not contains_at_least_3_vowels('zrazz')

# It contains at least one letter that appears twice in a row, like xx, abcdde (dd),
# or aabbccdd (aa, bb, cc, or dd).
def contains_at_least_one_letter_that_appears_twice_in_a_row(s):
	letters = [[k,len(list(g))] for k, g in groupby(s)]
	return any([ x[1]>=2 for x in letters])

assert contains_at_least_one_letter_that_appears_twice_in_a_row('xx')
assert contains_at_least_one_letter_that_appears_twice_in_a_row('abcdde')
assert contains_at_least_one_letter_that_appears_twice_in_a_row('aabbccdd')
assert not contains_at_least_one_letter_that_appears_twice_in_a_row('ciao')

# It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
def contains(x, strings=['ab', 'cd', 'pq', 'xy']):
	return any([s in x for s in strings])

assert not contains('dario')
assert contains('babbo')

def is_nice(s):
	return contains_at_least_3_vowels(s) and \
		contains_at_least_one_letter_that_appears_twice_in_a_row(s) and	\
		not contains(s)

# For example:
# ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...),
# a double letter (...dd...), and none of the disallowed substrings.
assert is_nice('ugknbfddgicrmopn')

# aaa is nice because it has at least three vowels and a double letter,
# even though the letters used by different rules overlap.
assert is_nice('aaa')

# jchzalrnumimnmhp is naughty because it has no double letter.
assert not is_nice('jchzalrnumimnmhp')

# haegwjzuvuyypxyu is naughty because it contains the string xy.
assert not is_nice('haegwjzuvuyypxyu')

# dvszwmarrgswjxmb is naughty because it contains only one vowel.
assert not is_nice('dvszwmarrgswjxmb')

# How many strings are nice?
nice_strings = [s for s in input if is_nice(s)]
print "we have %s nice strings" % len(nice_strings)


# --- Part Two ---

# Realizing the error of his ways, Santa has switched to a better model of determining
# whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

# Now, a nice string is one with all of the following properties:

# It contains a pair of any two letters that appears at least twice in the string without
# overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
def split_by_n( seq, n ):
	"""Returns a list of tuple (chunk, index)"""
	idx = 0
	while seq:
		yield (seq[:n], idx)
		idx += 1
		seq = seq[1:]
		if len(seq)<n:
			break

def contains_non_consecutive_indexes(xs):
	my_xs = sorted(xs)
	return any( my_xs[i+1]-my_xs[i] > 1 for i in xrange(len(my_xs)-1) )

def contains_pair_twice(s):
	pairs = list(split_by_n(s, 2))
	chunks = {}
	
	for chunk, index in pairs:
		if chunks.get(chunk):
			chunks[chunk].append(index)
		else:
			chunks[chunk] = [index]

	repeating_pairs_indexes = [v for k, v in chunks.items() if len(v) > 1]
	return any(contains_non_consecutive_indexes(p) for p in repeating_pairs_indexes)
			

assert contains_pair_twice('xyxy')
assert contains_pair_twice('aabcdefgaa')
assert not contains_pair_twice('aaa')

# It contains at least one letter which repeats with exactly one letter between them,
# like xyx, abcdefeghi (efe), or even aaa.
def contains_at_least_one_letter_which_repeats_with_one_letter_between(s):
	return any(s[i] == s[i+2] for i in xrange(len(s)-2))

assert contains_at_least_one_letter_which_repeats_with_one_letter_between('xyx')
assert contains_at_least_one_letter_which_repeats_with_one_letter_between('efe')
assert contains_at_least_one_letter_which_repeats_with_one_letter_between('aaa')
assert not contains_at_least_one_letter_which_repeats_with_one_letter_between('dario')

def is_cool(s):
	return contains_pair_twice(s) and \
		contains_at_least_one_letter_which_repeats_with_one_letter_between(s)

# For example:

# qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that
# repeats with exactly one letter between them (zxz).
assert is_cool('qjhvhtzxzqqjkmpb')

# xxyxx is nice because it has a pair that appears twice and a letter that repeats with
# one between, even though the letters used by each rule overlap.
assert is_cool('xxyxx')

# uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
assert not is_cool('uurcxstgmygtbstg')

# ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo),
# but no pair that appears twice.
assert not is_cool('ieodomkazucvgmuy')

# How many strings are nice under these new rules?

cool_items = [s for s in input if is_cool(s)]
print "we have %s cool strings" % len(cool_items)