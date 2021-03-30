from search_algos import *
from db_wrapper import DBWrapper


# this is a fake search algorithm which demos how to return routes
class ReturnPins(SearchAlgorithm):

    def generateRoutes(self):
        self.routes = self.db_wrapper.getPinsExampleRoutes()
        return

if __name__ == "__main__":
    search = ReturnPins(None, DBWrapper())
    search.generateRoutes()
    res = search.getRoutesJson()
    print(len(res['paths']))
    print(search.getElapsedTime())
    #print(res)
