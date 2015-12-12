from string import ascii_lowercase as letters
import re

# --- Day 11: Corporate Policy ---

# Santa's previous password expired, and he needs help choosing a new one.

# To help him remember his new password after the old one expires,
# Santa has devised a method of coming up with a password based on the previous one.
# Corporate policy dictates that passwords must be exactly eight lowercase letters (for security reasons),
# so he finds his new password by incrementing his old password string repeatedly until it is valid.

# Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on.
# Increase the rightmost letter one step; if it was z, it wraps around to a,
# and repeat with the next letter to the left until one doesn't wrap around.

def increment(s):
	try:
		return s[0:-1] + letters[ letters.index( s[-1] ) + 1 ]
	except IndexError:
		return increment(s[0:-1]) + letters[0]

assert increment('xz') == 'ya'

# Unfortunately for Santa, a new Security-Elf recently started, and he has imposed
# some additional password requirements:

# Passwords must include one increasing straight of at least three letters,
# like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.

def has_straight(pwd):
	indexes = [ord(c) for c in pwd]
	for idx, c in enumerate(indexes):
		try:
			if c == indexes[idx+1]-1 == indexes[idx+2]-2 :
				return True
		except IndexError:
			return False

assert has_straight('xabcf')
assert not has_straight('abd')

# Passwords may not contain the letters i, o, or l, as these letters can be mistaken
# for other characters and are therefore confusing.
confusing_expression = re.compile('[iol]+')
def has_confusing_letters(pwd):
	return confusing_expression.search(pwd)


assert has_confusing_letters('dario')
assert not has_confusing_letters('dar')

# Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
paris_expression = re.compile(r'(.)\1')
def has_two_pairs(pwd):
	return len( paris_expression.findall(pwd) ) >=2

assert has_two_pairs('ddaxxxxxrioo')
assert not has_two_pairs('dario')
# For example:

# hijklmmn meets the first requirement (because it contains the straight hij) but
assert has_straight('hijklmmn')
# fails the second requirement requirement (because it contains i and l).
assert has_confusing_letters('hijklmmn')
# abbceffg meets the third requirement (because it repeats bb and ff)
assert has_two_pairs('abbceffg')
# but fails the first requirement.
assert not has_straight('abbceffg')
# abbcegjk fails the third requirement, because it only has one double letter (bb).

def fulfills_policy(pwd):
	return has_straight(pwd) and (not has_confusing_letters(pwd)) and has_two_pairs(pwd)

def next_password(pwd):
	while True:
		pwd = increment(pwd)
		if fulfills_policy(pwd):
			return pwd

# The next password after abcdefgh is abcdffaa.
assert fulfills_policy('abcdffaa')
assert next_password('abcdefgh') == 'abcdffaa'

# The next password after ghijklmn is ghjaabcc, because you eventually skip all the
# passwords that start with ghi..., since i is not allowed.
assert fulfills_policy('ghjaabcc')
assert next_password('ghijklmn') == 'ghjaabcc'

# Given Santa's current password (your puzzle input), what should his next password be?

# Your puzzle input is 
# input = 'hepxcrrq'
# print next_password(input)
input2 = 'hepxxyzz'
print next_password(input2)
