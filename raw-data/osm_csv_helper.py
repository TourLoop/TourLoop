import json

#print(len(ways))
#print(len(nodes))

def path_type(w):
    # from a way, reduce to TourLoop path type
    # bike paths, dirt trials, and paved roads
    # assume bike, dirt, and paved are DISJOINT paths
    if set(w['tags'].values()).intersection({'dirt', 'gravel'}):
        return "dirt"
    elif bike_cond(w):
        return "bike"
    else:
        return "paved"

def bike_cond(w):
    tags = w['tags']
    tags_k = tags.keys()
    tags_v = tags.values()
    bike_keys = {'cycleway', 'cycleway:left', 'cycleway:right'}

    # specifically not a cycleway
    if 'cycleway' in tags_k:
        if tags['cycleway'] == "no":
            return False

    # highway = cycleway, probably a bike path
    if 'highway' in tags_k:
        if tags['highway'] == "cycleway":
            return True

    # got a cycleway tag key
    # TODO: this is an approximation
    if set(tags_k).intersection(bike_keys):
        return True

    # assume not a bike path
    return False

def distance(a, b):
    # calc distance between node a and b
    return 1.0

def write_node_csv(n, f):
    point_fmt = '"{' + "latitude:{}, longitude:{}".format(n['lat'], n['lon']) + '}"'
    line = "Node,{},{},{},{},".format(n['id'],n['id'],n['lat'],n['lon']) + point_fmt
    f.write(line +"\n")

def write_way_csv(w, f):
    for i in range(len(w['path']) -1):
        j = i+1
        a = w['path'][i]
        b = w['path'][j]
        f.write("{},{},{},{},{}\n".format(\
            "Way",\
            a,\
            b,\
            '"{}"'.format(path_type(w)),\
            distance(a,b)))


if __name__ == "__main__":
    print("reading json")
    a = []
    with open("extracted/extracted.json") as f:
        a = json.load(f)


    nodes = a['node']
    ways = a['way']
    print("write nodes csv")
    with open("extracted/osm-nodes.csv", 'w') as f:

        f.write("id,lat,lon\n")
        for n in nodes:
            write_node_csv(n, f)

    print("write ways csv")
    with open("extracted/osm-ways.csv", 'w') as f:
        f.write("is,type,distance,a,b\n")
        for w in ways:
            write_way_csv(w, f)
