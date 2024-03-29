# from https://www.tutorialspoint.com/python3/python_xml_processing.htm
import xml.sax
import json
import os
from osm_csv_helper import *

class Node:
    def __init__(self, lat, lng, id):
        self.lat = lat
        self.lng = lng
        self.id = id

    def getCoords(self):
        return (self.lat, self.lng)


class OsmHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.curr_tag = None

        self.way_f = open("osm-ways.csv", 'w')
        self.node_f = open("osm-nodes.csv", 'w')

        self.all_dirt_paths_f = open("all_dirt_paths.txt", 'w')
        self.all_bike_paths_f = open("all_bike_paths.txt", 'w')
        self.all_paved_paths_f = open("all_paved_paths.txt", 'w')

        self.curr = dict()
        self.curr["node"] = None
        self.curr["way"] = None

        self.id_to_nodes = dict()
        self.written_node_ids = set()

        self.parsed = dict()
        self.parsed["node"] = []
        self.parsed["way"] = []

# super class

    # Call when an element starts
    def startElement(self, tag, attributes):
        #print("tag: {}".format(tag))
        if self.isItem(tag):
            self.startItem(tag)
            self.curr_tag = tag
            if tag == "way":
                self.newWay(tag, attributes)
            if tag == "node":
                self.newNode(tag, attributes)

        elif self.curr_tag == "node":
            # current tag is a child of <node>
            None
        elif self.curr_tag == "way":
            # current tag is a child of <way>
            # building a path for a way node
            if tag == "nd":
                self.curr["way"]["path"].append(attributes["ref"])

            # construct tags dictionary for way
            if tag == "tag":
                self.curr["way"]["tags"][attributes['k']] = attributes['v']

        return

    # Call when an elements ends
    def endElement(self, tag):
        # close csv files
        if tag == "osm":
            self.way_f.close()
            self.node_f.close()

        # handle finish node or way
        if self.isItem(tag):
            self.endItem(tag)
        return

# helper functions

    def newWay(self, tag, attributes):
        way = dict()
        way["id"] = attributes["id"]
        way["path"] = []
        way["tags"] = dict()
        way["path-type"] = "?"
        self.curr["way"] = way

    def newNode(self, tag, attributes):
        node = dict()
        for t in ["id", "lat", "lon"]:
            node[t] = attributes[t]
        self.curr["node"] = node

    def isItem(self, name):
        return name in {"node", "way"}

    def startItem(self, tag):
        self.curr[tag] = dict()

    def endItem(self, tag):
        # finished a node or a way
        if self.curr_tag == tag:
            self.curr_tag = None
            self.writeToCsv(tag)

    def writeToCsv(self, tag):
        if tag == "way":
            write_way_csv(self.curr[tag], self.written_node_ids, self.id_to_nodes,
                          self.way_f, self.node_f, self.all_dirt_paths_f, self.all_bike_paths_f, self.all_paved_paths_f)
        if tag == "node":
            self.id_to_nodes[self.curr[tag]['id']] = Node(self.curr[tag]['lat'], self.curr[tag]['lon'], self.curr[tag]['id'])


# TOURLOOP FR17 : Clean OpenStreetMap data
def main():
    parse_osm_xml("../raw-data/edmonton-OSM-data.xml")

def parse_osm_xml(filename):
    """
    >>> test_filename ="../raw-data/belgravia-test.xml"
    >>> parse_osm_xml(test_filename)
    >>> assert count_nodes(test_filename)  >= count_lines("osm-nodes.csv")
    >>> count_nodes(test_filename) != 0
    True
    >>> cleanup_parsed_files()

    """
    # code largely from turotial
    # from https://www.tutorialspoint.com/python3/python_xml_processing.htm

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = OsmHandler()
    parser.setContentHandler(Handler)

    parser.parse(filename)

def count_lines(filename, fil= lambda x: True ):
    with open(filename) as f:
        return len(list(filter(fil, f.readlines())))


def count_nodes(filename):
    return count_lines(filename, lambda x: "<node " in x)

def cleanup_parsed_files():
    import os
    import glob
    for pattern in ["./*.csv", "./*.txt"]:
        for filePath in glob.glob(pattern):
            os.remove(filePath)

if __name__ == "__main__":
    main()
