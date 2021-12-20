#!/usr/bin/bash



# Example input variables
from src.project.oscNetwork import OscNetwork
from src.project.sceneProcessor import SceneProcessor
from src.project.tcpNetwork import Server
from src.project.parser import Parser
from src.project.userPosTracking import UserPosTracking
import src.Structs.Constants as const

def main():
    # Run the server in navigation mode
    # s = Parser("res/AAU_AR_LAB.txt")
    # geo = s.getTrimeshGeo
    # sceneProcessor = SceneProcessor(geo)
    # oscNetwork = OscNetwork(sceneProcessor)

    # Run the server for serving the Environment Mapping module..
    tcpNetwork = Server("192.168.1.100", 8050)


if __name__ == '__main__':
    main()