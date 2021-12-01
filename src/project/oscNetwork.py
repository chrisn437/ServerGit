#from pythonosc import dispatcher
#from pythonosc import osc_server
#from pythonosc import udp_client


class OscNetwork():
    """ OSC Message receiver and sender
    """


    def __init__(self):
        #self.sceneParser = Parser(SAVED_SCENE)
        print("Initializing OSC interface")

        self.ip = "192.168.1.214"
        self.sendPort = 7000
        self.inPort = 8000
        self.stop_listening = None

        #setting oscNetwork up
        self.client = udp_client.SimpleUDPClient(self.ip, self.sendPort)

        #catch OSC message
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/start listeneng", handler= None)
        self.start_listening()

        #Serer for listening
        server = osc_server.ThreadingOSCUDPServer((self.ip, self.inPort),self.dispatcher)
        print("Servering on {}".format(server.server_address))
        server.serve_forever()

    def start_listening(self):
        global stop_listening
        string2 = "hallo wie gehts"
        encoded_string = string2.encode()
        byte_array = bytearray(encoded_string)
        print("started listening")
        self.client.send_message("/position update", byte_array)
        self.stop_listening = None
        pass
