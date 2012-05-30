import os
import sys

class AQTimeHandler:
    def __init__(self):
        pass

    def execute(self):
        try:
            os.system("AQTimeScript.vbs")
            
        except Exception, e:
            print "Error on launching executable, ", e

if __name__ == "__main__":
    a = AQTimeHandler()
    a.execute()
