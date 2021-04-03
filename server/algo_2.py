from search_algos import *
from time import time
from node import Node
import heapq


class Algo2(SearchAlgorithm):
    def generateRoutes(self):
        self.start_time = time()

        self.options.setOptions((53.626489, -113.321961),
                                (53.604000, -113.314345), "bike", 10.0,  "ALGO2")

        Node.target = self.options.getEnd()
        Node.target_distance = self.options.getTargetDistance()

        n = self.db_wrapper.getClosestPoint(self.options.getStart()[
            0], self.options.getStart()[1])

        visited = set(n.node_id)
        frontier = [n]
        heapq.heapify(frontier)
        while n.target_dist_est > 0.1:
            n = heapq.heappop(frontier)
            # print("Distance: ", n.path_dist, n.target_dist_est)

            for c in self.db_wrapper.getNeighbours(n):
                if c.node_id not in visited:
                    visited.add(c.node_id)
                    heapq.heappush(frontier, c)

        self.distance = n.path_dist

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        self.getElapsedTime()
