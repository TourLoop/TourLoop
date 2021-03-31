from search_algos import *
from db_wrapper import DBWrapper
from heapq import heappush, heappop
import copy


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

        start_row = {'node': start_node, 'p_type': 'fake', 'dist': 0.0}

        # add start point to frontiner
        mock_row = start_row
        self.frontier = [(0,Path(mock_row,\
                self.options.getPathType(),\
                self.options.getTargetDistance(),\
                goal_node['id']))]

        # ----- itterative BFS ------
        count = 0
        while True:
            count += 1

            # no more paths
            if len(self.frontier) == 0:
                print("didn't find solution")
                return

            _, curr = heappop(self.frontier) # let curr: Path, ignore weight

            # bad path, skip
            if curr.isInvalid():
                continue

            # not solution, keep searching
            rows = self.db_wrapper.getNeighbours(\
                        curr.getCurrentId(),\
                        curr.getRemainingD())

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
                weight = new_path.getWeight()
                # TODO: <bug> can't break when there are equal weights
                heappush(self.frontier, (weight,new_path))



def mockRow(node_id, dist, path_type="bike"):
    return {'node':{'id':node_id}, 'p_type':path_type, 'dist':dist}

class Path:
    """
>>> p1 = Path(mockRow(1, 0), "", 10.0, 10)
>>> p1.addRow(mockRow(2, 0.1))
>>> assert len(p1.node_list) == 2
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(3, 0.1))
>>> assert len(p1.node_list) == 3
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(4, 0.1))
>>> assert len(p1.node_list) == 4
>>> assert p1.isGoal() == False
>>> assert p1.isInvalid() == False
>>> p1.addRow(mockRow(10, 0.1))
>>> assert len(p1.node_list) == 5
>>> assert p1.isInvalid() == False
>>> assert p1.isGoal() == True
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
        self.node_list.append(row['node'])
        self.updateD(row)
        self.updatePathCount(row)
        self.backtrackSafeCheck()

    def updateD(self, row):
        self.total_d += row['dist']
        if self.total_d >= self.max_d:
            self.over_d = True

    def updatePathCount(self, row):
        if row['p_type'] == self.pref_path:
            self.pref_path_count += 1

    def isGoal(self):
        return len(self.node_list) >= 3 and self.goal_id == self.node_list[-1]['id'] and not self.isInvalid()

    def isInvalid(self):
        return self.over_d or not self.backtrack_valid

    def backtrackSafeCheck(self):
        if len(self.node_list) < 3:
            self.backtrack_valid = True
            return
        a = self.node_list[-1]['id']
        b = self.node_list[-2]['id']
        c = self.node_list[-3]['id']
        self.backtrack_valid = a != c

    def getCurrentId(self):
        return self.node_list[-1]['id']

    def getRemainingD(self):
        return self.max_d - self.total_d

    def getWeight(self):
        return self.total_d


if __name__ == "__main__":
    from path_options import *
    from db_wrapper import *
    db = DBWrapper('bolt://localhost:7687', 'neo4j', 'test')
    ops = PathOptions((53.509905, -113.541233),(53.509905, -113.541233), None, 4.0, "")
    search = BFS(ops, db)
    search.generateRoutes()
    print(search.getElapsedTime())
