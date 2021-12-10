#!/usr/bin/bash



# Example input variables
from src.project.oscNetwork import OscNetwork
from src.project.sceneProcessor import SceneProcessor
from src.project.tcpNetwork import TcpNetwork
from src.project.tcpNetwork import Server
from src.project.parser import Parser
import src.Structs.Constants as const

def main():
    s = Parser("res/savedFile_224024.txt")
    geo = s.getTrimeshGeo
    sceneProcessor = SceneProcessor(geo)
    oscNetwork = OscNetwork(sceneProcessor)
    #tcpNetwork = Server("192.168.1.100", 8050)
    #creatserver = Server()

if __name__ == '__main__':
    main()