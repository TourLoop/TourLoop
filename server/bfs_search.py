from search_algos import *
from db_wrapper import DBWrapper
from heapq import heappush, heappop
import copy
from functools import total_ordering


# this is a fake search algorithm which demos how to return routes
class BFS(SearchAlgorithm):

    def generateRoutes(self):
        # TODO: account for the fact that...
        # since getStart() != start_node
        # since getEnd() != end_node

        goal_node = self.db_wrapper.getClosestPoint(\
            str(self.options.getStart()[0]),\
            str(self.options.getStart()[1]))
        start_node = self.db_wrapper.getClosestPoint(\
            str(self.options.getEnd()[0]),\
            str(self.options.getEnd()[1]))

        start_row = mockRow(start_node['id'], 0, 0)

        # add start point to frontiner
        mock_row = start_row
        self.frontier = [Path(mock_row,\
                self.options.getPathType(),\
                self.options.getTargetDistance(),\
                goal_node['id'])]


        print(goal_node['id'])
        print(start_node['id'])
        # ----- itterative BFS ------
        count = 0
        while True:
            count += 1

            # no more paths
            if len(self.frontier) == 0:
                print("didn't find solution")
                return

            curr = heappop(self.frontier) # let curr: Path, ignore weight

            # bad path, skip
            if curr.isInvalid():
                continue

            # not solution, keep searching
            rows = self.db_wrapper.getNeighbours(
                        curr.getCurrentId(),
                        curr.getRemainingD(),
                        None)

            # insert neighbours into frontier
            print("iter: {}, new_nodes: {}".format(count, len(rows)))
            for row in rows:
                #print(row)
                new_path = copy.deepcopy(curr)
                new_path.addRow(row)
                # TODO: <bug> if multiple goals are in neighs...
                # found sol
                if new_path.isGoal():
                    self.routes.append(new_path.node_list)
                    print("found a solution")
                    return
                # push path to frontiner
                heappush(self.frontier, new_path)



def mockRow(node_id, dist, path_count):
    return {'nodes':[{'id':node_id}], 'c':path_count, 'path_d':dist}


@total_ordering
class Path:
    """
>>> p1 = Path(mockRow(1, 0, 0), "", 10.0, 10)
>>> p1.addRow(mockRow(2, 0.1, 1))
>>> assert len(p1.node_list) == 2
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(3, 0.1, 1))
>>> assert len(p1.node_list) == 3
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(4, 0.1, 2))
>>> assert len(p1.node_list) == 4
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(10, 0.1, 1))
>>> assert len(p1.node_list) == 5
>>> assert p1.isInvalid() == False
>>> assert p1.isGoal() == True
>>> back = Path(mockRow(1, 0, 0), "", 10, 10)
>>> assert not back.isInvalid()
>>> back.addRow(mockRow(2, 0.1, 1))
>>> assert not back.isInvalid()
>>> back.addRow(mockRow(1, 0.1, 1))
>>> assert back.isInvalid()
    """
    def __init__(self, start_row, path_pref, max_d, goal_id):
        self.node_list = []
        self.pref_path_count = 0
        self.pref_path = path_pref
        self.total_d = 0
        self.max_d = max_d
        self.over_d = False
        self.backtrack_valid = True
        self.goal_id = goal_id
        self.addRow(start_row)

    def addRow(self, row):
        old_index = len(self.node_list)
        for n in row['nodes']:
            # TODO: <bug> solution may no longer be at end
            self.node_list.append(n)
            if n['id'] == self.goal_id:
                # goal found within n-hops neighbours
                # TODO: <bug> rollback diatance and pathcount
                break
        self.updateD(row)
        self.updatePathCount(row)
        self.backtrackSafeCheck(old_index)

    def updateD(self, row):
        self.total_d += row['path_d']
        if self.total_d >= self.max_d:
            self.over_d = True

    def updatePathCount(self, row):
        self.pref_path_count += row['c']

    def isGoal(self):
        return len(self.node_list) >= 3 and self.goal_id == self.node_list[-1]['id'] and not self.isInvalid()

    def isInvalid(self):
        return self.over_d or not self.backtrack_valid

    def backtrackSafeCheck(self, start_index):
        if len(self.node_list) < 3:
            self.backtrac_valid = True
            return
        for i in range(start_index, len(self.node_list)):
            a = self.node_list[i]['id']
            c = self.node_list[i-2]['id']
            if a == c:
                self.backtrack_valid = False
                return

    def getCurrentId(self):
        return self.node_list[-1]['id']

    def getRemainingD(self):
        return self.max_d - self.total_d

    def getWeight(self):
        return self.total_d

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getWeight() == other.getWeight()

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.getWeight() < other.getWeight()


if __name__ == "__main__":
    from path_options import *
    from db_wrapper import *
    db = DBWrapper('bolt://localhost:7687', 'neo4j', 'test')
    ops = PathOptions((53.509905, -113.541233),(53.508098, -113.545846), None, 4.0, "")
    search = BFS(ops, db)
    search.generateRoutes()
    print(search.getElapsedTime())
