from search_algos import *
from db_wrapper import DBWrapper


# this is a fake search algorithm which demos how to return routes
class ReturnPins(SearchAlgorithm):

    def generateRoutes(self):
        routes = self.db_wrapper.getPinsExampleRoutes()
        return routes_to_json(routes)


if __name__ == "__main__":
    search = ReturnPins(None, DBWrapper())
    res = search.generateRoutes()
    print(search.getElapsedTime())
    #print(res)
