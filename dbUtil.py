import sqlite3
import numpy as np

class dbUtil():
    def __init__(self):
        db_conn = sqlite3.connect('data.db')
        self.db_cursor = db_conn.cursor()

        rs_db_conn = sqlite3.connect('rs.db')
        self.rs_db = rs_db_conn.cursor()


    def get_driver_list_by_time(self,start_time,end_time):
        excuteSQL = "select * from drivers where timestamp between ? and ?"
        query_result = self.db_cursor.excute(excuteSQL,(start_time,end_time))
        return [line[0] for line in query_result]


    def get_request_list_by_time(self,start_time,end_time):
        excuteSQL = "select * from request where timestamp between ? and ?"
        query_result = self.db_cursor.excute(excuteSQL,(start_time,end_time))
        return [line[0] for line in query_result]