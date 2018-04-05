import dbUtil
import listUtil
import hungaryAlgorithm
import weightedBipartiteMatch

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

def weighted_experiment():
	db = dbUtil.dbUtil()

	start_time = 1
	end_time = 1

	driver_limit = 500
	request_limit = 500

	driver_list = db.get_limited_driver_list_by_time(start_time,end_time,driver_limit)
	request_list = db.get_limited_request_list_by_time(start_time,end_time,request_limit)

	print "#driver: ", len(driver_list)
	print "#request: ", len(request_list)

	list_util = listUtil.listUtil(driver_list,request_list)

	# Run random matching and display criteria
	print "Random match: ", list_util.random_match()
	avg_price, avg_rating = list_util.avg_price_rating_for_matching(list_util.random_matching)
	print "     Average price: ", avg_price, "     Average rating: ", avg_rating

	# Run FCFS matching and display criteria
	print "FCFS: ", list_util.firstComeFirstServe()
	avg_price, avg_rating = list_util.avg_price_rating_for_matching(list_util.fcfs_matching)
	print "     Average price: ", avg_price, "     Average rating: ", avg_rating

	# Run weighted bipartite matching
	edge_list, weight = list_util.gen_weighted_edge_list()

	bipartiteMatching = weightedBipartiteMatch.spfa(request_list, driver_list, edge_list, weight)
	num_match, weight_sum = bipartiteMatching.max_match()
	print "Bipartite Match: ", num_match

	matching = bipartiteMatching.get_matching_detail()
	avg_price, avg_rating = list_util.avg_price_rating_for_matching(matching)
	print "     Average price: ", avg_price, "     Average rating: ", avg_rating


if __name__ == '__main__':
	weighted_experiment()
