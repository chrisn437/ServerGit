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

from src.Structs.Constants import SAVED_SCENE
from src.project.parser import Parser
import src.project.sceneProcessor as sp


from src.project.parser import Parser
from src.Structs.Constants import SAVED_SCENE, COMPLEX_SCENE

class OscNetwork():
    """ OSC Message receiver and sender """
    time2 = str(datetime.datetime.now().strftime(("%H%M%S")))

    def __init__(self, sceneProcessor : sp.SceneProcessor):
        print("Initializing OSC interface")
        # Initial variables
        self.magicLeapIP = "127.0.0.1"
        self.ip = "127.0.0.1"
        self.sendPort = 8052
        self.inPort = 8051

        # Scene processor for accessing certain properties from it
        self.sceneProcessor = sceneProcessor

        # Reference to transmitter aiming at Magic Leap's IP address
        self.oscSender = udp_client.SimpleUDPClient(self.magicLeapIP, self.sendPort)

        #catch OSC message
        self.dispatcher = dispatcher.Dispatcher()
        self.listenToPositionUpdates = True
        self.setDispatcherHandlers()

        # Server for listening
        server = osc_server.ThreadingOSCUDPServer((self.ip, self.inPort),self.dispatcher)
        print("Servering on {}".format(server.server_address))
        server.serve_forever()

    def setDispatcherHandlers(self):
        """ Sets incoming message handlers """
        self.dispatcher.map("/setDestinations", self.respToNavReq)
        self.dispatcher.map("/position", self.posListener)
        self.dispatcher.map("/stopTiming", self.stopListening)

    def respToNavReq(self, addr, startPos, *destinatons):
        """ Responds to a navigation request """

        # Get the starting position and create a Vector3 out of it
        print(addr)
        startPos = startPos.strip('(').strip(')')
        startPos = startPos.replace(",", "")
        startPos = startPos.split()
        print(startPos)
        startPos = [float(i) for i in startPos]
        startPos = Vector3(startPos[0], startPos[1], startPos[2])

        # Convert destination indices to integers
        destinatons = [int(i) for i in destinatons]

        # Get markers, voxel grid and prepare a route collection for output
        routes = []
        sceneGrid = self.sceneProcessor.getGrid()
        markers = self.sceneProcessor.getMarkers()
        print(markers)

        for iteration, i in enumerate(destinatons):
            if iteration == 0: # During first iteration we compute Start -> A
                # Check if any of the markers has the destination IDs
                for marker in markers:
                    if marker.id == i:

                        # Query the grid for the indices at which the start and end Vec3's are located and convert them to tuples
                        startIndecie = sceneGrid[0].voxelGrid.points_to_indices(startPos.Vec3)
                        markerIndecie = sceneGrid[0].voxelGrid.points_to_indices(marker.pos.Vec3)

                        startIndecie = (startIndecie[0], startIndecie[1], startIndecie[2])
                        markerIndecie = (markerIndecie[0], markerIndecie[1], markerIndecie[2])

                        # Get and append the path
                        pathfinder = Pathfinder(sceneGrid, startIndecie, markerIndecie)
                        routes.append(pathfinder.getRoute())
                        print("Route appended..")

            else: # 2nd to Nth iteration we computed B -> C -> N.. paths
                startPos = None
                endPos = None

                for marker in markers:
                    # Get the start-end. Start is previous marker, end is the upcoming destination
                    if marker.id == i:
                        endPos = marker.pos
                    if marker.id == destinatons[iteration - 1]:
                        startPos = marker.pos

                # Query the grid for the indices at which the start and end Vec3's are located and convert them to tuples
                startIndecie = sceneGrid[0].voxelGrid.points_to_indices(startPos.Vec3)
                endrIndecie = sceneGrid[0].voxelGrid.points_to_indices(endPos.Vec3)
                startIndecie = (startIndecie[0], startIndecie[1], startIndecie[2])
                endrIndecie = (endrIndecie[0], endrIndecie[1], endrIndecie[2])

                # Get and append the route
                pathfinder = Pathfinder(sceneGrid, startIndecie, endrIndecie)
                routes.append(pathfinder.getRoute())
                print("Route appended..")



        points = []
        for route in routes:
            for indice in route:
                e = np.array([indice[0], indice[1], indice[2]]) # go from tuple to list because tuple doesnt have asType as required by pycharm
                entry = sceneGrid[0].voxelGrid.indices_to_points(e)
                entry = np.array([entry[0], entry[1], entry[2]])
                points.append(entry)


        # Flatten out the points array into a single 1D array
        output = []
        for point in points:
            for dimension in point:
                output.append(dimension)
        print(route)
        print(output)
        self.oscSender.send_message("/destinations", output)

    def stopListening(self, addr):
        print(addr)
        self.listenToPositionUpdates = False

    def posListener(self, addr, *args):
        """Logs incoming user position """

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


