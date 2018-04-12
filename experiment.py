import dbUtil
import listUtil
import hungaryAlgorithm
import weightedBipartiteMatch
import matplotlib.pyplot as plt

def unweighted_experiment():
	db = dbUtil.dbUtil()

	start_time = 1
	end_time = 1

	driver_limit = 2000
	request_limit = 500

	driver_list = db.get_limited_driver_list_by_time(start_time,end_time,driver_limit)
	request_list = db.get_limited_request_list_by_time(start_time,end_time,request_limit)

	print("#driver: ", len(driver_list))
	print("#request: ", len(request_list))

	listUtil = listUtil.listUtil(driver_list,request_list)

	print("Random match: ", listUtil.random_match())
	print("FCFS: ", listUtil.firstComeFirstServe())

	edge_list = listUtil.gen_edge_list()
	match_driver_list = listUtil.gen_driver_id_list(-1)
	match_request_list = listUtil.gen_request_id_list(-1)
	visited = listUtil.gen_driver_id_list(False)

	print("Hungary Match: ",
		hungaryAlgorithm.DFS_hungary(
			request_list,driver_list,
			edge_list,match_request_list,
			match_driver_list,visited).max_match())

class weightedExperiment():
	def __init__(self, driver_limit, request_limit):
		self.db = dbUtil.dbUtil()

		self.start_time = 1
		self.end_time = 1

		self.driver_limit = driver_limit
		self.request_limit = request_limit

		self.driver_list = self.db.get_limited_driver_list_by_time(self.start_time, self.end_time, self.driver_limit)
		self.request_list = self.db.get_limited_request_list_by_time(self.start_time, self.end_time, self.request_limit)

		self.list_util = listUtil.listUtil(self.driver_list, self.request_list)

	# Run random matching and display criteria
	def run_random_matching(self):
		match_num = self.list_util.random_match()
		avg_price, avg_rating = self.list_util.avg_price_rating_for_matching(self.list_util.random_matching)
		return match_num, avg_price, avg_rating

	# Run FCFS matching and display criteria
	def run_FCFS_matching(self):
		match_num = self.list_util.firstComeFirstServe()
		avg_price, avg_rating = self.list_util.avg_price_rating_for_matching(self.list_util.fcfs_matching)
		return match_num, avg_price, avg_rating

	# Run unweighted bipartite matching
	def run_unweighted_matching(self):
		edge_list = self.list_util.gen_edge_list()
		match_driver_list = self.list_util.gen_driver_id_list(-1)
		match_request_list = self.list_util.gen_request_id_list(-1)
		visited = self.list_util.gen_driver_id_list(False)
		unweightedMatching = hungaryAlgorithm.DFS_hungary(
			self.request_list,
			self.driver_list,
			edge_list,
			match_request_list,
			match_driver_list,
			visited)

		match_num = unweightedMatching.max_match()
		matching = unweightedMatching.get_matching()
		avg_price, avg_rating = self.list_util.avg_price_rating_for_matching(matching)
		return match_num, avg_price, avg_rating

	# Run weighted bipartite matching
	def run_weighted_matching(self):
		edge_list, weight = self.list_util.gen_weighted_edge_list()
		bipartiteMatching = weightedBipartiteMatch.spfa(self.request_list, self.driver_list, edge_list, weight)
		num_match, weight_sum = bipartiteMatching.max_match()

		matching = bipartiteMatching.get_matching_detail()
		avg_price, avg_rating = self.list_util.avg_price_rating_for_matching(matching)
		return num_match, avg_price, avg_rating

def display_result(method, matched, avg_price, avg_rating):
	print "[{}] Matched: {}  Average price: {}  Average rating: {}".format(
		method, matched, avg_price, avg_rating)

def draw_one_figure(fig_id, title, ylabel, legend_pos, col, x, num_request,
	random_result, fcfs_result, unweighted_result, weighted_result):
	if col == 0:
		y_random = [float(m[col]) / float(rnum) for m, rnum in zip(random_result, num_request)]
		y_fcfs = [float(m[col]) / float(rnum) for m, rnum in zip(fcfs_result, num_request)]
		y_unweighted = [float(m[col]) / float(rnum) for m, rnum in zip(unweighted_result, num_request)]
		y_weighted = [float(m[col]) / float(rnum) for m, rnum in zip(weighted_result, num_request)]
	else:
		y_random = [float(m[col]) for m in random_result]
		y_fcfs = [float(m[col]) for m in fcfs_result]
		y_unweighted = [float(m[col]) for m in unweighted_result]
		y_weighted = [float(m[col]) for m in weighted_result]
	plt.figure(fig_id)
	plt.title(title)
	plt.xlabel('#drivers/#requests')
	plt.ylabel(ylabel)
	plt.plot(x, y_random, 'yo-', label='random')
	plt.plot(x, y_fcfs, 'co-', label = 'FCFS')
	if col == 0:
		plt.plot(x, y_weighted, 'ro-', label='bipartite matching')
	else:
		plt.plot(x, y_unweighted, 'bo-', label='unweighted bipartite')
		plt.plot(x, y_weighted, 'ro-', label='weighted bipartite')
	plt.legend(loc=legend_pos)
	plt.show()

def visualize(num_driver, num_request, random_result, fcfs_result, unweighted_result, weighted_result):
	x = [float(dnum) / float(rnum) for dnum, rnum in zip(num_driver, num_request)]
	draw_one_figure(1, 'Experimental Matched Number Result', '#matched/#requests', 'lower right', 0, x,
		num_request, random_result, fcfs_result, unweighted_result, weighted_result)
	draw_one_figure(2, 'Experimental Average Unit Price Result', 'average unit price', 'upper right', 1, x,
		num_request, random_result, fcfs_result, unweighted_result, weighted_result)
	draw_one_figure(3, 'Experimental Average Rating Result', 'average rating', 'upper left', 2, x,
		num_request, random_result, fcfs_result, unweighted_result, weighted_result)

def weighted_experiment():
	driver_sizes = [100, 200, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000]
	request_sizes = [500] * 11

	random_result = []
	fcfs_result = []
	unweighted_result = []
	weighted_result = []
	num_driver = []
	num_request = []

	for dnum, rnum in zip(driver_sizes, request_sizes):
		exp = weightedExperiment(dnum, rnum)
		print "#driver: ", len(exp.driver_list), "  #request: ", len(exp.request_list)

		num_driver.append(len(exp.driver_list))
		num_request.append(len(exp.request_list))

		# Run random
		num_match, avg_price, avg_rating = exp.run_random_matching()
		display_result("Random", num_match, avg_price, avg_rating)
		random_result.append((num_match, avg_price, avg_rating))

		# Run FCFS
		num_match, avg_price, avg_rating = exp.run_FCFS_matching()
		display_result("FCFS", num_match, avg_price, avg_rating)
		fcfs_result.append((num_match, avg_price, avg_rating))

		# Run unweighted bipartite matching
		num_match, avg_price, avg_rating = exp.run_unweighted_matching()
		display_result("Unweighted bipartite", num_match, avg_price, avg_rating)
		unweighted_result.append((num_match, avg_price, avg_rating))

		# Run weighted bipartite matching
		num_match, avg_price, avg_rating = exp.run_weighted_matching()
		display_result("Weighted bipartite", num_match, avg_price, avg_rating)
		weighted_result.append((num_match, avg_price, avg_rating))

	visualize(num_driver, num_request, random_result, fcfs_result, unweighted_result, weighted_result)

if __name__ == '__main__':
	weighted_experiment()
