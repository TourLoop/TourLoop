from time import time
import polyline

def node_list_to_polyline(node_list, accuracy=6):
    return polyline.encode([(float(n['lat']), float(n['lon'])) for n in node_list], accuracy)

def routes_to_json(routes):
    return {"paths": [node_list_to_polyline(r) for r in routes] }

class SearchAlgorithm:

    def __init__(self, options, db):
        self.start_time = time()
        self.elapsed_time = None
        self.options = options
        self.frontier = []
        self.db_wrapper = db

    def getElapsedTime(self):
        if self.elapsed_time == None:
            self.elapsed_time = time() - self.start_time
        return self.elapsed_time

    # override in sub-classes
    def generateRoutes(self):
        routes = []
        return routes_to_json(routes)

