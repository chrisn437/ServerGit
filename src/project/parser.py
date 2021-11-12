import xml.etree.ElementTree as ET
# TODO Add TriMesh library and save the scene as a trimesh object

import trimesh
from src.project.sceneProcessor import SceneProcessor
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
        self.fc :list = []
        self.meshpos : list= []
        self.meshrot : list= []
        # TODO add marker container

        self.scene : trimesh.Trimesh = None
        self.sceneProcessor = None

        self.parseScene()
        self.createTrimeshScene(None, None)
        self.startSceneProcessor()



    def parseScene(self):
        for elm in self.root.findall(".//Vertex"):
            atb = elm.attrib.get("position")
            vertex = atb.split()
            vertex = [float(i) for i in vertex]
            self.vrtx.append(Vector3(vertex[0], vertex[1], vertex[2]))
            print(f"{vertex}")
            x2 = atb[0]

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

    def createTrimeshScene(self, vertices, faces):
        # TODO Create a trimesh object
        # TODO add markers to the scene.metadata collection
        markerExample = Marker(1, "exampleLabel", Vector3(1, 1, 1), Vector3(0.0, 0.0, 0.0))
        self.scene.metadata(markerExample.label, markerExample)
        pass

    def startSceneProcessor(self):
        self.sceneProcessor = SceneProcessor()




