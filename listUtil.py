import random
from math import radians, cos, sin, asin, sqrt
import numpy as np

class listUtil():
    def __init__(self, driver_list, request_list):
        self.M = []
        self.driver_list = driver_list
        self.request_list = request_list
        self.min_rating = min([float(driver[1]) for driver in self.driver_list])
        self.max_rating = max([float(driver[1]) for driver in self.driver_list])
        self.min_price = min([float(driver[2]) for driver in self.driver_list])
        self.max_price = max([float(driver[2]) for driver in self.driver_list])
        # x-axis is driver capacity, y-axis is request weight
        self.match_matrix = [[8,4,2],[1,8,4],[1,1,8]]
        self.acceptable_dist = 10

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def gen_edge_list(self):
        list = {}
        driver_list = self.driver_list
        request_list = self.request_list
        for request_id, request in enumerate(request_list):
            unit_budget, req_weight, min_rating, req_lat, req_lon = self.parse_request(request)
            list[request_id] = {}
            for driver in driver_list:
                driver_id, rating, unit_price, capacity, dri_lat, dri_lon = self.parse_driver(driver)
                dist = abs(self.haversine(dri_lon,dri_lat,req_lon,req_lat))
                if dist != 0:
                    self.M.append(dist)
                # same lon and lat, discard results
                if dri_lat == req_lat and dri_lon == req_lon :
                    list[request_id][driver_id] = 0
                # price, rating, weight match and within acceptable distance
                elif rating >= min_rating and unit_price <= unit_budget and req_weight <= capacity \
                        and dist <= self.acceptable_dist:
                    list[request_id][driver_id] = 1
                else:
                    list[request_id][driver_id] = 0
        return list


    def gen_weighted_edge_list(self):
        list = {}
        weight = {}
        driver_list = self.driver_list
        request_list = self.request_list
        for request_id, request in enumerate(request_list):
            unit_budget, req_weight, min_rating, req_lat, req_lon = self.parse_request(request)
            list[request_id] = {}
            weight[request_id] = {}
            for driver_id, driver in enumerate(driver_list):
                _, rating, unit_price, capacity, dri_lat, dri_lon = self.parse_driver(driver)
                dist = abs(self.haversine(dri_lon, dri_lat, req_lon, req_lat))
                if dri_lat == req_lat and dri_lon == req_lon :
                    list[request_id][driver_id] = 0
                # price, rating, weight match and within acceptable distance
                elif rating >= min_rating and unit_price <= unit_budget and req_weight <= capacity \
                        and dist <= self.acceptable_dist:
                    list[request_id][driver_id] = 1
                    weight[request_id][driver_id] = self.calculate_weight(unit_price, rating, req_weight, capacity, dist)
                else:
                    list[request_id][driver_id] = 0
        return list, weight

    def car_type_match_factor_generator(self,req_weight,capacity):
        req_type = int(req_weight / 10.0)
        dri_type = int(capacity / 10.0)
        return self.match_matrix[req_type][dri_type]

    def calculate_weight(self, price, rating,weight,capacity, dist):
        price_range = self.max_price - self.min_price
        rating_range = self.max_rating - self.min_rating
        dist_range = max(self.M) - min(self.M)
        return abs(  (price - self.min_price) / price_range   +
                1 - (rating - self.min_rating) / rating_range ) + \
                dist


    def firstComeFirstServe(self):
        count = 0
        visited = {}
        driver_list = self.driver_list
        request_list = self.request_list
        self.fcfs_matching = []
        # initialized dict
        for driver in driver_list:
            driver_id = int(driver[0])
            visited[driver_id] = False

        for request_id, request in enumerate(request_list):
            unit_budget, req_weight, min_rating, req_lat, req_lon = self.parse_request(request)
            for ind, driver in enumerate(driver_list):
                driver_id, rating, unit_price, capacity, dri_lat, dri_lon = self.parse_driver(driver)
                dist = abs(self.haversine(dri_lon, dri_lat, req_lon, req_lat))
                if rating >= min_rating and unit_price <= unit_budget and not visited[driver_id] \
                        and dist <= self.acceptable_dist and req_weight <= capacity:
                    visited[driver_id] = True
                    count = count + 1
                    # request, driver
                    self.fcfs_matching.append((request_id, ind))
                    break
        return count

    def random_match(self):
        count = 0
        visited = {}
        driver_list = self.driver_list
        request_list = self.request_list
        self.random_matching = []
        # initialized dict
        for driver in driver_list:
            driver_id = int(driver[0])
            visited[driver_id] = False

        for request_id, request in enumerate(request_list):
            unit_budget, req_weight, min_rating, req_lat, req_lon = self.parse_request(request)
            temp_list = []
            temp_ind = []
            for ind, driver in enumerate(driver_list):
                driver_id, rating, unit_price, capacity, dri_lat, dri_lon = self.parse_driver(driver)
                dist = abs(self.haversine(dri_lon, dri_lat, req_lon, req_lat))
                if rating >= min_rating and unit_price <= unit_budget and not visited[driver_id] \
                        and dist <= self.acceptable_dist and req_weight <= capacity:
                    temp_list.append(driver_id)
                    temp_ind.append(ind)
            if len(temp_list) >= 1:
                list_len = len(temp_list)
                random_index = random.randint(0,list_len - 1)
                visited[temp_list[random_index]] = True
                count = count + 1
                # request, driver
                self.random_matching.append((request_id, temp_ind[random_index]))
        return count

    def parse_driver(self,driver):
        driver_id, rating, unit_price, capacity, lat, lon = driver
        driver_id = int(driver_id)
        rating = float(rating)
        unit_price = float(unit_price)
        capacity = int(capacity)
        dri_lat = float(lat)
        dri_lon = float(lon)
        return driver_id, rating, unit_price, capacity, dri_lat, dri_lon

    def parse_request(self,request):
        unit_budget = float(request[0])
        req_weight = float(request[1])
        min_rating = float(request[4])
        req_lat = float(request[5])
        req_lon = float(request[6])
        return unit_budget, req_weight, min_rating, req_lat, req_lon

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

    def statistic_for_matching(self, matching):
        sum_rating = 0
        sum_price = 0
        distance = 0
        total_capacity = 0
        total_weight = 0
        for inr, ind in matching:
            _, rating, unit_price, capacity, lat, lon = self.driver_list[ind]
            unit_budget, req_weight, min_rating, req_lat, req_lon = self.parse_request(self.request_list[inr])
            sum_price += unit_price
            sum_rating += rating
            distance += abs(self.haversine(lon,lat,req_lon,req_lat))
            total_capacity += capacity
            total_weight += req_weight
        return sum_price / len(matching), sum_rating / len(matching), \
               distance / len(matching), total_weight / total_capacity


    def print_max_min_dist(self):
        print max(self.M),min(self.M)