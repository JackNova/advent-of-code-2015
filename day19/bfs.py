import collections

def breadth_first_search(start, is_goal, successors, heuristic=lambda successor, path, initial_state : True, pick_next=lambda xs: xs.pop()):
	
	frontier = collections.deque([(start, [])])
	visited = collections.defaultdict(bool)
	ops = 0

	while len(frontier) > 0:
		state, path = frontier.pop()
		for s in successors(state):
			if is_goal(s):
				print 'operations: %s' % ops
				return path + [s]
			else:
				if not visited[s] and heuristic(s, path):
					ops += 1
					frontier.appendleft( (s, path+[s]) )
					visited[s] = True
