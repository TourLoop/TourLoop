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

        n = self.db_wrapper.getClosestPoint(
            self.options.getStart()[0], self.options.getStart()[1])

        visited = set(n.node_id)
        frontier = [n]
        heapq.heapify(frontier)
        while n.target_dist_est > 0.1:
            n = heapq.heappop(frontier)
            print("Distance: ", n.path_dist, n.target_dist_est)

            for c in self.db_wrapper.getNeighbours(n):
                if c.node_id not in visited:
                    # modify hueristic
                    #print("h1: ", c.huer)
                    decimals = 2
                    factor = 10 ** decimals
                    c.huer = (math.floor(c.huer * factor) / factor, randint(0,2))
                    #print("h2: ", c.huer)
                    visited.add(c.node_id)
                    heapq.heappush(frontier, c)

        self.distance = n.path_dist

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        self.getElapsedTime()
