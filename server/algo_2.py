from search_algos import *
from time import time
from collections import deque
from vincenty import vincenty


class Algo2(SearchAlgorithm):
    def generateRoutes(self):
        self.start_time = time()

        self.options.setOptions((53.626489, -113.321961),
                                (53.604000, -113.314345), "bike", 5.0,  "ALGO2")

        s = self.db_wrapper.getClosestPoint(self.options.getStart()[
            0], self.options.getStart()[1])
        frontier = deque([s])
        visited = set(s.node_id)
        d = float('inf')
        while d > 0.5:
            n = frontier.popleft()
            d = vincenty((n.lat, n.lon), self.options.getEnd())
            print("Distance: ", d)

            for c in self.db_wrapper.getNeighbours(n):
                if c.node_id not in visited:
                    visited.add(c.node_id)
                    frontier.append(c)

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        self.getElapsedTime()
