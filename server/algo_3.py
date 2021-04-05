from search_algos import *
from time import time
from node import Node
import heapq
import math
from random import randint


class Algo3(SearchAlgorithm):
    def generateRoutes(self):
        self.start_time = time()
        print(self.options.__dict__)

        Node.target = self.options.getEnd()
        Node.target_distance = self.options.getTargetDistance()
        Node.target_path_type = self.options.getPathType()

        n = self.db_wrapper.getClosestPoint(
            self.options.getStart()[0], self.options.getStart()[1])

        visited = set(n.node_id)
        frontier = [n]
        heapq.heapify(frontier)
        while n.target_dist_est > 0.05 or n.path_dist < (Node.target_distance / 2):
            n = heapq.heappop(frontier)
            print("Distance: ", n.path_dist, n.target_dist_est)

            for c in self.db_wrapper.getNeighbours(n):
                if c.node_id not in visited:
                    # modify hueristic
                    #print("h1: ", c.huer)
                    decimals = 2
                    factor = 10 ** decimals
                    # round for more matching
                    percent_good_paths = math.floor(100 - 100 * (c.pref_count / c.count))
                    c.huer = (math.floor(c.huer * factor) / factor, percent_good_paths, randint(0,9))
                    #print("h2: ", c.huer)
                    visited.add(c.node_id)
                    heapq.heappush(frontier, c)

        self.distance = n.path_dist

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        print("Elapsed time: ", self.getElapsedTime())





if __name__ == "__main__":
    from path_options import *
    from db_wrapper import *
    db = DBWrapper('bolt://localhost:7687', 'neo4j', 'test')
    ops = PathOptions((53.509905, -113.541233),(53.504764, -113.560748), "bike", 4.0, "algo_1")
    search = Algo3(ops, db)
    search.generateRoutes()
    print(search.getRoutesJson()['path'])
    assert len(search.getRoutesJson()['path']) > 0, "didn't find solution"
    ops = PathOptions((53.510339, -113.536677),(53.510339, -113.536677), "paved", 4.5, "algo_3") # loop example
    search = Algo3(ops, db)
    search.generateRoutes()
    print(search.getRoutesJson()['path'])
    assert len(search.getRoutesJson()['path']) > 0, "didn't find solution"
