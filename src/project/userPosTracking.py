#from src.project.oscNetwork import OscNetwork
#import matplotlib.pylab as plt
import re
import matplotlib.pyplot as plt
import numpy as np

class UserPosTracking():
    def __init__(self):
        f = open("res\\PositionLog_155724.txt", "r")
        lines = f.readlines()
        # find every position digit in the document

        self.positions = lines
        self.title = []
        self.positions = [item.split() for item in self.positions]
        length = len(self.positions)
        self.x :list = []
        self.y :list = []
        self.z :list = []
        self.time :list = []


        self.title = self.positions[0]
        #get only the elemts which correspond to the x-value/achse
        for i in range(1, len(self.positions), 2):
            self.time.append(self.positions[i][0])
            self.x.append(self.positions[i][1])
            self.y.append(self.positions[i][2])
            self.z.append(self.positions[i][3])




        # Converting the Strings in the list to floats
        self.x = [item.replace("(", "") for item in self.x]
        self.x = [item.replace("'", "") for item in self.x]
        self.x = [item.replace(",", "") for item in self.x]
        self.x = [float(i) for i in self.x]
        print(self.x.__len__())
        self.y = [item.replace("(", "") for item in self.y]
        self.y = [item.replace("'", "") for item in self.y]
        self.y = [item.replace(",", "") for item in self.y]
        self.y = [float(i) for i in self.y]
        print(self.y.__len__())
        self.z = [item.replace(")", "") for item in self.z]
        self.z = [item.replace("'", "") for item in self.z]
        self.z = [item.replace(",", "") for item in self.z]
        self.z = [float(i) for i in self.z]
        print(self.z.__len__())

        self.time = [item.replace(":", "") for item in self.time]
        self.time = [float(i) for i in self.time]

        self.totaltime = self.time[-1] - self.time[0]
        # Calculating from X.Y minutes into X minutes and Y seconds


        plt.scatter(self.x, self.z)
        plt.title("Person number: {0}. \n\nTotal time taken {1} seconds".format(self.title, self.totaltime))
        plt.ylabel('x coordinats of the test-subject')
        plt.xlabel('Z coordinats of the test-subject')
        plt.show()

        f.close()

