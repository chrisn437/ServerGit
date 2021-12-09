#from src.project.oscNetwork import OscNetwork
#import matplotlib.pylab as plt

class UserPosTracking():
    def __init__(self, x, y, t):

        self.scatter(x, y)


    def scatter(self, xpos, ypos):
        for x in xpos:
            plt.scatter(xpos[x], ypos[x])
            plt.hold(True)
        plt.show()
