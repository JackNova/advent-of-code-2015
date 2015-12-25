import collections

def breadth_first_search(start, is_goal, successors):
	
	frontier = collections.deque([(start, [])])
	visited = collections.defaultdict(bool)

	while len(frontier) > 0:
		state, path = frontier.pop()
		for s in successors(state):
			if is_goal(s):
				return path + [s]
			else:
				if not visited[s]:
					frontier.appendleft( (s, path+[s]) )
					visited[s] = True
