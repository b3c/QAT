import os
import sys
import getopt
import memoryProfilingScriptAQTime
import memoryProfilingScriptGPerfTool

currentPathScript = os.path.split(os.path.realpath(__file__))[0]

try:
    sys.path.append(os.path.realpath(os.path.join(currentPathScript,"..","..")))
    from qa import mafPath
except ImportError:
    import mafPath

modulesDir = mafPath.mafSourcesDir
qaDir = mafPath.mafQADir

def windowsProfiling():
    obj = memoryProfilingScriptAQTime;
    obj.execute()

def linuxProfiling():
    obj = memoryProfilingScriptAQTime;
    obj.execute()

def osxProfiling():
    obj = memoryProfilingScriptAQTime;
    obj.execute()

def run(param):
    platforms = {
        'win32': windowsProfiling
        'linux': linuxProfiling
        'darwin': osxProfiling
    }
    
    platforms.get(sys.platform, print 'Platform Not Supported')

def usage():
    print "python memoryProfilingScript.py"
    print "-h, --help                 show help (this)"
    print        

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    param = {}
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        else:
            assert False, "unhandled option"
            
    run(param)
    
if __name__ == "__main__":
  main()
