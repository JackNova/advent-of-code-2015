import re
from collections import defaultdict
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

    return (walked_distance, name)


# After one second, Comet has gone 14 km, while Dancer has gone 16 km.
# After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh second,
# Comet begins resting (staying at 140 km), and Dancer continues on for a total distance of 176 km.
# On the 12th second, both reindeer are resting. They continue to rest until the 138th second,
# when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

# In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km
# (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win
# (if the race ended at 1000 seconds).

comet = eval_input("Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.")

assert reindeer(1, comet) == (14, 'Comet')
assert reindeer(10, comet) == (140, 'Comet')
assert reindeer(1000, comet) == (1120, 'Comet')

dancer = eval_input("Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.")
assert reindeer(1, dancer) == (16, "Dancer")
assert reindeer(10, dancer) == (160, "Dancer")
assert reindeer(1000, dancer) == (1056, "Dancer")


# Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds,
# what distance has the winning reindeer traveled?

with open('input.txt', 'r') as f: input = f.read().splitlines()

results = [ reindeer(2503, eval_input(x)) for x in input ]
print results
print max(results, key=lambda x: x[0])

# --- Part Two ---

# Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

# Instead, at the end of each second, he awards one point to the reindeer currently in the lead.
# (If there are multiple reindeer tied for the lead, they each get one point.)
# He keeps the traditional 2503 second time limit, of course, as doing otherwise would be entirely ridiculous.

# Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point.
# He stays in the lead until several seconds into Comet's second burst: after the 140th second, Comet pulls
# into the lead and gets his first point. Of course, since Dancer had been in the lead
# for the 139 seconds before that, he has accumulated 139 points by the 140th second.

# After the 1000th second, Dancer has accumulated 689 points, while poor Comet,
# our old champion, only has 312. So, with the new scoring system, Dancer would win
# (if the race ended at 1000 seconds).

# Again given the descriptions of each reindeer (in your puzzle input), after exactly 2503
# seconds, how many points does the winning reindeer have?

partecipants = [eval_input(x) for x in input]
points = defaultdict(int)
for s in range(1, 2503+1):
    leaderbord = sorted( [ reindeer(s, deer) for deer in partecipants ], key=lambda x: -x[0] )
    leader_position = leaderbord[0][0]

    for leader in leaderbord:
        km, name = leader
        if km == leader_position:
            points[name] += 1
            
print points



