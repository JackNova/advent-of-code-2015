import collections

def breadth_first_search(start, is_goal, successors, heuristic=lambda successor, path, initial_state : True, pick_next=lambda xs: xs.pop()):

	print '#'*50
	print 'starting search for %s ' % start
	
	frontier = collections.deque([(start, [])])
	visited = collections.defaultdict(bool)
	ops = 0

	while len(frontier) > 0 and ops < 100000:
		# fucking pick the shorter state first! doesn't simply pop!
		state, path = pick_next(frontier)
		# print 'computing state %s, path %s' % (state, path)
		for s in successors(state):
			if is_goal(s):
				print 'got result %s with %s operations' % (s, ops)
				return path + [s]
			else:
				if not visited[s] and heuristic(s, path, start):
					# print 'enqueuing state %s with path %s' % (s, path)
					ops += 1
					frontier.appendleft( (s, path+[s]) )
					visited[s] = True

	sorted_frontier = sorted(frontier, key=lambda x: -len(x[1]))
	print 'at this point computation is stopped. reached %s operations' % ops
	print 'frontier has %s elements' % len(frontier)
	print 'the longest path in the frontier has %s steps ' % len(sorted_frontier[0][1])
	print 'and this is his state %s' % sorted_frontier[0][0]

