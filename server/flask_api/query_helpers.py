from neo4j import GraphDatabase, basic_auth


closest_point_query = """
MATCH (n:Node)
WITH n, distance(point({latitude:toFloat('$lat'), longitude:toFloat('$lon')}), n.location) AS d
ORDER BY d
  LIMIT 1
RETURN n
"""

closest_point_to_pathtype_query = """
MATCH (n:Node) -[:Way {pathType:$pathtype}] - (n2:Node)
WITH n, distance(point({latitude:toFloat('$lat'), longitude:toFloat('$lon')}), n.location )AS d
ORDER BY d
  LIMIT 1
RETURN n
"""

def get_neo4j_driver():
    return GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "test"))


def record_to_lat_lon_dict(record):
    # TODO: handle record keys len!=1 and name != 'n'
    return {'lat':record.data()['n']['lat'], 'lon': record.data()['n']['lon']}


# TOURLOOP FR3 : Closest Node point
def closest_point(session, lat_string, lon_string):
    """find closest lat long point in db given a lat long string
    >>> closest_point(get_neo4j_driver().session(), '53.509905', '-113.541233')
    {'lat': 53.5714699, 'lon': -113.6278968}
    """
    #print("finding closest point...")
    res = session.run(closest_point_query, lat=lat_string, lon=lon_string)
    record = res.single()
    return record_to_lat_lon_dict(record)

# TOURLOOP FR3 : Closest Node point
def closest_point_to_pathtype(session, pathtype, lat_string, lon_string):
    # TODO: pass docstring test
    """find closest lat long point in db given a lat long string
    >>> closest_point_to_pathtype(get_neo4j_driver().session(), "bike", '53.509905', '-113.541233')
    {'lat': 53.5098266, 'lon': -113.5411793}
    """
    #print("finding closest point...")
    res = session.run(closest_point_to_pathtype_query, pathtype=pathtype, lat=lat_string, lon=lon_string)
    record = res.single()
    return record_to_lat_lon_dict(record)
