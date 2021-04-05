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
        >>> n = d.getClosestPoint('53.509905', '-113.541233')
        >>> n == Node(None, '2815578994', '53.5098266', '-113.5411793')
        True
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
        >>> n = d.getClosestPointToPathtype("bike", '53.509905', '-113.541233')
        >>> n == Node(None, '2815578994', '53.5098266', '-113.5411793')
        True
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
        >>> prev_node = Node(None, "2815578994", "53.5098266", "-113.5411793")
        >>> n = d.getNeighbours(prev_node)
        >>> n == [Node(prev_node, "2815578992", "53.5098175", "-113.5411438"), Node(prev_node, "2815578985", "53.5098175", "-113.5412035")]
        True
        """

        with self.driver.session() as session:
            return session.read_transaction(
                self._getNeighbours, prev_node)

    def getNHopNeighbours(self, prev_node, path_type, hops=10):
        # TODO: finish doc test
        """gets the n-hop neighbours for the prev_node:Node

        >>> hops = 10
        >>> d=DBWrapper("bolt://localhost:7687", "neo4j", "test")
        >>> prev_node = SimpleNode(None, "2815578994", "53.5098266", "-113.5411793")
        >>> rows = d.getNHopNeighbours(prev_node, "bike", hops)
        >>> assert len(rows) > 0
        >>> for row in rows:
        ...     assert row[1] >= 0
        ...     assert len(row[0]) == hops + 1
        """

        with self.driver.session() as session:
            return session.read_transaction(
                self._getNHopNeighbours, prev_node, path_type, hops)

    @staticmethod
    def _getNeighbours(tx, prev_node):
        closest_point_to_pathtype_query = """
        Match(n:Node {nodeId: $id})-[w:Way]-(n1:Node)
        Return n1, w.pathType
        """
        res = tx.run(closest_point_to_pathtype_query,
                     id=prev_node.node_id)
        nodes = []
        for r in res:
            nodes.append(Node(prev_node, r.data()['n1']['nodeId'], r.data()[
                         'n1']['lat'], r.data()['n1']['lon'], r.data()['w.pathType']))

        return nodes


    @staticmethod
    def _getNHopNeighbours(tx, prev_node, path_type, hops=10):
        n_hop_q = """
        Match p = (n:Node {nodeId: $id})-[:Way*""" + str(hops) + """]-(n1:Node)
        CALL {
            with p
            UNWIND relationships(p) as w
            with w as W
            where W.pathType = $ptype
            with count(W) as c
            return c
        }
        return nodes(p), c
        """
        res = tx.run(n_hop_q,
                     id=prev_node.node_id,
                     ptype=path_type)

        rows = []
        for r in res:
            # convert list of neo4j nodes to server Nodes
            l = []
            for i, n in enumerate(r.data()['nodes(p)']):
                prev = None
                if i == 0:
                    prev = prev_node
                else:
                    prev = l[i-1]
                l.append(SimpleNode(prev, n['nodeId'], n['lat'], n['lon']))
            # append path and count
            rows.append((l, r.data()['c']))

        # returns: [([Node], int)]
        return rows

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
