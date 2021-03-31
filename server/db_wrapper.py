from query_helpers import get_neo4j_driver, closest_point
from neo4j import GraphDatabase, basic_auth

class DBWrapper:
    def __init__(self, uri, username, password):
        driver = GraphDatabase.driver(uri, auth=basic_auth(username, password))
        self.driver = driver

    def close(self):
        self.driver.close()

    def getSession(self):
        return self.driver.session()

    def getClosestPoint(self, lat_string, lon_string):
        with self.getSession() as session:
            return closest_point(self.getSession(), lat_string, lon_string)

    def getNeighbours(self, currentId, max_path_length):
        neigh_q = """
        match (start:Node {id: '$currentId'})
        match (start:Node)-[w:Way]-(nxt:Node)
        where w.dist < $maxD
        return nxt, w
        order by w.pathType
        """
        with self.getSession() as session:
            res = session.run(neigh_q, currentId=currentId, maxD=max_path_length)
            # r in res is dict('nxt', 'pathtype')
            return res

    def getClosestPointToPathtype(self, path_string, lat_string, lon_string):
        with self.getSession() as session:
            return closest_point_to_pathtype(self.getSession(), path_string, lat_string, lon_string)

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
        with self.getSession() as session:
            res = self.getSession().run(pins_query)
            # res has many rows
            # res.data() returns a list of these rows
            # each row has keys : ['c', 'd', 'nodes', 'ways']

            # one route is a list of node json objects
            routes = [row['nodes'] for row in res]
        return routes

