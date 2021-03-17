import json

#print(len(ways))
#print(len(nodes))

def path_type(w):
    # from a way, reduce to TourLoop path type
    return "?"

def distance(a, b):
    # calc distance between node a and b
    return 1.0

def write_node_csv(n, f):
    f.write("{},{},{}\n".format(n['id'], float(n['lat']), float(n['lon'])))

def write_way_csv(w, f):
    for i in range(len(w['path']) -1):
        j = i+1
        a = w['path'][i]
        b = w['path'][j]
        f.write("{},{},{},{},{}\n".format(\
            w['id'],\
            path_type(w),\
            distance(a, b),\
            a,\
            b))


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
