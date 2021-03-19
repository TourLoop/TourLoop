// from https://neo4j.com/developer/guide-import-csv/#_optimizing_load_csv_for_performance

// clear data
MATCH (n)
DETACH DELETE n;

// load nodes
LOAD CSV WITH HEADERS FROM 'file:///osm-nodes.csv' AS row
MERGE (n:Node {id:row.id, lat:row.lat, lon:row.lon})
;

// create paths
LOAD CSV WITH HEADERS FROM 'file:///osm-ways.csv' AS row
MATCH (a:Node {id: row.a})
MATCH (b:Node {id: row.b})
MERGE (a)<-[:Way {id:row.id, type:row.type, dist:row.distance}]->(b)
;
