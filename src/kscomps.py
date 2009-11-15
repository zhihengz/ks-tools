import getopt,sys,os
from rhks import comps,log
from rhks.error import *

def print_usage( ):
    print """usage: kscomps  [OPTIONS] [FILE] ...
[OPTIONS] are:
-h, --help                print this help information
-v, --version             print version
-q, --query               query comps file and outpu all packages
-V, --verify=[DIR]        verify comps file against rpm folders
-i, --ignore-[GROUP]      ignore package missing in group of GROUP
-m, --merge               merge multiple comps files, default output is comps.xml
                          in working path
-o, --out=[FILE]          output file of merged comps
"""

def mergeComps( compsFiles, outfile ):
    compsMergeList = []
    for compsFile in compsFiles:
        compsMergeList.append( comps.parseCompsMerge( comps.parseCompsXmlNode( compsFile ) ) )
    result = compsMergeList[0]
    for i in range( 1, len( compsMergeList ) ):
        try:
            result.merge( compsMergeList[i] )
        except DuplicationError, e:
            log.print_error( e.msg + " in " + compsFiles[ i ] )
            sys.exit( 1 )

    result.output( outfile )

def queryAllPackages( compsFile, ignoredGroups ):
    mycomps = comps.parseComps( comps.parseCompsXmlNode( compsFile ) )
    ignoredpkgs = mycomps.findAllPkgsInGroups( ignoredGroups )
    for pkg in mycomps.packages.keys():
        if not pkg in ignoredpkgs:
            print pkg

def verifyAllPackages( compsFile, rpmdir, ignoredGroups ):
    mycomps = comps.parseComps( comps.parseCompsXmlNode( compsFile ) )
    compsset = mycomps.packages.keys()
    foundset = comps.getAllRpmTagNamesInDir( rpmdir )
    ignoredset = mycomps.findAllPkgsInGroups( ignoredGroups )
    missedInRpms = comps.findMissedPackages( foundset, compsset, ignoredset )
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
    shortOpts = "hvqV:i:mo:"
    longOpts = [ "help", "version", "query", "verify=", "ignore=", "merge", "out=" ]
    try:
        opts, args = getopt.getopt( sys.argv[1:], 
                                    shortOpts,
                                    longOpts )
    except getopt.GetoptError:
        log.print_error( "non-recognized command line arguments" )
        print_usage( )
        sys.exit( 1 )
        
    action = None
    ignoredGroups = []
    outfile="comps.xml"
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
        elif o == "--ignore" or o == "-i":
            if not a in ignoredGroups:
                ignoredGroups.append( a )
        elif o in ( "-m", "--merge" ):
            action = "merge"
        elif o in ( "-o", "--out" ):
            outfile = a
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
        queryAllPackages( compsFile, ignoredGroups )
    elif action == "verify":
        verifyAllPackages( compsFile, rpmdir, ignoredGroups )
    elif action == "merge":
        mergeComps( args, outfile )

if __name__ == "__main__":
	main()
