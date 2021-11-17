#!/usr/bin/bash



# Example input variables
from src.project.oscNetwork import OscNetwork
from src.project.parser import Parser
from src.project.sceneProcessor import SceneProcessor
from src.project.tcpNetwork import TcpNetwork
from src.project.tcpNetwork import Server
import src.Structs.Constants as const

def main():
<<<<<<< HEAD
    #oscNetwork = OscNetwork()
    tcpNetwork = Server("192.168.1.214", 8050)
    creatserver = Server()
    sceneProcessor = SceneProcessor()
=======
    s = Parser(const.SAVED_SCENE)
    geo = s.getTrimeshGeo
    sceneProcessor = SceneProcessor(geo)
>>>>>>> WIP draft simple mesh fill flooding and locating voxel cell of the listener
    #oscNetwork = OscNetwork()
    #tcpNetwork = Server("127.0.0.1", 7000)
    #creatserver = Server()

if __name__ == '__main__':
    main()