import datetime
import os
import sys
import getopt

from xml.dom import minidom as xd

from matplotlib.pyplot import figure, show
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange

"""
try:
    from qa import mafPath
except ImportError:
    import mafPath
"""
currentPathScript = os.path.split(os.path.realpath(__file__))[0]
#modulesDir = mafPath.mafSourcesDir
#outputDir = mafPath.mafQADir


def parseData():
    root = os.path.join("/home/guestadmin/workspace/QAResults");
    resultFiles = []
    # walk on the filesystem listing xml files in an array of full paths
    for oDirPaths, oDirNames, oFiles in os.walk( root, True, None ):
        for file in oFiles:
            extension = file.split(".")[-1]
            path = oDirPaths.split("/")[-1]
            if(extension == "xml" and path == "xml"):
                resultFiles.append( os.path.join(oDirPaths,file) )
    
    #print "\n".join(resultFiles)
    # parse each file, retrieving information
    for item in resultFiles:
        day = None
        rule = None
        value = -1
        #get the day
        day = item.split("/")[-3][:-8]
        #get the rule
        rule = item.split("/")[-1][:-4]
        #get the value
        dom = xd.parse(item)
        if("Coverage" in rule):
            value = dom.getElementsByTagName('root')[0].getElementsByTagName('results')[0].getElementsByTagName('percentage')[0].firstChild.nodeValue
        else:
            value = dom.getElementsByTagName('root')[0].getElementsByTagName('results')[0].getElementsByTagName('percentageCoverage')[0].firstChild.nodeValue
        
        print day, rule, value[-3:]
    # save in a dictionary with keys made by rules, and values the final result
    
    # graph data
    pass

def drawGraph():
    date1 = datetime.datetime( 2000, 3, 2)
    date2 = datetime.datetime( 2000, 3, 6)
    delta = datetime.timedelta(hours=6)
    dates = drange(date1, date2, delta)

    y = arange( len(dates)*1.0)

    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, y*y, '-')

    # this is superfluous, since the autoscaler should get it right, but
    # use date2num and num2date to to convert between dates and floats if
    # you want; both date2num and num2date convert an instance or sequence
    ax.set_xlim( dates[0], dates[-1] )

    # The hour locator takes the hour or sequence of hours you want to
    # tick, not the base multiple

    ax.xaxis.set_major_locator( DayLocator() )
    ax.xaxis.set_minor_locator( HourLocator(arange(0,25,6)) )
    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )

    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate()

    fig.savefig('test1.png', dpi=300)

def run(param):
    parseData()
    drawGraph()

def usage():
    print "Usage: python drawGraphs.py [-h]"
    print "-h, --help                    show help (this)"
    print 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        else:
            assert False, "unhandled option"

    param = {}
    run(param)
    
if __name__ == "__main__":
  main()
