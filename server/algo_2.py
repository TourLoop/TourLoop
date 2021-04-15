from search_algos import *
from time import time
from node import Node
import math

MAX_FRONTIER = 20
MAX_DIST_FROM_START_END = 0.1

# TOURLOOP FR1 : generate loops
# TOURLOOP FR2 : generate point to point routes
class Algo2(SearchAlgorithm):

    def generateRoutes(self):
        self.start_time = time()
        print(self.options.__dict__)

        Node.target = self.options.getEnd()
        Node.target_distance = self.options.getTargetDistance()
        Node.target_path_type = self.options.getPathType()

        n = self.db_wrapper.getClosestPoint(
            self.options.getStart()[0], self.options.getStart()[1])

        frontier = [n]
        # TOURLOOP FR7 : backtracking prevention
        visited = set([n.node_id])
        while n.target_dist_est > MAX_DIST_FROM_START_END or n.path_dist < (Node.target_distance / 2):
            # TOURLOOP FR5 : no route error
            if n.path_dist > 2 * Node.target_distance:
                self.err_message = "Could not find a route given the input parameters."
                return

            # TOURLOOP FR5 : no route error
            if not frontier:
                self.err_message = "Could not find a path between start and end location."
                return

            n = frontier.pop(0)

            print("Huer: ", n.huer, "ID: ", n.node_id, "Dist: ", n.path_dist, "Remaining Dist: ", n.target_dist_est, "Front: ", len(frontier))

            for c in self.db_wrapper.getNeighbours(n):
                if n.prev_node == None or c.node_id != n.prev_node.node_id:
                    if c.node_id not in visited:

                        percent_good_paths = max(math.floor(1 - (c.pref_count / c.count)), 0.5)
                        c.huer *= percent_good_paths

                        frontier.append(c)
                        visited.add(c.node_id)

            frontier.sort()
            while len(frontier) > MAX_FRONTIER:
                p = frontier.pop()

        self.distance = n.path_dist

        while n.prev_node != None:
            self.route.append((n.lat, n.lon))
            n = n.prev_node
        self.route.append((n.lat, n.lon))

        self.getElapsedTime()
