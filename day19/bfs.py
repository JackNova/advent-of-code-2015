import collections

def breadth_first_search(start, is_goal, successors):
	
	frontier = collections.deque([(start, [])])

	while len(frontier) > 0:
		state, path = frontier.pop()
		for s in successors(state):
			if is_goal(s):
				return path + [s]
			else:
				if not any([x for x, _ in frontier if x==s]):
					frontier.appendleft( (s, path+[s]) )
			# print frontier
