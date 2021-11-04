from src.parser import Parser

class TcpNetwork():
    def __init__(self):
        print("Opening a TCP socket")
        self.sceneFile = "<MyScene />"
        self.initSceneParser()

    def initSceneParser(self):
        parser = Parser(self.sceneFile) 

    # TODO port the TCP code here