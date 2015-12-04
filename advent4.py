# -*- coding: utf8 -*-

# --- Day 4: The Ideal Stocking Stuffer ---

# Santa needs help mining some AdventCoins (very similar to bitcoins) to
# use as gifts for all the economically forward-thinking little girls and boys.

# To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
# least five zeroes. The input to the MD5 hash is some secret key
# (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins,
# you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...)
# that produces such a hash.

import md5
import itertools


def mine(n, secret):
	x = secret+str(n)
	m = md5.new()
	m.update(x)
	return m.hexdigest()

# For example:

# If your secret key is abcdef, the answer is 609043, because the MD5 hash
# of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest
# such number to do so.
secret = "abcdef"
number = 609043
assert next(x for x in itertools.count(start=1, step=1) if mine(x, secret).startswith('0'*5)) == number

# If your secret key is pqrstuv, the lowest number it combines with to make an
# MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of
# pqrstuv1048970 looks like 000006136ef....
secret = "pqrstuv"
number = 1048970
assert next(x for x in itertools.count(start=1, step=1) if mine(x, secret).startswith('0'*5)) == number

# let's rock
secret = "ckczppom"
result = next(x for x in itertools.count(start=1, step=1) if mine(x, secret).startswith('0'*5))
print "result for first part of the quiz is following: %s" % result

result2 = next(x for x in itertools.count(start=1, step=1) if mine(x, secret).startswith('0'*6))
print "result for first part of the quiz is following: %s" % result2
