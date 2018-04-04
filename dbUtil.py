import sqlite3
import numpy as np

class dbUtil():
    def __init__(self):
        db_conn = sqlite3.connect('data.db')
        self.db_cursor = db_conn.cursor()

        rs_db_conn = sqlite3.connect('rs.db')
        self.rs_db = rs_db_conn.cursor()


    def get_driver_list_by_time(self,start_time,end_time):
        excuteSQL = "select * from drivers limit 500"
        query_result = self.db_cursor.execute(excuteSQL)
        return query_result.fetchall()


    def get_request_list_by_time(self,start_time,end_time):
        excuteSQL = "select * from request limit 500"
        query_result = self.rs_db.execute(excuteSQL)
        return query_result.fetchall()


    def get_limited_driver_list_by_time(self,start_time,end_time,limit):
        excuteSQL = "select * from drivers limit " + str(limit)
        query_result = self.db_cursor.execute(excuteSQL)
        return query_result.fetchall()


    def get_limited_request_list_by_time(self,start_time,end_time,limit):
        excuteSQL = "select * from request limit " + str(limit)
        query_result = self.rs_db.execute(excuteSQL)
        return query_result.fetchall()