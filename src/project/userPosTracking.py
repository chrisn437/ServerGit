#from src.project.oscNetwork import OscNetwork
#import matplotlib.pylab as plt
import re

class UserPosTracking():
    def __init__(self):
        f = open("res\\PositionLog_133554.txt", "r")
        lines = f.readlines()
        for i in range(100):
            lines1 = lines[i]

            text_in_brackets = re.findall('\d.\d\d\d\d\d\d\d\d', lines1)





        print(text_in_brackets[0])

        f.close()

