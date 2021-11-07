from src.project.parser import Parser
from src.Structs.Constants import SAVED_SCENE
class OscNetwork():
    """ OSC Message receiver and sender
    """

    def __init__(self):
        self.sceneParser = Parser(SAVED_SCENE)
        print("Initializing OSC interface")