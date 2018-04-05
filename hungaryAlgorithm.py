M=[]
class DFS_hungary():

    def __init__(self, nx, ny, edge, cx, cy, visited):
        self.nx, self.ny=nx, ny
        self.edge = edge
        self.cx, self.cy=cx,cy
        self.visited=visited

    def max_match(self):
        res=0
        for idx,request in enumerate(self.nx):
            if self.cx[idx]==-1:
                for driver in self.ny:
                    self.visited[driver[0]]=0
                res+=self.path(idx)
        return res

    def path(self, request_num):
        for driver in self.ny:
            driver_num = int(driver[0])
            if self.edge[request_num][driver_num] and (not self.visited[driver_num]):
                self.visited[driver_num]=1
                if self.cy[driver_num]==-1:
                    self.cx[request_num] = driver_num
                    self.cy[driver_num] = request_num
                    M.append((request_num,driver_num))
                    return 1
                else:
                    #M.remove((self.cy[driver_num], driver_num))
                    if self.path(self.cy[driver_num]):
                        self.cx[request_num] = driver_num
                        self.cy[driver_num] = request_num
                        M.append((request_num, driver_num))
                        return 1
        return 0

    def get_matching(self):
        matching = []
        driver_id_dict = {int(driver[0]): i for i, driver in enumerate(self.ny)}
        for idx, request in enumerate(self.nx):
            if self.cx[idx] >= 0:
                matching.append((idx, driver_id_dict[self.cx[idx]]))
        return matching
