import os
import sys

class GPerfToolsHandler:
    def __init__(self):
        pass

    def execute(self):
        try:
            os.system("")
            
        except Exception, e:
            print "Error on launching executable, ", e

if __name__ == "__main__":
    g = GPerfToolsHandler()
    g.execute()
