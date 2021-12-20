import datetime
import argparse
import math
import numpy as np
import os

from src.Structs.Vector3 import Vector3

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
from src.project.pathfinder import Pathfinder
from src.project.userPosTracking import UserPosTracking

from src.Structs.Constants import SAVED_SCENE
from src.project.parser import Parser
import src.project.sceneProcessor as sp


from src.project.parser import Parser
from src.Structs.Constants import SAVED_SCENE, COMPLEX_SCENE

class OscNetwork():
    """ OSC Message receiver and sender
    """
    time2 = str(datetime.datetime.now().strftime(("%H%M%S")))

    def __init__(self, sceneProcessor : sp.SceneProcessor):
        #self.sceneParser = Parser(SAVED_SCENE)
        print("Initializing OSC interface")

        self.magicLeapIP = "192.168.1.100"
        self.ip = "192.168.1.103"
        self.sendPort = 8052
        self.inPort = 8051

        self.sceneProcessor = sceneProcessor

        #setting oscNetwork up
        self.client = udp_client.SimpleUDPClient(self.magicLeapIP, self.sendPort)

        #catch OSC message
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/setDestinations", self.start_listening)
        self.dispatcher.map("/position", self.posListener)
        self.dispatcher.map("/stopTiming", self.stopListening)
        self.listenToPositionUpdates = True


        #Serer for listening
        server = osc_server.ThreadingOSCUDPServer((self.ip, self.inPort),self.dispatcher)
        print("Servering on {}".format(server.server_address))
        server.serve_forever()


    # Starts listnening and takes in the destinations and start position
    def start_listening(self, addr, startPos, *destinatons):
        print(addr)
        startPos = startPos.strip('(').strip(')')
        startPos = startPos.replace(",", "")
        startPos = startPos.split()

        print(startPos)
        startPos = [float(i) for i in startPos]
        startPos = Vector3(startPos[0], startPos[1], startPos[2])
        startingPos = startPos

        destinatons = [int(i) for i in destinatons]
        # enables we can calculate more than just one route
        routes = []
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
                        print(startIndecie)
                        print(markerIndecie)
                        pathfinder = Pathfinder(grid, startIndecie, markerIndecie)
                        routes.append(pathfinder.getRoute())
                        print("Route appended..")

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

                print(startIndecie)
                print(endrIndecie)
                pathfinder = Pathfinder(grid, startIndecie, endrIndecie)
                routes.append(pathfinder.getRoute())
                print("Route appended..")



        points = []
        for route in routes:
            for indice in route:
                e = np.array([indice[0], indice[1], indice[2]]) # go from tuple to list because tuple doesnt have asType as required by pycharm
                entry = grid[0].voxelGrid.indices_to_points(e)
                entry = np.array([entry[0], entry[1], entry[2]])
                points.append(entry)


        # Flatten out the points array into a single 1D array
        output = []
        for point in points:
            for dimension in point:
                output.append(dimension)
        print(route)
        print(output)
        self.client.send_message("/destinations", output)

    # Stops listening, so we can switch it on and off
    def stopListening(self, addr):
        print(addr)
        self.listenToPositionUpdates = False

    # Creates and safes a file of the position updates
    def posListener(self, addr, *args):

        if self.listenToPositionUpdates == True:
            print(f"{addr} {args}")

            path = "res"
            fileName = f"PositionLog_{OscNetwork.time2}.txt"
            outputpath = os.path.join(os.getcwd(), path, fileName)
            fileexist: bool = os.path.exists(outputpath)
            time = str(datetime.datetime.now().strftime(('%H:%M:%S.%f')))
            with open(outputpath, "a" if fileexist else "w") as fh:
                fh.write(f"{time} {args} \n\r")
                fh.flush()
                fh.close()