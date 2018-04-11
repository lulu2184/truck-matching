import random
import json
import urllib
import urllib2
import numpy as np

# google API key : AIzaSyC33XFuyHVYjxtc19UYA7vls2PmgKnSBlo

import numpy as np

class listUtil():
    def __init__(self, driver_list, request_list):
        self.driver_list = driver_list
        self.request_list = request_list
        self.min_rating = min([float(driver[1]) for driver in self.driver_list])
        self.max_rating = max([float(driver[1]) for driver in self.driver_list])
        self.min_price = min([float(driver[2]) for driver in self.driver_list])
        self.max_price = max([float(driver[2]) for driver in self.driver_list])


    def cal_distance_by_Google_API(self,driver_lat,driver_lon,request_lat,request_lon):
        map_key = "AIzaSyC33XFuyHVYjxtc19UYA7vls2PmgKnSBlo"
        distance_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"

        url = distance_url + '?' + urllib.urlencode({
            'origins': "%s,%s" % (driver_lat, driver_lon),
            'destinations': "%s,%s" % (request_lat,request_lon),
            'key': map_key,
        })

        while True:
            try:
                # Get the API response.
                response = str(urllib2.urlopen(url).read())
            except IOError:
                pass  # Fall through to the retry loop.
            else:
                # If we didn't get an IOError then parse the result.
                result = json.loads(response.replace('\\n', ''))
                if result['status'] == 'OK':
                    return result['distance']
                elif result['status'] != 'UNKNOWN_ERROR':
                    # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                    # ZERO_RESULTS. There is no point retrying these requests.
                    raise Exception(result['error_message'])

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

    def gen_weighted_edge_list(self):
        list = {}
        weight = {}
        driver_list = self.driver_list
        request_list = self.request_list
        for request_id, request in enumerate(request_list):
            unit_budget = float(request[0])
            min_rating = float(request[3])
            list[request_id] = {}
            weight[request_id] = {}
            for driver_id, driver in enumerate(driver_list):
                _, rating, unit_price = driver
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget:
                    list[request_id][driver_id] = 1
                    weight[request_id][driver_id] = self.calculate_weight(unit_price, rating)
                else:
                    list[request_id][driver_id] = 0
        return list, weight

    def calculate_weight(self, price, rating):
        return (price - self.min_price) / (self.max_price - self.min_price) \
            + 1 - (rating - self.min_rating) / (self.max_rating - self.min_rating)

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
            unit_budget = float(request[0])
            min_rating = float(request[3])
            for ind, driver in enumerate(driver_list):
                driver_id, rating, unit_price = driver
                driver_id = int(driver_id)
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget and not visited[driver_id]:
                    visited[driver_id] = True
                    count = count + 1
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
            unit_budget = float(request[0])
            min_rating = float(request[3])
            temp_list = []
            temp_ind = []
            for ind, driver in enumerate(driver_list):
                driver_id, rating, unit_price = driver
                driver_id = int(driver_id)
                rating = float(rating)
                unit_price = float(unit_price)
                if rating >= min_rating and unit_price <= unit_budget and not visited[driver_id]:
                    temp_list.append(driver_id)
                    temp_ind.append(ind)
            if len(temp_list) >= 1:
                list_len = len(temp_list)
                random_index = random.randint(0,list_len - 1)
                visited[temp_list[random_index]] = True
                count = count + 1
                self.random_matching.append((request_id, temp_ind[random_index]))
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

    def avg_price_rating_for_matching(self, matching):
        sum_rating = 0
        sum_price = 0
        for inr, ind in matching:
            _, rating, unit_price = self.driver_list[ind]
            sum_price += unit_price
            sum_rating += rating
        return sum_price / len(matching), sum_rating / len(matching)
