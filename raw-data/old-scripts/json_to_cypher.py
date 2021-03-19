import json

print("\nThe full OSM dataset makes a 347Mb cypher file... cypher has a really hard time loading this")
print("Stop it. get some help. Just make a CSV file.\n")

print("reading json")
a = []
#with open("extracted/extracted.json") as f:
with open("extracted/extracted.json") as f:
    a = json.load(f)


nodes = a['node']
ways = a['way']
#print(len(ways))
#print(len(nodes))

print("converting data to dict")
nodes_dict = {n["id"]:n for n in nodes}
ways_dict = {w["id"]:w for w in ways}


def node_to_cypher_create(n):
    create_node_fmt = "CREATE (n{}:Node {})\n"
    props_fmt = "id:{}, lat: {}, lng: {}"
    d = props_fmt.format(n['id'], float(n['lat']), float(n['lon']))
    return create_node_fmt.format(n['id'], "{"+d+"}")

def way_to_cypher_create(w):
    # TODO: fill in with real path type
    create_statement = "CREATE\n"
    edge_props = ""
    edge_fmt = "({})<-[:Way {}]->({}){}\n"

    for i in range(len(w['path']) -1):
        j = i+1
        a = 'n' + w['path'][i]
        b = 'n' + w['path'][j]
        comma = ","
        if j == len(w['path']) - 1:
            # working with last edge
            comma = ""
        create_statement += edge_fmt.format(a, edge_props, b, comma)
    return create_statement

print("write cypher create statement")
with open("osm-create.cypher", 'w') as f:

    print("write nodes")
    for n in nodes:
        f.write(node_to_cypher_create(n))

    print("write paths")
    for w in ways:
        f.write(way_to_cypher_create(w))
