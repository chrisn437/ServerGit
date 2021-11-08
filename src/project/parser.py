import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction

from src.Structs.Vector3 import Vector3
from src.Structs.Marker import Marker
from src.Structs.Environment import Environment


class Parser():
    # Parses an XML file and creates internal datastructures for representing the environment
    def __init__(self, xmlfile):
        print(f"Creating a parser object {xmlfile}")
        self.tree = ET.parse(xmlfile)
        self.root = self.tree.getroot()

        ET.dump(self.tree)

        self.vrtx : list = []
        self.fc = []
        self.meshpos = []
        self.meshrot = []
        self.parseScene()
        pass


    def parseScene(self):
        for elm in self.root.findall(".//Vertex"):
            atb = elm.attrib.get("position")
            self.vrtx.append(atb)
            print(f"{atb}")
            #Vector = Vector3(3.2, 2.6, 9.1)
            #self.vrtx.append(Vector)

        for elm in self.root.findall(".//Face"):
            atb = elm.attrib.get("vertices")
            self.fc.append(atb)
            print(f"{atb}")

        for elm in self.root.findall("./Mesh"):
            # 1. Extract pivot point and pivot orientation
            # 2. Create a mesh object and initialize it with the pivots, vertices, face
            # 3. Set the mesh object equal to the mesh member variable
            #self.mesh = Mesh(pivotPoint, pivotOrientat, self.vrtx, self.fc)
            atbpos = elm.attrib.get("pos")
            self.meshpos.append(atbpos)
            print(f"{atbpos}")

            atbrot = elm.attrib.get("rot")
            self.meshrot.append(atbrot)
            print(f"{atbrot}")

