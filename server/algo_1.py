from search_algos import *
from db_wrapper import DBWrapper
from heapq import heappush, heappop
import copy
from functools import total_ordering
from time import time
from vincenty import vincenty
from node import *


class Algo1(SearchAlgorithm):

    def generateRoutes(self):
        # TODO: account for the fact that...
        # since getStart() != start_node
        # since getEnd() != end_node

        start_node = self.db_wrapper.getClosestPoint(
            str(self.options.getStart()[0]),
            str(self.options.getStart()[1]))
        goal_node = self.db_wrapper.getClosestPoint(
            str(self.options.getEnd()[0]),
            str(self.options.getEnd()[1]))

        # add start point to frontiner
        start_path = Path(None,
                0,
                self.options.getPathType(),
                self.options.getTargetDistance(),
                goal_node,
                0,
                ([start_node], 0))

        self.frontier = [start_path]

        # estabilsh visited nodes set
        last_id = None
        already_searched_from = set()


        print(start_node.node_id)
        print(goal_node.node_id)
        # ----- itterative BFS ------
        count = 0
        while True:
            count += 1

            # no more paths
            if len(self.frontier) == 0:
                print("didn't find solution")
                return

            curr = heappop(self.frontier) # let curr: Path, ignore weight

            # TODO: modernize this
            # popuntil we're starting from somewhere new
            while curr.node_list[-1].node_id in already_searched_from:
                # no more paths
                if len(self.frontier) == 0:
                    print("didn't find solution")
                    return
                curr = heappop(self.frontier)
            already_searched_from.add(curr.node_list[-1].node_id)

            # bad path, skip
            if curr.isInvalid():
                continue

            # not solution, keep searching
            rows = self.db_wrapper.getNHopNeighbours(
                        curr.node_list[-1],
                        self.options.getPathType(),
                        5)

            # insert neighbours into frontier
            print("iter: {}, row_#: {}, front: {}, w: {}, id: {}".format(count, len(rows), len(self.frontier), curr.getWeight(), curr.node_list[-1].node_id ))
            # TODO: don't add all paths to frontier
            for row in rows:
                new_path = Path(
                    curr,
                    curr.pref_path_count,
                    self.options.getPathType(),
                    self.options.getTargetDistance(),
                    goal_node,
                    curr.total_d,
                    row)

                # found sol
                if new_path.isGoal():
                    # TODO: reconstruct route from linked list
                    self.extract_route(new_path)
                    print("found a solution")
                    return
                # push path to frontiner
                heappush(self.frontier, new_path)

    def extract_route(self, path):
        print(path)
        self.route = [n.getLatLonTuple() for n in path.node_list] + self.route
        path = path.prev_path
        while path != None:
            self.route = [n.getLatLonTuple() for n in path.node_list] + self.route
            path = path.prev_path
        # TODO: some points are duplicates...


def mockRow(node_id, path_count):
    return ([mockSimpleNode(node_id)], path_count)

def mockSimpleNode(node_id):
    return SimpleNode(None, node_id, 0.0, 0.0)


@total_ordering
class Path:
    """
>>> p1 = Path(None, 0, "", 10.0, SimpleNode(None, 10, 1.0, 1.0), 0, mockRow(2,1))
>>> assert len(p1.node_list) == 1
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(3, 1))
>>> assert len(p1.node_list) == 2
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(4, 1))
>>> assert len(p1.node_list) == 3
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(10, 1))
>>> assert len(p1.node_list) == 4
>>> assert p1.isInvalid() == False
>>> assert p1.isGoal() == True
>>> back = Path(None, 0, "", 10.0, SimpleNode(None, 10, 1.0, 1.0), 0, mockRow(2,1))
>>> assert not back.isInvalid()
>>> back.addRow(mockRow(1, 1))
>>> assert not back.isInvalid()
>>> back.addRow(mockRow(2, 1))
>>> assert back.isInvalid()
    """

    def __init__(self, prev_path, start_count, path_pref, target_d, goal_node, traveled_d, row):
        self.pref_path_count = start_count
        self.prev_path = prev_path

        self.total_d = traveled_d

        self.node_list = []
        self.backtrack_valid = True

        self.target_d = target_d
        self.pref_path = path_pref

        self.goal_node = goal_node # TODO: make this a path global
        self.addRow(row)


    def addRow(self, row):
        for n in row[0]:
            self.addNode(n)
            if self.isGoal():
                # goal found within n-hops neighbours!
                break
        self.pref_path_count += row[1] # TODO: could overestimate path count if goal in middle of path
        self.backtrackSafeCheck()


    def addNode(self, n):
        if len(self.node_list) != 0:
            self.total_d += self.node_list[-1].getD(n)
        self.node_list.append(n)

    def isGoal(self):
        return len(self.node_list) >= 3 and self.goal_node.node_id == self.node_list[-1].node_id and not self.isInvalid() and self.min_length()

    def min_length(self):
        return self.total_d > (self.target_d / 2)

    def isInvalid(self):
        # TODO: missing what else?
        return not self.backtrack_valid

    def backtrackSafeCheck(self):
        if len(self.node_list) < 3:
            self.backtrac_valid = True
            return
        for i in range(len(self.node_list)-2):
            a = self.node_list[i].node_id
            c = self.node_list[i+2].node_id
            if a == c:
                self.backtrack_valid = False
                return

    def getDistanceDiff(self):
        return abs(self.target_d - self.total_d - self.node_list[-1].getD(self.goal_node))

    def getWeight(self):
        # TODO: what else goes in the tuple
        # TODO: add random variable
        # TODO: 1 - pref_path_count
        return (round(self.getDistanceDiff(), 2), self.pref_path_count)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getWeight() == other.getWeight()

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getWeight() < other.getWeight()

    def __str__(self):
        string = """Path:
        traveled_d: {}
        segment # nodes: {}
        weight: {}
        Good paths: {}
        """.format(self.total_d, len(self.node_list), self.getWeight(), self.pref_path_count)
        return string


if __name__ == "__main__":
    from path_options import *
    from db_wrapper import *
    db = DBWrapper('bolt://localhost:7687', 'neo4j', 'test')
    ops = PathOptions((53.509905, -113.541233),(53.504764, -113.560748), None, 4.0, "algo_1")
    search = Algo1(ops, db)
    search.generateRoutes()
    print(search.getRoutesJson()['path'])
