import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction

from src.Structs.Vector3 import Vector3
from src.Structs.Marker import Marker
from src.Structs.Environment import Environment

xmlfile = r"C:\Users\chris\AppData\Local\GitHubDesktop\app-2.9.4\SP_Server\res\savedScene.xml"

tree = ET.parse(xmlfile)
root = tree.getroot()

ET.dump(tree)

meshpos= []
meshrot = []

fc = []

for elm in root.findall(".//Vertex"):
    vrtx = elm.attrib
    print(f"{vrtx}")

print(f"{vrtx[0]}")
"""""
for elm in root.findall(".//Face"):
    fc = elm.attrib
    print(f"{fc}")

for elm in root.findall("./Mesh[@pos=' ']"):
    print(elm.attrib)
"""
class Parser():
    """ Parses an XML file and creates internal datastructures for representing the environment
    """

    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        print(f"Creating a parser object {xmlfile}")
        d = Vector3(1, 2, 3)

    def parseScene(xmlfile):
        for vertices in xmlfile():
            print(f"{vertices.tag}")
        # 1. Read the XML files using an XML reading library, for example xml.elementtree(google precise name)
        # 2. Create the data structure objects from whatever you're reading
        pass
