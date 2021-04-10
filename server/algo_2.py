from search_algos import *
from time import time
from node import Node
from vincenty import vincenty

MAX_FRONTIER = 7
MAX_DIST_FROM_START_END = 0.5

class Algo2(SearchAlgorithm):

    def generateRoutes(self):
        self.start_time = time()
        print(self.options.__dict__)

        Node.target = self.options.getEnd()
        Node.target_distance = self.options.getTargetDistance()
        Node.target_path_type = self.options.getPathType()

        n = self.db_wrapper.getClosestPoint(
            self.options.getStart()[0], self.options.getStart()[1])

        if n == None:
            self.err_message = "Could not find path within 1 km of your start location."
            return

        n_closest_end = self.db_wrapper.getClosestPoint(
            self.options.getEnd()[0], self.options.getEnd()[1])

        if n_closest_end == None:
            self.err_message = "Could not find path within 1 km of your end location."
            return

        frontier = [n]
        frontier_ids = set([n.node_id])
        while n.path_dist < Node.target_distance * 2 and (n.target_dist_est > MAX_DIST_FROM_START_END or n.path_dist < (Node.target_distance / 2)):
            if not frontier:
                self.err_message = "Could not find a path between start and end location."

            n = frontier.pop(0)
            frontier_ids.remove(n.node_id)


            for c in self.db_wrapper.getNeighbours(n):
                if n.prev_node == None or c.node_id != n.prev_node.node_id:
                    if c.node_id not in frontier_ids:
                        frontier.append(c)
                        frontier_ids.add(c.node_id)

            frontier.sort()
            while len(frontier) > MAX_FRONTIER:
                p = frontier.pop()
                frontier_ids.remove(p.node_id)

        self.distance = n.path_dist

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        self.getElapsedTime()
