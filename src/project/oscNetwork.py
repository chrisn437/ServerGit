from src.project.parser import Parser
class OscNetwork():
    """ OSC Message receiver and sender
    """

    def __init__(self):
        d = Parser()
        print("Initializing OSC interface")