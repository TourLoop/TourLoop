from search_algos import *
from time import time
from node import Node
import heapq
import math
from random import randint
from algo_test_suite import *

# TOURLOOP FR1 : generate loops
# TOURLOOP FR2 : generate point to point
# TOURLOOP FR8 : 1/3 route generation algorithms
class Algo3(SearchAlgorithm):
    def generateRoutes(self):
        self.start_time = time()

        Node.target = self.options.getEnd()
        Node.target_distance = self.options.getTargetDistance()
        Node.target_path_type = self.options.getPathType()

        n = self.db_wrapper.getClosestPoint(
            self.options.getStart()[0], self.options.getStart()[1])

        # TOURLOOP FR7 : backtracking prevention
        visited = set(n.node_id)
        frontier = [n]
        heapq.heapify(frontier)
        while n.target_dist_est > 0.1 or n.path_dist < (Node.target_distance / 2):
            # TOURLOOP FR5 : no route error
            if n.path_dist > 2* Node.target_distance:
                self.err_message = "Could not find a route given the input paramaters"
                return
            # TOURLOOP FR5 : no route error
            if len(frontier) == 0:
                self.err_message = "Could not find a route given the input paramaters"
                return
            n = heapq.heappop(frontier)

            for c in self.db_wrapper.getNeighbours(n):
                # TOURLOOP FR7 : backtracking prevention
                if c.node_id not in visited:
                    # modify hueristic
                    #print("h1: ", c.huer)
                    decimals = 2
                    factor = 10 ** decimals
                    # round for more matching
                    percent_good_paths = math.floor(100 - 100 * (c.pref_count / c.count))
                    # TOURLOOP FR9 : route generation randomess
                    # TOURLOOP FR10 : path preference
                    c.huer = (math.floor(c.huer * factor) / factor, percent_good_paths, randint(0,9))
                    #print("h2: ", c.huer)
                    visited.add(c.node_id)
                    heapq.heappush(frontier, c)

        self.distance = n.path_dist

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        # print("Elapsed time: ", self.getElapsedTime())


def smoke_tests():
    from path_options import PathOptions
    from db_wrapper import DBWrapper
    db = DBWrapper('bolt://localhost:7687', 'neo4j', 'test')

    # doesn't have solution...?
    ops = PathOptions((53.515521, -113.513749),(53.515521, -113.513749), "paved", 2, "algo_3")
    search = Algo3(ops, db)
    search.generateRoutes()
    print(search.getRoutesJson()['path'])
    assert len(search.getRoutesJson()['path']) > 0, "didn't find solution"

    # loop example
    ops = PathOptions((53.509905, -113.541233),(53.504764, -113.560748), "bike", 4.0, "algo_1")
    search = Algo3(ops, db)
    search.generateRoutes()
    print(search.getRoutesJson()['path'])
    assert len(search.getRoutesJson()['path']) > 0, "didn't find solution"

    # this example should produce different paths randomly
    ops = PathOptions((53.510339, -113.536677),(53.510339, -113.536677), "paved", 4.5, "algo_3") # loop example
    search = Algo3(ops, db)
    search.generateRoutes()
    print(search.getRoutesJson()['path'])
    assert len(search.getRoutesJson()['path']) > 0, "didn't find solution"


# Algo 3 test suite
if __name__ == "__main__":
    smoke_tests()
