import xml.etree.ElementTree as ET
from src.Structs.Vector3 import Vector3
import trimesh
from src.project.sceneProcessor import SceneProcessor
from src.Structs.Vector3 import Vector3
from src.Structs.Marker import Marker

class Parser():
    """ Parses an XML file and creates a TriMesh objectinternal datastructures for representing the environment        
    """
    def __init__(self, xmlfile):
        print(f"Creating a parser object {xmlfile}")
        # Parse the XML..
        self.tree = ET.parse(xmlfile)
        self.root = self.tree.getroot()

        # Containers for mesh attributes
        self.vrtx : list    = []
        self.fc : list      = []
        self.meshpos : list = []
        self.meshrot : list = []
        self.__trimeshGeo : trimesh.Trimesh = None

        # Container for Marker data structures
        self.markers : list = []
        self.scene : trimesh.Trimesh = None
        self.sceneProcessor = None
        self.parseScene()

    @property
    def getTrimeshGeo(self):
        """ Returns a trimesh object that represents the scene"""
        return self.__trimeshGeo

    def parseScene(self):
        """Extracts XML nodes and saves their attributes
        """
        pivotPoint = None
        # Get mesh node
        for elm in self.root.findall("./Mesh"):
            # 1. Extract pivot point and pivot orientation
            # 2. Create a mesh object and initialize it with the pivots, vertices, face
            # 3. Set the mesh object equal to the mesh member variable
            atbpos = elm.attrib.get("pos")
            new_atbpos = str(atbpos)[1:-1]
            atribute : list = new_atbpos.split(",")
            atribute = [float(i) for i in atribute]
            pivotPoint = [atribute[0], atribute[1], atribute[2]]


        # Get Vertex node
        for elm in self.root.findall(".//Vertex"):
            atb = elm.attrib.get("position")
            vertex : list = atb.split()
            vertex = [float(i) for i in vertex]

            # Append vertices and convert them to global coordinate space by adding the mesh pivot point
            self.vrtx.append([vertex[0] + pivotPoint[0],
                              vertex[1] + pivotPoint[1],
                              vertex[2] + pivotPoint[2]])

        # Get faces
        for elm in self.root.findall(".//Face"):
            atb = elm.attrib.get("vertices")
            face : list = atb.split()
            face = [float(i) for i in face]
            self.fc.append([face[0], face[1], face[2]])

        # Get mesh rotation
        for elm in self.root.findall(".//Mesh"):
            atbrot = elm.attrib.get("rot")
            new_atbrot = str(atbrot)[1:-1]
            atribute : list = new_atbrot.split(",")
            atribute = [float(i) for i in atribute]
            self.meshrot.append(Vector3(atribute[0], atribute[1], atribute[2]))

        # Get markers
        for elm in self.root.findall("./Marker"):
            atbpos = elm.attrib.get("pos")
            new_atbpos = str(atbpos)[1:-1]
            atribute : list = new_atbpos.split(",")
            pos = [float(i) for i in atribute]
            pos = Vector3(pos[0], pos[1], pos[2])

            atbRot = elm.attrib.get("rot").strip("(").strip(")").split(",")
            atbRot = [float(i) for i in atbRot]

            atbID = int(elm.attrib.get("id"))

            # Ignore marker ID 49, that's for global reference
            if atbID == 49:
                continue
            self.markers.append(Marker(atbID, atbID, pos, atbRot))

        # Create the Trimesh object once the XML is parsed
        self.createTrimeshScene(self.vrtx, self.fc, self.markers)

    

    def createTrimeshScene(self, vectorvertex, vectorfaces, markers):
        # Create a Trimesh object with Markers as metadata
        if(self.__trimeshGeo is None):
            self.__trimeshGeo :trimesh.Trimesh  = trimesh.Trimesh(vectorvertex, vectorfaces)
            self.__trimeshGeo.metadata['markers'] = markers

    def startSceneProcessor(self, geometry):
        self.sceneProcessor = SceneProcessor(geometry)
        