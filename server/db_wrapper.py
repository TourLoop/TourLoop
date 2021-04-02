from neo4j import GraphDatabase, basic_auth


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
            res = session.read_transaction(self._getClosestPoint,
                                           lat_string, lon_string)

        return record_to_lat_lon_dict(res)

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
        return res.single()

    # TOURLOOP FR3 : Closest Node point
    def getClosestPointToPathtype(self, path_string, lat_string, lon_string):
        """find closest lat long point in db given a lat long string

        >>> d=DBWrapper("bolt://localhost:7687", "neo4j", "test")
        >>> d.getClosestPointToPathtype("bike", '53.509905', '-113.541233')
        {'lat': 53.5098266, 'lon': -113.5411793}
        """

        with self.driver.session() as session:
            res = session.read_transaction(
                self._getClosestPointToPathtype, path_string, lat_string, lon_string)
        return record_to_lat_lon_dict(res)

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
        return res.single()

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


if __name__ == "__main__":
    d = DBWrapper("bolt://localhost:7687", "neo4j", "test")
    print(d.getClosestPoint('53.509905', '-113.541233'))
