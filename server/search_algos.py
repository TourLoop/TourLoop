from time import time
from path_options import PathOptions
import polyline


# TOURLOOP FR1: loop generation
# TOURLOOP FR2: point to point routes
class SearchAlgorithm:

    def __init__(self, options, db):
        self.start_time = None
        self.elapsed_time = None
        self.options = options
        self.distance = None
        self.percent_path_type = None
        self.frontier = []
        self.db_wrapper = db
        self.route = []
        self.err_message = None

    def getElapsedTime(self):
        if self.elapsed_time == None:
            self.elapsed_time = time() - self.start_time
        return self.elapsed_time

    # override in sub-classes
    def generateRoutes(self):
        # add node_list's to self.route
        return

    def getRoutesJson(self):
        if self.err_message != None:
            return {"errMessage": self.err_message}

        return {"path": polyline.encode(self.route, 6), "time": self.elapsed_time, "distance": self.distance, "percentpathtype": self.percent_path_type, "algorithm": self.options.getAlgorithmType()}
