import json

print("reading json")
a = []
with open("extracted/extracted.json") as f:
    a = json.load(f)


nodes = a['node']
ways = a['way']
#print(len(ways))
#print(len(nodes))

print("converting data to dict")
nodes_dict = {n["id"]:n for n in nodes}
ways_dict = {w["id"]:w for w in ways}

# convert id's in way path to actual node
print("replace way path with polyline base")
for k, w in ways_dict.items():
    w['polyline'] = [ {'lat':float(nodes_dict[nid]['lat']), "lng":float(nodes_dict[nid]['lon'])} for nid in w['path']]

print("write only polyline datastructure")
with open("extracted/polylines.json", 'w') as f:
    json.dump([w['polyline'] for w in ways], f)
