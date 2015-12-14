import re
# --- Day 14: Reindeer Olympics ---

# This year is the Reindeer Olympics! Reindeer can fly at high speeds,
# but must rest occasionally to recover their energy. Santa would like to know which
# of his reindeer is fastest, and so he has them race.

# Reindeer can only either be flying (always at their top speed) or resting
# (not moving at all), and always spend whole seconds in either state.

# For example, suppose you have the following Reindeer:

# Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
# Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

eval_template = re.compile('(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
def eval_input(input):
    """Returns a representation of the model as a tuple
    (name, velocity, resistance, rest_time)
    """
    elements = eval_template.match(input).groups()
    return ( elements[0], int(elements[1]), int(elements[2]), int(elements[3]) )

assert eval_input("Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.") == ('Comet', 14, 10, 127)

def reindeer(seconds, config):
    name, velocity, resistance, rest_time = config

    walked_distance = 0
    steps = 0

    while seconds > 0:
        if (steps > 0) and (steps % resistance == 0):
            seconds -= rest_time
            steps = 0
        else:
            seconds -= 1
            walked_distance += velocity
            steps += 1

    return walked_distance


# After one second, Comet has gone 14 km, while Dancer has gone 16 km.
# After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh second,
# Comet begins resting (staying at 140 km), and Dancer continues on for a total distance of 176 km.
# On the 12th second, both reindeer are resting. They continue to rest until the 138th second,
# when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

# In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km
# (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win
# (if the race ended at 1000 seconds).

comet = eval_input("Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.")

assert reindeer(1, comet) == 14
assert reindeer(10, comet) == 140
assert reindeer(1000, comet) == 1120

dancer = eval_input("Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.")
assert reindeer(1, dancer) == 16
assert reindeer(10, dancer) == 160
assert reindeer(1000, dancer) == 1056


# Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds,
# what distance has the winning reindeer traveled?