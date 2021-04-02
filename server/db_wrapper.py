from neo4j import GraphDatabase, basic_auth
from node import *


class DBWrapper:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(
            uri, auth=basic_auth(username, password))

    def close(self):
        self.driver.close()

    # TOURLOOP FR3 : Closest Node point
    def getClosestPoint(self, lat_string, lon_string):
        """find closest lat long point in db given a lat long string

        >>> d=DBWrapper("bolt://localhost:7687", "neo4j", "test")
        >>> d.getClosestPoint('53.509905', '-113.541233')
        {'lat': 53.5098266, 'lon': -113.5411793}
        """

        with self.driver.session() as session:
            return session.read_transaction(self._getClosestPoint,
                                            lat_string, lon_string)

    @staticmethod
    def _getClosestPoint(tx, lat_string, lon_string):
        closest_point_query = """
        Match (n:Node)
        WHERE distance(n.location, point({latitude:toFloat($lat), longitude:toFloat($lon)})) < 1000
        Return n
        Order by distance(n.location, point({latitude:toFloat($lat), longitude:toFloat($lon)}))
        limit 1
        """
        res = tx.run(closest_point_query, lat=lat_string, lon=lon_string)
        r = res.single()
        return Node(None, r.data()['n']['nodeId'], r.data()['n']['lat'], r.data()['n']['lon'])

    # TOURLOOP FR3 : Closest Node point
    def getClosestPointToPathtype(self, path_string, lat_string, lon_string):
        """find closest lat long point in db given a lat long string

        >>> d=DBWrapper("bolt://localhost:7687", "neo4j", "test")
        >>> d.getClosestPointToPathtype("bike", '53.509905', '-113.541233')
        {'lat': 53.5098266, 'lon': -113.5411793}
        """

        with self.driver.session() as session:
            return session.read_transaction(
                self._getClosestPointToPathtype, path_string, lat_string, lon_string)

    @staticmethod
    def _getClosestPointToPathtype(tx, path_string, lat_string, lon_string):
        closest_point_to_pathtype_query = """
        MATCH (n:Node) -[:Way {pathType:$pathtype}] - (n2:Node)
        WHERE distance(n.location, point({latitude:toFloat($lat), longitude:toFloat($lon)})) < 1000
        Return n
        Order by distance(n.location, point({latitude:toFloat($lat), longitude:toFloat($lon)}))
        limit 1
        """
        res = tx.run(closest_point_to_pathtype_query,
                     pathtype=path_string, lat=lat_string, lon=lon_string)
        r = res.single()
        return Node(None, r.data()['n']['nodeId'], r.data()['n']['lat'], r.data()['n']['lon'])

    def getNeighbours(self, prev_node):
        """returns the node_id of the neighbouring nodes connected by a way

        >>> d=DBWrapper("bolt://localhost:7687", "neo4j", "test")
        >>> d.getNeighbours("2815578994")
        ['2815578992', '2815578985']
        """

        with self.driver.session() as session:
            return session.read_transaction(
                self._getNeighbours, prev_node)

    @staticmethod
    def _getNeighbours(tx, prev_node):
        closest_point_to_pathtype_query = """
        Match(n:Node {nodeId: $id})-[:Way]-(n1:Node)
        Return n1
        """
        res = tx.run(closest_point_to_pathtype_query,
                     id=prev_node.node_id)
        nodes = []
        for r in res:
            nodes.append(Node(prev_node, r.data()['n1']['nodeId'], r.data()[
                         'n1']['lat'], r.data()['n1']['lon']))

        return nodes

    def getPinsExampleRoutes(self):
        pins_query = """
        match (start:Node {id: "2815578994"}) // pick a point on keilor
        match p = (start)-[:Way*15]-(:Node) // get a path
        CALL { // calculate distnace of p
            with p
            UNWIND relationships(p) as w
            with sum(w.dist) as d
            return d
        }
        CALL { // calculate # of bike segments in path
            with p
            UNWIND relationships(p) as w
            with w as W
            where W.pathType = "bike"
            with count(W) as c
            return c
        }
        with *, nodes(p) AS nodes
        with *, relationships(p) as ways
        return c, d, nodes, ways
        order by d
        """
        routes = []
        with self.driver.session() as session:
            res = session.run(pins_query)
            # res has many rows
            # res.data() returns a list of these rows
            # each row has keys : ['c', 'd', 'nodes', 'ways']

            # one route is a list of node json objects
            routes = [row['nodes'] for row in res]
        return routes


def record_to_lat_lon_dict(record):
    # TODO: handle record keys len!=1 and name != 'n'
    return {'lat': record.data()['n']['lat'], 'lon': record.data()['n']['lon']}
