# --- Day 7: Some Assembly Required ---

# This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates!
# Unfortunately, little Bobby is a little under the recommended age range,
# and he needs help assembling the circuit.

# Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal
# (a number from 0 to 65535). A signal is provided to each wire by a gate, another wire,
# or some specific value.

# **Each wire can only get a signal from one source**, but can provide
# its signal to multiple destinations. A gate provides no signal until all of its inputs have a signal.

# The included instructions booklet describe how to connect the parts together:
# x AND y -> z means to connect wires x and y to an AND gate, and then connect its output to wire z.

# For example:

# 123 -> x means that the signal 123 is provided to wire x.
# x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
# p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
# NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.
# Other possible gates include OR (bitwise OR) and RSHIFT (right-shift).
# If, for some reason, you'd like to emulate the circuit instead,
# almost all programming languages (for example, C, JavaScript, or Python) provide operators for these gates.

# For example, here is a simple circuit:

# 123 -> x
# 456 -> y
# x AND y -> d
# x OR y -> e
# x LSHIFT 2 -> f
# y RSHIFT 2 -> g
# NOT x -> h
# NOT y -> i
# After it is run, these are the signals on the wires:

# d: 72
# e: 507
# f: 492
# g: 114
# h: 65412
# i: 65079
# x: 123
# y: 456

with open('input.txt', 'r') as f: input = f.read().splitlines()

def as_topology(expression):
	""" This is the adapter needed in topological_sort
	returns a tuple of kind ``(name, [list of dependancies])``
	"""
	operators = ['NOT', 'AND', 'OR', 'LSHIFT', 'RSHIFT', '->']

	def is_dependency(token):
		return token not in operators and not token.isdigit()

	tokens = expression.split(' ')
	name = tokens[-1]
	dependancies = [d for d in tokens[:-2] if is_dependency(d)]
	return (name, dependancies)

def topological_sort(source, adapter):
    """perform topo sort on elements.
    similar to https://en.wikipedia.org/wiki/Topological_sorting
    http://stackoverflow.com/questions/11557241/python-sorting-a-dependency-list

	:arg adapter: should transform the source in a list of ``(name, [list of dependancies])`` pairs
    :arg source: the original list
    :returns: the original source, with dependancies listed first
    """
    pending = [(adapter(x), x) for x in source]
    pending = [(name, set(deps), original) for (name, deps), original in pending]
    # copy deps so we can modify set in-place       
    emitted = []        
    while pending:
        next_pending = []
        next_emitted = []
        for entry in pending:
            name, deps, original = entry
            deps.difference_update(emitted) # remove deps we emitted last pass
            if deps: # still has deps? recheck during next pass
                next_pending.append(entry) 
            else: # no more deps? time to emit
                yield original 
                emitted.append(name) # <-- not required, but helps preserve original ordering
                next_emitted.append(name) # remember what we emitted for difference_update() in next pass
        if not next_emitted: # all entries have unmet deps, one of two things is wrong...
            raise ValueError("cyclic or missing dependancy detected: %r" % (next_pending,))
        pending = next_pending
        emitted = next_emitted

sorted_input = topological_sort(input, as_topology)

for x in sorted_input:
	print x



# In little Bobby's kit's instructions booklet (provided as your puzzle input),
# what signal is ultimately provided to wire a?