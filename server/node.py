class Node:
    def __init__(self, prev_node, node_id, lat, lon):
        self.prev_node = prev_node
        self.node_id = node_id
        self.lat = float(lat)
        self.lon = float(lon)
