import weightedBipartiteMatch

if __name__ == '__main__':
	nx = [0, 1, 2]
	ny = [0, 1, 2, 3]
	edge = [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]]
	weight = [[2, 1, 0, 0], [4, 0, 7, 0], [0, 6, 0, 1]]

	print weightedBipartiteMatch.spfa(nx, ny, edge, weight).max_match()
