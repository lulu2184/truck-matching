import dbUtil
import listUtil
import hungaryAlgorithm


if __name__ == '__main__':
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