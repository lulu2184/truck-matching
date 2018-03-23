class listUtil():
    def __init__(self, driver_list, request_list):
        self.driver_list = driver_list
        self.request_list = request_list

    def gen_edge_list(self):
        list = {}
        driver_list = self.driver_list
        request_list = self.request_list
        for request_id, request in enumerate(request_list):
            unit_budget = float(request[0])
            min_rating = float(request[3])
            for driver in driver_list:
                driver_id, rating, unit_price = driver
                driver_id = int(driver_id)
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget:
                    list[request_id][driver_id] = 1
        return list

    def gen_driver_id_list(self,value):
        list = {}
        driver_list = self.driver_list
        for driver in driver_list:
            driver_id = int(driver[0])
            list[driver_id] = value
        return list

    def gen_request_id_list(self,value):
        list = {}
        request_list = self.request_list
        for n,request in enumerate(request_list):
            list[n] = value
        return list
