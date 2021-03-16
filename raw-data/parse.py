# from https://www.tutorialspoint.com/python3/python_xml_processing.htm
import xml.sax
import json

class MovieHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.curr_tag = None

        self.curr = dict()
        self.curr["node"] = None
        self.curr["way"] = None

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

        return

    # Call when an elements ends
    def endElement(self, tag):
        if self.isItem(tag):
            self.endItem(tag)
        return

# helper functions

    def newWay(self, tag, attributes):
        way = dict()
        way["id"] = attributes["id"]
        way["path"] = []
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
        if self.curr_tag == tag:
            self.curr_tag = None
            self.parsed[tag].append(self.curr[tag])



if ( __name__ == "__main__"):

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler( Handler )

    parser.parse("edmonton-OSM-data.xml")
    #print(len(list(filter(lambda x: x != None, Handler.parsed["way"]))))

    print("json dump parsed")
    with open("extracted/extracted.json", 'w') as f:
        json.dump(Handler.parsed, f)
