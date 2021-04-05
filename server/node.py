from vincenty import vincenty


# TODO: make this a subclass of simple node
class Node:

    # Remember to initialize the end target (lat, lon)
    # and target_distance for the Node class!
    target = (0.0, 0.0)
    target_distance = 0.0

    def __init__(self, prev_node, node_id, lat, lon):
        self.prev_node = prev_node
        self.node_id = node_id
        self.lat = float(lat)
        self.lon = float(lon)

        if prev_node == None:
            self.path_dist = 0.0
        else:
            self.path_dist = prev_node.path_dist + \
                vincenty((self.lat, self.lon), (prev_node.lat, prev_node.lon))

        self.target_dist_est = vincenty((self.lat, self.lon), Node.target)

        self.huer = abs(Node.target_distance - self.path_dist - self.target_dist_est)

    def __lt__(self, other):
        return self.huer < other.huer

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def getLatLonTuple(self):
        return (self.lat, self.lon)

    def getD(self, other):
        return vincenty(self.getLatLonTuple(), other.getLatLonTuple())

class SimpleNode:
    def __init__(self, prev_node, node_id, lat, lon):
        self.prev_node = prev_node
        self.node_id = node_id
        self.lat = float(lat)
        self.lon = float(lon)

    def getLatLonTuple(self):
        return (self.lat, self.lon)

    def getD(self, other):
        return vincenty(self.getLatLonTuple(), other.getLatLonTuple())
