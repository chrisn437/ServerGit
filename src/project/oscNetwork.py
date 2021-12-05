
import argparse
import math
import numpy as np

from src.Structs.Vector3 import Vector3

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
from src.project.pathfinder import Pathfinder

from src.Structs.Constants import SAVED_SCENE
from src.project.parser import Parser
import src.project.sceneProcessor as sp


from src.project.parser import Parser
from src.Structs.Constants import SAVED_SCENE, COMPLEX_SCENE

class OscNetwork():
    """ OSC Message receiver and sender
    """


    def __init__(self, sceneProcessor : sp.SceneProcessor):
        #self.sceneParser = Parser(SAVED_SCENE)
        print("Initializing OSC interface")

        self.magicLeapIP = "192.168.1.112"
        self.ip = "192.168.1.214"
        self.sendPort = 8052
        self.inPort = 8051

        self.sceneProcessor = sceneProcessor

        #setting oscNetwork up
        self.client = udp_client.SimpleUDPClient(self.magicLeapIP, self.sendPort)

        #catch OSC message
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/setDestinations", self.start_listening)


        #Serer for listening
        server = osc_server.ThreadingOSCUDPServer((self.ip, self.inPort),self.dispatcher)
        print("Servering on {}".format(server.server_address))
        server.serve_forever()



    def start_listening(self, addr, startPos, *destinatons):
        print(addr)
        startPos = startPos.strip('(').strip(')')
        startPos = startPos.replace(",", "")
        startPos = startPos.split()
        print(startPos)
        startPos = [float(i) for i in startPos]
        startPos = Vector3(startPos[0], startPos[1], startPos[2])
        destinatons = [int(i) for i in destinatons]





        route = []
        grid = self.sceneProcessor.getGrid()
        markers = self.sceneProcessor.getMarkers()
        print(markers)
        for iteration, i in enumerate(destinatons):
            if iteration == 0:
                # Check if any of the markers has the IDs
                for marker in markers:
                    if marker.id == i:
                        startIndecie = grid[0].voxelGrid.points_to_indices(startPos.Vec3)
                        markerIndecie = grid[0].voxelGrid.points_to_indices(marker.pos.Vec3)
                        startIndecie = (startIndecie[0], startIndecie[1], startIndecie[2])
                        markerIndecie = (markerIndecie[0], markerIndecie[1], markerIndecie[2])
                        pathfinder = Pathfinder(grid, startIndecie, markerIndecie)
                        route.append(pathfinder.getRoute())
            else:
                startPos = None
                endPos = None
                for marker in markers:
                    if marker.id == i:
                        endPos = marker.pos
                    if marker.id == destinatons[iteration - 1]:
                        startPos = marker.pos

                startIndecie = grid[0].voxelGrid.points_to_indices(startPos.Vec3)
                endrIndecie = grid[0].voxelGrid.points_to_indices(endPos.Vec3)
                startIndecie = (startIndecie[0], startIndecie[1], startIndecie[2])
                endrIndecie = (endrIndecie[0], endrIndecie[1], endrIndecie[2])
                pathfinder = Pathfinder(grid, startIndecie, endrIndecie)
                route.append(pathfinder.getRoute())

        self.client.send_message("/destinations", route)