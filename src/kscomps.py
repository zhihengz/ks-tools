import getopt,sys,os
from rhks import comps,log
from rhks.error import *

def print_usage( ):
    print """usage: kscomps  [OPTIONS] [FILE] ...
[OPTIONS] are:
-h, --help              print this help information
-v, --version           print version
-q, --query             query comps file and outpu all packages
"""

def queryAllPackages( compsFile ):
    for pkg in comps.getAllPackages( comps.parseCompsXmlNode( compsFile ) ):
        print pkg
def main():
    version= "1.0.0"
    author="Zhiheng Zhang"
    shortOpts = "hvq"
    longOpts = [ "help", "version", "query" ]
    try:
        opts, args = getopt.getopt( sys.argv[1:], 
                                    shortOpts,
                                    longOpts )
    except getopt.GetoptError:
        log.print_error( "non-recognized command line arguments" )
        print_usage( )
        sys.exit( 1 )
        
    action = None
    for o, a in opts:
        if o == "--help" or o == "-h":
            print_usage()
            sys.exit( 0 )
        elif o == "--version" or o == "-v":
            print "kscomps version " + version + " by " + author
            sys.exit(0 )
        elif o == "--query" or o == "-q":
            action = "query"

    if action == None:
        log.print_error( "no action asked" )
        print_usage()
        sys.exit(1)

    if len( args ) < 1:
        log.print_error( "no comps file" )
        print_usage( )
        sys.exit( 1 )
    
    compsFile = args[0]

    if action == "query":
        queryAllPackages( compsFile )

if __name__ == "__main__":
	main()
