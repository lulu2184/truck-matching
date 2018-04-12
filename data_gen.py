import sqlite3
import numpy as np

class DataGen:
    def __init__(self, db_cursor, rs_db_cursor):
        self.db_cursor = db_cursor
        self.rs_db = rs_db_cursor

        self.rs_db.execute("drop table if exists driver_data")
        self.rs_db.execute("drop table if exists request")
        self.rs_db.execute("create table driver_data (driver_id integer, timestamp integer, lat real, lon real,"
                          + " occupied integer)")
        # request data
        self.rs_db.execute("create table request (unit_budget real, weight integer, start_time integer, end_time integer,"
                           + "min_rating real, start_lat real, start_lon real, dst_lat real, dst_lon real)")
        self.request_cols = ['unit_budget', 'weight','start_time', 'end_time', 'min_rating', 'start_lat', 'start_lon',
                             'dst_lat', 'dst_lon']

    @staticmethod
    def gen_rating():
        rating = np.random.normal(4, 0.5, 1)[0]
        rating = min(5, max(2, rating))
        return float(rating)

    @staticmethod
    def gen_unit_price():
        return max(1, np.random.normal(10, 0.3))


    @staticmethod
    def gen_weight():
        return np.random.uniform(0,14);

    def has_driver(self, driver_id):
        query_result = self.db_cursor.execute("select * from drivers where driver_id = " + str(driver_id))
        for _ in query_result:
            return True
        return False

    def insert_driver(self, driver_id,lat,lon):
        rating = self.gen_rating()
        unit_price = self.gen_unit_price()
        weight = self.gen_weight()
        self.db_cursor.execute("insert into drivers values (?,?,?,?,?,?)", (driver_id, rating, unit_price, weight, lat, lon))

    def get_driver_list(self):
        query_result = self.db_cursor.execute("select * from drivers")
        return [line[0] for line in query_result]

    def get_records_for_driver(self, driver_id):
        return self.db_cursor.execute(
            "select * from data where driver_id = {} order by timestamp".format(driver_id))

    def get_rating_price(self, driver_id):
        query_result = self.db_cursor.execute("select * from drivers where driver_id = " + str(driver_id))
        for row in query_result:
            return row[1], row[2]
        return None, None

    def process_one_driver(self, driver_id, records):
        print('processing driver ' + str(driver_id))
        pending_request = None
        for line in records:
            driver_id, timestamp, lat, lon, occupied = line
            lat = float(lat)
            lon = float(lon)
            occupied = int(occupied)
            timestamp = int(timestamp)
            if not occupied:
                self.rs_db.execute('insert into driver_data values({})'.format(','.join([str(v) for v in line])))
                if pending_request:
                    pending_request['dst_lat'] = lat
                    pending_request['dst_lon'] = lon
                    pending_request['end_time'] = timestamp
                    self.rs_db.execute("insert into request values ({})".format(','.join(['?'] * len(self.request_cols))),
                                       tuple(str(pending_request[field]) for field in self.request_cols))
                    pending_request = None

            else:
                if not pending_request:
                    pending_request = {'start_time': timestamp, 'min_rating': self.gen_rating(),
                                       'start_lat': lat, 'start_lon': lon,
                                       'unit_budget': self.gen_unit_price(),'weight':self.gen_weight()}

    def load_data_to_db(self):
        db_cursor.execute('drop table if exists drivers')
        db_cursor.execute('drop table if exists data')
        # driver table here
        db_cursor.execute("CREATE TABLE drivers (driver_id integer, rating real, unit_price real, capacity integer," +
                          "lat real, lon real)")
        db_cursor.execute("CREATE TABLE data (driver_id integer, timestamp integer, lat real, lon real,"
                          + " occupied integer)")

        f = open("20151112.txt", "r")
        counter = 0
        id = 0
        for line in f:
            if counter == 4000000:
                print('finishing loading data...')
                break
            counter += 1
            if np.random.randint(10) > 0:
                continue
            # if counter > 20000:
            #     break
            # Data format:
            # taxi id, time stamp, lat, lon, orientation, speed, flag_occupied, flag operation
            taxi_id, timestamp, lat, lon, ori, speed, occupied, _ = line.split(',')
            taxi_id = int(taxi_id)
            timestamp = int(timestamp)
            lat = float(lat)
            lon = float(lon)
            occupied = bool(int(occupied))
            if not self.has_driver(taxi_id):
                self.insert_driver(taxi_id,lat,lon)

            db_cursor.execute("INSERT INTO data VALUES (?,?,?,?,?)", (taxi_id, timestamp, lat, lon, occupied))

    def gen_data_from_db(self):
        drivers = self.get_driver_list()
        for driver in drivers:
            records = self.get_records_for_driver(driver)
            self.process_one_driver(driver, records)

if __name__ == "__main__":
    db_conn = sqlite3.connect('data.db')
    db_cursor = db_conn.cursor()

    rs_db_conn = sqlite3.connect('rs.db')
    rs_db_cursor = rs_db_conn.cursor()

    gen = DataGen(db_cursor, rs_db_cursor)
    gen.load_data_to_db()
    gen.gen_data_from_db()

    db_conn.commit()
    rs_db_conn.commit()
    db_conn.close()
    rs_db_conn.close()

