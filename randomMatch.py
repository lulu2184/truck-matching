import dbUtil
import listUtil
import hungaryAlgorithm


# driver id,rating,unit_price
# request unit_budget, min_rating
if __name__ == '__main__':
    db = dbUtil.dbUtil()

    start_time = 1
    end_time = 1

    driver_list = db.get_driver_list_by_time(start_time,end_time)
    request_list = db.get_request_list_by_time(start_time,end_time)
    listUtil = listUtil.listUtil(driver_list,request_list)

    print listUtil.random_match()




