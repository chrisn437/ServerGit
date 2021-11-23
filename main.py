#!/usr/bin/bash



# Example input variables
from src.project.oscNetwork import OscNetwork
from src.project.parser import Parser
from src.project.sceneProcessor import SceneProcessor
from src.project.tcpNetwork import TcpNetwork
from src.project.tcpNetwork import Server

def main():
    #oscNetwork = OscNetwork()
    tcpNetwork = Server("192.168.1.214", 8050)
    creatserver = Server()

if __name__ == '__main__':
    main()