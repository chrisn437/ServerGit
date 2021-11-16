import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client


from src.Structs.Constants import SAVED_SCENE
from src.project.parser import Parser


class OscNetwork():
    """ OSC Message receiver and sender
    """

    def __init__(self):
        self.sceneParser = Parser(SAVED_SCENE)
        print("Initializing OSC interface")

        ip = "127.0.0.1"
        sendPort = 7000
        inPort = 8000

        #Sending osc message
        client = udp_client.SimpleUDPClient(ip, sendPort)

        #catch OSC message
        dispater = dispatcher.Dispatcher()
        dispater.map()

        #Serer for listening
        server = osc_server.ThreadingOSCUDPServer((ip, inPort),dispatcher)
        print("Servering on {}".format(server.server_address))
        server.serve_forever()

