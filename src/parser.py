class Parser():
    """ Parses an XML file and creates internal datastructures for representing the environment
    """
    def __init__(self, sceneFile=None) -> None:
        print(f"Creating a parser object {sceneFile}")