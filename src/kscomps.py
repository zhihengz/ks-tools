import getopt,sys,os
from rhks import comps,log
from rhks.error import *

def print_usage( ):
    print """usage: kscomps  [OPTIONS] [FILE] ...
[OPTIONS] are:
-h, --help              print this help information
-v, --version           print version
-q, --query             query comps file and outpu all packages
-V, --verify=[DIR]      verify comps file against rpm folders
"""

def queryAllPackages( compsFile ):
    mycomps = comps.parseComps( comps.parseCompsXmlNode( compsFile ) )
    for pkg in mycomps.packages.keys():
        print pkg

def verifyAllPackages( compsFile, rpmdir ):
    compsset = comps.parseComps( comps.parseCompsXmlNode( compsFile ) ).packages.keys()
    foundset = comps.getAllRpmTagNamesInDir( rpmdir )
    missedInRpms = comps.findMissedPackages( foundset, compsset )
    noError = False
    noWarning = False

    if len( missedInRpms ) > 0:
        for pkg in missedInRpms:
            log.print_error( "no " + pkg + " rpm found in " + rpmdir )
    else:
        noError = not False
        print "Nothing missed in comps"
    
    missedInComps = comps.findMissedPackages( compsset, foundset )
    if len( missedInComps ) > 0:
        for pkg in missedInComps:
            log.print_warn( "no " + pkg + " rpm found in compsFile" )
    else:
        noWarning = not False
        print "Nothing missed in comps"

    if not noError:
        sys.exit( 1 )


def main():
    version= "1.0.0"
    author="Zhiheng Zhang"
    shortOpts = "hvqV:"
    longOpts = [ "help", "version", "query", "verify=" ]
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
        elif o == "--verify" or o == "-V":
            action = "verify"
            rpmdir=a
            if not os.path.isdir( rpmdir ):
                log.print_error( rpmdir + " is not directory" )
                sys.exit( 1 )

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
    elif action == "verify":
        verifyAllPackages( compsFile, rpmdir )
        
if __name__ == "__main__":
	main()
