# from https://www.tutorialspoint.com/python3/python_xml_processing.htm
import xml.sax
import json
import os
from osm_csv_helper import *


class OsmHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.curr_tag = None

        self.way_f = open("osm-ways.csv", 'w')
        self.node_f = open("osm-nodes.csv", 'w')
#        self.way_f.write("id,type,distance,a,b\n")
#        self.node_f.write("id,lat,lon\n")

        self.all_paths_f = open("all_paths.txt", 'w')
        self.all_bike_paths_f = open("all_bike_paths.txt", 'w')

        self.curr = dict()
        self.curr["node"] = None
        self.curr["way"] = None

        self.id_to_coords = dict()

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
            # self.parsed[tag].append(self.curr[tag])
            self.writeToCsv(tag)

    def writeToCsv(self, tag):
        if tag == "way":
            write_way_csv(self.curr[tag], self.id_to_coords,
                          self.way_f, self.all_paths_f, self.all_bike_paths_f)
        if tag == "node":
            self.id_to_coords[self.curr[tag]['id']] = (
                self.curr[tag]['lat'], self.curr[tag]['lon'])
            write_node_csv(self.curr[tag], self.node_f)


# TOURLOOP FR17 : Clean OpenStreetMap data
def main():
    # code largely from turotial
    # from https://www.tutorialspoint.com/python3/python_xml_processing.htm

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = OsmHandler()
    parser.setContentHandler(Handler)

    parser.parse("../raw-data/edmonton-OSM-data.xml")


if __name__ == "__main__":
    main()
