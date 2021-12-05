#!/usr/bin/bash



# Example input variables
from src.project.oscNetwork import OscNetwork
from src.project.parser import Parser
from src.project.sceneProcessor import SceneProcessor
from src.project.tcpNetwork import TcpNetwork
from src.project.tcpNetwork import Server
import src.Structs.Constants as const

def main():
    s = Parser("res\\savedFile_162649.txt")
    geo = s.getTrimeshGeo
    sceneProcessor = SceneProcessor(geo)
    oscNetwork = OscNetwork(sceneProcessor)
    tcpNetwork = Server("192.168.1.214", 8050)
    #creatserver = Server()

if __name__ == '__main__':
    main()