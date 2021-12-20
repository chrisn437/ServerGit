import xml.etree.ElementTree as ET
# TODO Add TriMesh library and save the scene as a trimesh object
from src.Structs.Vector3 import Vector3
import trimesh
from src.project.sceneProcessor import SceneProcessor
from src.Structs.Vector3 import Vector3
from src.Structs.Marker import Marker
from src.Structs.Mesh import Mesh



class Parser():
    # Parses an XML file and creates internal datastructures for representing the environment
    def __init__(self, xmlfile):
        print(f"Creating a parser object {xmlfile}")
        self.tree = ET.parse(xmlfile)
        self.root = self.tree.getroot()

        self.vrtx : list = []
        self.fc :list = []
        self.meshpos : list= []
        self.meshrot : list= []
        self.__trimeshGeo : trimesh.Trimesh = None
        self.markers : list = []
        arucoMarker = Marker(2, "shelf 2", (2, 6, 0), (1, 2, 3))


        self.scene : trimesh.Trimesh = None
        self.sceneProcessor = None
        self.parseScene()

    @property
    def getTrimeshGeo(self):
        return self.__trimeshGeo

    def parseScene(self):
        pivotPoint = None
        for elm in self.root.findall("./Mesh"):
            # 1. Extract pivot point and pivot orientation
            # 2. Create a mesh object and initialize it with the pivots, vertices, face
            # 3. Set the mesh object equal to the mesh member variable
            atbpos = elm.attrib.get("pos")
            new_atbpos = str(atbpos)[1:-1]
            atribute : list = new_atbpos.split(",")
            atribute = [float(i) for i in atribute]
            pivotPoint = [atribute[0], atribute[1], atribute[2]]
            self.meshpos.append([atribute[0], atribute[1], atribute[2]])

        # Parses the Vertexes
        for elm in self.root.findall(".//Vertex"):
            atb = elm.attrib.get("position")
            vertex : list = atb.split()
            vertex = [float(i) for i in vertex]
            self.vrtx.append([vertex[0] + pivotPoint[0],
                              vertex[1] + pivotPoint[1],
                              vertex[2] + pivotPoint[2]])

        # Parses the Faces
        for elm in self.root.findall(".//Face"):
            atb = elm.attrib.get("vertices")
            face : list = atb.split()
            face = [float(i) for i in face]
            self.fc.append([face[0], face[1], face[2]])


        # Parses the rotation Data of the Mesh
        for elm in self.root.findall("./Mesh"):
            atbrot = elm.attrib.get("rot")
            new_atbrot = str(atbrot)[1:-1]
            atribute : list = new_atbrot.split(",")
            atribute = [float(i) for i in atribute]
            self.meshrot.append(Vector3(atribute[0], atribute[1], atribute[2]))

        # Parses the Marker information
        for elm in self.root.findall("./Marker"):
            # 1. Extract pivot point and pivot orientation
            # 2. Create a mesh object and initialize it with the pivots, vertices, face
            # 3. Set the mesh object equal to the mesh member variable
            #self.mesh = Mesh(pivotPoint, pivotOrientat, self.vrtx, self.fc)
            atbpos = elm.attrib.get("pos")
            new_atbpos = str(atbpos)[1:-1]
            atribute : list = new_atbpos.split(",")
            pos = [float(i) for i in atribute]
            pos = Vector3(pos[0], pos[1], pos[2])

            atbRot = elm.attrib.get("rot").strip("(").strip(")").split(",")
            atbRot = [float(i) for i in atbRot]

            atbID = int(elm.attrib.get("id"))

            if atbID == 49:
                continue
            self.markers.append(Marker(atbID, atbID, pos, atbRot))

        self.createTrimeshScene(self.vrtx, self.fc, self.markers)

    
    # Creating a TriMesh scene
    def createTrimeshScene(self, vectorvertex, vectorfaces, markers):
        # TODO add markers to the scene.metadata collection
        self.arucoMarker = 1, "exampleLabel", Vector3(1, 1, 1), Vector3(0.0, 0.0, 0.0)
        #  metadata = {}
        # metadata : dict = self.scene.metadata(self.arucoMarker.ID, self.arucoMarker)

        # TODO Create a trimesh object
        if(self.__trimeshGeo is None):
            self.__trimeshGeo :trimesh.Trimesh  = trimesh.Trimesh(vectorvertex, vectorfaces)
            self.__trimeshGeo.metadata['markers'] = markers
        #self.startSceneProcessor(sceneGeo)

    # Initialising the ScneProcessor
    def startSceneProcessor(self, geometry):
        self.sceneProcessor = SceneProcessor(geometry)
        