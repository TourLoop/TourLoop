from search_algos import *
from algo_1 import *
from algo_2 import *
from algo_3 import *
from path_options import PathOptions
from db_wrapper import DBWrapper
from random import *

k_point = (53.507640, -113.546640)
fav_belgravia_point = (53.510339, -113.536677)


def assert_no_error(algo):
    assert algo.err_message == None, "Error finding route for " + type(algo).__name__

def assert_has_route_polyline(algo):
    assert len(algo.getRoutesJson()["path"]) > 0

def get_db():
    return DBWrapper('bolt://localhost:7687', 'neo4j', 'test')

def search_test(algo_class, ops):
    search = algo_class(ops, get_db())
    search.generateRoutes()
    assert_no_error(search)
    assert_has_route_polyline(search)
    return search

def bel_to_k_test(algo_class):
    ops = PathOptions(fav_belgravia_point, k_point, "paved", 2.0, "algo_x") # loop example
    search_test(algo_class, ops)

def bel_loop_test(algo_class):
    ops = PathOptions(fav_belgravia_point, fav_belgravia_point, "paved", 4.5, "algo_x") # loop example
    search_test(algo_class, ops)


def paths_are_random_test():
    """ test FR9
    >>> paths_are_random_test()
    """
    ops = PathOptions(fav_belgravia_point, fav_belgravia_point, "paved", 4.5, "algo_3") # loop example
    searches = [Algo3(ops, get_db()), Algo3(ops, get_db()),Algo3(ops, get_db()),Algo3(ops, get_db()),Algo3(ops, get_db())]
    # all find paths
    for s in searches:
        s.generateRoutes()
        assert_no_error(s)
        assert_has_route_polyline(s)

    # assert at least 2 differnt routes generated
    assert 1 < len({ s.getRoutesJson()['path'] for s in searches})

def loop_and_p2p_all_test():
    """ Tests FR1, FR2, and FR3
    >>> loop_and_p2p_all_test()
    """
    bel_to_k_test(Algo1)
    bel_loop_test(Algo1)
    bel_to_k_test(Algo2)
    bel_loop_test(Algo3)
    bel_to_k_test(Algo3)
    bel_loop_test(Algo1)

def path_pref_has_impact_test(algo_class):
    """ test FR10
    >>> path_pref_has_impact_test(Algo3)
    >>> path_pref_has_impact_test(Algo1)
    >>> path_pref_has_impact_test(Algo2)
    """
    ops = [PathOptions(fav_belgravia_point, fav_belgravia_point, p_type, 4.5, "algo_x")  for p_type in ["bike", "paved", "dirt"]]
    searches = [search_test(algo_class, op) for op in ops]
    # assert different solutions
    assert 1 < len({ s.getRoutesJson()['path'] for s in searches})

def random_edmonton_point():
    top =  53.6482
    bottom =  53.3971
    right =  -113.3161
    left =  -113.7155

    scale = lambda L, U: (U - L) * random() + L
    lat = scale(bottom, top)
    lon = scale(left, right)

    assert bottom <= lat and lat <= top, "Point out of Edmonton, you did your math wrong"
    assert left <= lon and lon <= right, "Point out of Edmonton, you did your math wrong"

    return (lat, lon)


def cant_find_closest(point):
    return None == get_db().getClosestPoint(str(point[0]), str(point[1]))

def random_params():
    # generate solveable under 5km paramaters
    target_d = random() * 5
    p1 = random_edmonton_point()
    p2 = random_edmonton_point()
    while vincenty(p1, p2) > target_d or cant_find_closest(p1) or cant_find_closest(p2):
        target_d = random() * 5
        p1 = random_edmonton_point()
        p2 = random_edmonton_point()

    ops = PathOptions(p1, p2, choice(['dirt', 'bike', 'paved']), target_d, "algo_x")
    return ops


def random_param_test(algo_class, n=1):
    """
    >>> random_param_test(Algo1, 5)
    >>> random_param_test(Algo2, 5)
    >>> random_param_test(Algo3, 5)
    """
    for i in range(n):
        #print("Random test #" + str(i+1) + "/" + str(n))
        search_test(algo_class, random_params())
        #print("passed")

