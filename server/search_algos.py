from time import time
from path_options import PathOptions
import polyline


def node_list_to_polyline(node_list, accuracy=6):
    return polyline.encode([(float(n['lat']), float(n['lon'])) for n in node_list], accuracy)


class SearchAlgorithm:

    def __init__(self, options, db):
        self.start_time = None
        self.elapsed_time = None
        self.options = PathOptions()
        self.frontier = []
        self.db_wrapper = db
        self.route = []

    def getElapsedTime(self):
        if self.elapsed_time == None:
            self.elapsed_time = time() - self.start_time
        return self.elapsed_time

    # override in sub-classes
    def generateRoutes(self):
        # add node_list's to self.route
        return

    def getRoutesJson(self):
        return {"path": polyline.encode(self.route, 6), "time": self.elapsed_time}
