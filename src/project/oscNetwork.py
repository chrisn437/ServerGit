from src.project.parser import Parser
from src.Structs.Constants import SAVED_SCENE, COMPLEX_SCENE
class OscNetwork():
    """ OSC Message receiver and sender
    """

    def __init__(self):
        print("Initializing OSC interface")