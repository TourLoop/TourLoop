from vincenty import vincenty


# TODO: make this a subclass of simple node
class Node:
    """
    >>> n = Node(None, "1", 0.0, 0.0)
    >>> n.pref_count
    0
    >>> n.count
    1
    >>> Node.target_path_type = "bike"
    >>> n2 = Node(n, "2", 0.0, 0.0, "bike")
    >>> n2.count
    2
    >>> n2.pref_count
    1
    """

    # Remember to initialize the end target (lat, lon)
    # and target_distance for the Node class!
    target = (0.0, 0.0)
    target_distance = 0.0
    target_path_type = None

    def __init__(self, prev_node, node_id, lat, lon, path_type=""):
        self.prev_node = prev_node
        self.node_id = node_id
        self.lat = float(lat)
        self.lon = float(lon)

        one_or_zero = lambda x : 1 if x == Node.target_path_type else 0
        if prev_node == None:
            self.path_dist = 0.0
            self.pref_count = one_or_zero(path_type)
            self.count = 1
        else:
            self.pref_count = prev_node.pref_count + one_or_zero(path_type)
            self.count = prev_node.count + 1
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
