from neo4j import GraphDatabase, basic_auth


if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "test"
    driver = GraphDatabase.driver( uri, auth=basic_auth(username, password))
    with driver.session() as session:
        index1 = """
        CREATE INDEX nodeid_index IF NOT EXISTS FOR (n:Node) ON (n.nodeId)
        """
        index2 = """
        CREATE INDEX location_index IF NOT EXISTS FOR (n:Node) ON (n.location)
        """

        delsingles = """
        Match(n:Node)
        WHERE NOT (n)-[:Way]-(:Node)
        Delete n
        """

        session.run(index1)
        session.run(index2)
        session.run(delsingles)

        print("indices created and deleted single nodes :)")
