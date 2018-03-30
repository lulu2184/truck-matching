import random

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
            list[request_id] = {}
            for driver in driver_list:
                driver_id, rating, unit_price = driver
                driver_id = int(driver_id)
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget:
                    list[request_id][driver_id] = 1
                else:
                    list[request_id][driver_id] = 0
        return list


    def firstComeFirstServe(self):
        count = 0
        visited = {}
        driver_list = self.driver_list
        request_list = self.request_list
        # initialized dict
        for driver in driver_list:
            driver_id = int(driver[0])
            visited[driver_id] = False

        for request_id, request in enumerate(request_list):
            unit_budget = float(request[0])
            min_rating = float(request[3])
            for driver in driver_list:
                driver_id, rating, unit_price = driver
                driver_id = int(driver_id)
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget and not visited[driver_id]:
                    visited[driver_id] = True
                    count = count + 1
                    break
        return count


    def random_match(self):
        count = 0
        visited = {}
        driver_list = self.driver_list
        request_list = self.request_list
        # initialized dict
        for driver in driver_list:
            driver_id = int(driver[0])
            visited[driver_id] = False

        for request_id, request in enumerate(request_list):
            unit_budget = float(request[0])
            min_rating = float(request[3])
            temp_list = []
            for driver in driver_list:
                driver_id, rating, unit_price = driver
                driver_id = int(driver_id)
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget and not visited[driver_id]:
                    temp_list.append(driver_id)
            if len(temp_list) >= 1:
                list_len = len(temp_list)
                random_index = random.randint(0,list_len - 1)
                visited[temp_list[random_index]] = True
                count = count + 1
        return count

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
