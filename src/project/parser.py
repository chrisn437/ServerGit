import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction

from src.Structs.Vector3 import Vector3
from src.Structs.Marker import Marker
from src.Structs.Environment import Environment

xmlfile = r"res\\savedScene.xml"

tree = ET.parse(xmlfile)
root = tree.getroot()

ET.dump(tree)

mesh = []
vrtx = []
fc = []

for elm in root.findall(".//Vertex"):
    vrtx = elm.attrib
    print(f"{vrtx}")

for elm in root.findall(".//Face"):
    fc = elm.attrib
    print(f"{fc}")

for elm in root.findall("./Mesh"):
    mesh = elm.attrib
    print(f"{mesh}")

class Parser():
    # Parses an XML file and creates internal datastructures for representing the environment
    def __init__(self, xmlfile):
        print(f"Creating a parser object {xmlfile}")




    def parseScene(xmlfile):
        for vertices in xmlfile():
            print(f"{vertices.tag}")
        # 1. Read the XML files using an XML reading library, for example xml.elementtree(google precise name)
        # 2. Create the data structure objects from whatever you're reading
        pass
