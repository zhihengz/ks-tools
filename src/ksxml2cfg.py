import getopt,sys,os
from rhks import parser,components,log
from rhks.error import *

def print_usage( ):
	print """usage: ksxml2cfg  [OPTIONS] [FILE] ...
[OPTIONS] are:
-h, --help              print this help information
-v, --version           print version
-o, --out=[FILE]        output file
"""

def output( kickstart, filename ):
    file = open(filename, "w" )
    for command in kickstart.commands:
	    file.write( command.compile() + "\n" )
    for includeMacro in kickstart.includes:
	    file.write( includeMacro.compile() )
    if not kickstart.packages == None :
            file.writelines( kickstart.packages.compile() )
    if not kickstart.preAction == None :
            file.writelines( kickstart.preAction.compile( kickstart.srcDir ) )
    if not kickstart.postAction == None :
            file.writelines( kickstart.postAction.compile( kickstart.srcDir ) )
    file.close

def getAbsDir( fileName ):
        dirname = os.path.dirname( fileName )
        return os.path.abspath( dirname )

def parseOneFile( fileName ):
  	try:
		ks = parser.parseKickstartXmlSource( fileName )
	except DuplicationError , e:
		log.print_error( e.msg )
		sys.exit(1)
        ks.srcDir= getAbsDir( fileName )
        return ks

def mergeKickstart( ksList, args ):
        head = ksList[0]

        for i in range( 1, len(ksList) ):
                try:
                        head.merge( ksList[i] )
                except DuplicationError, e:
                        log.print_error( e.msg + " in " + args[i])
                        sys.exit( 1 )
                        
        return head
def main():
        version= "1.0.0"
        author="Zhiheng Zhang"
        shortOpts = "hvo:"
        longOpts = [ "help", "version", "out=" ]
        outFile = None
        try:
                opts, args = getopt.getopt( sys.argv[1:], 
                                            shortOpts,
                                            longOpts )
        except getopt.GetoptError:
                log.print_error( "non-recognized command line arguments" )
                print_usage( )
                sys.exit( 1 )

        for o, a in opts:
                if o == "--help" or o == "-h":
                        print_usage()
                        sys.exit( 0 )
                elif o == "--version" or o == "-v":
                        print "ksxml2cfg version " + version + " by " + author
                        sys.exit(0 )
                elif o == "--out" or o == "-o":
                        outFile = a
        if len( args ) < 1:
                log.print_error( "no input file" )
                print_usage( 1 )
                sys.exit( 1 )

        ksList = []
        for inFile in args:
                ks = parseOneFile( inFile )
                ksList.append( ks )

        head =ksList[0]
        if outFile == None:
                outFile = head.srcDir + "/" + head.name + ".cfg"

        finalKs = mergeKickstart( ksList, args )
	output( finalKs, outFile )

if __name__ == "__main__":
	main()
