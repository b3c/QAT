import os
import sys
import getopt
import shutil

try:
    from qa import mafPath
except ImportError:
    import mafPath

currentPathScript = os.path.split(os.path.realpath(__file__))[0]
modulesDir = mafPath.mafSourcesDir
outputDir = mafPath.mafQADir

def run(param):
    scriptsDir = currentPathScript
    f = None
    try:
        f = open("TestListQA.txt")
    except:
        print "QA FAILED"
        print "Probem open TestListQA.txt"

    lines = f.readlines()
    python = "python "

    suffix = "QA.py"
    fileSuffix = "FilePattern.ini"

    resultDir = os.path.abspath(os.path.join(outputDir, "QAResults" , "xml"))
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)

    tempDir = os.path.join(outputDir , "Temp")
    #destroy and create temporary directory for Rules operations
    if  os.path.exists(tempDir):
        shutil.rmtree(tempDir)
    os.makedirs(tempDir)

    for line in lines:
        line = line.replace("\r", "").replace("\n", "")
        ruleGroup = line.replace(suffix,"")

        print "QA Running...", ruleGroup

        filePattern = ruleGroup + fileSuffix
  
        rulesFile = os.path.join(currentPathScript, "Rules", filePattern)
        r = open(rulesFile)
        linesRule = r.readlines()
        #  print linesRule
  
        sourceDir = eval(str(linesRule[1]).rsplit("=")[1])
  
        command = python + line + " " + sourceDir + " " + resultDir + "/"
        print command
        os.system(command.replace("\"","").replace("\r", "").replace("\n", ""))

    print "QA SUCCESSFUL"


    if(param['coverage']):
        baseDir = modulesDir
        externalScriptFile = os.path.join(currentPathScript, "ExternalScripts", "coverageScript.py")

        for item in os.listdir(baseDir):
            if (os.path.isfile(os.path.join(baseDir, item))==False):
                if(item.find("maf") != -1):
                    os.system("python " + externalScriptFile + " " + item)
    if(param['cppcheck']):
        baseDir = modulesDir
        externalScriptFile = os.path.join(currentPathScript, "ExternalScripts", "cppcheckScript.py")
        print baseDir
        os.system("python " + externalScriptFile)
    if(param['cccc']):
        baseDir = modulesDir
        externalScriptFile = os.path.join(currentPathScript, "ExternalScripts", "ccccScript.py")
        for item in os.listdir(baseDir):
            if (os.path.isfile(os.path.join(baseDir, item))==False):
                if(item.find("maf") != -1):
                    os.system("python " + externalScriptFile + " -m " + item)
    if(param['memory-profiling']):
        baseDir = modulesDir
        externalScriptFile = os.path.join(currentPathScript, "ExternalScripts", "memoryProfilingScript.py")
        print baseDir
        #os.system("python " + externalScriptFile)      
        
def usage():
    print "Usage: python ScriptLauncher.py [-h] [-l] [-c] [-M]"
    print "-h, --help                     show help (this)"
    print "-l, --enable-coverage          enable coverage"
    print "-c, --enable-cppcheck          enable cppcheck tool"
    print "-C, --enable-cccc              enable cccc tool: conditional complexity"
    print "-M, --enable-memory-profiling  enable memory profiler tool"
    print 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlcCM", ["help","enable-coverage","enable-cppcheck","enable-cccc", "enable-memory-profiling"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    param = {'coverage':False, 'cppcheck':False, 'cccc':False, 'memory-profiling' : False}
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        elif o in ("-l", "--enable-coverage"):
            param['coverage'] = True
        elif o in ("-c", "--enable-cppcheck"):
            param['cppcheck'] = True
        elif o in ("-C", "--enable-cccc"):
            param['cccc'] = True
        elif o in ("-M", "--enable-memory-profiling"):
            param['memory-profiling'] = True
        else:
            assert False, "unhandled option"

    run(param)
    
if __name__ == "__main__":
  main()
