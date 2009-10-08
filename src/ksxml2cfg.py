import getopt,sys,os
from rhks import parser,components,log
from rhks.error import *

def print_usage( ):
	print """usage: ksxml2cfg  [OPTIONS] [FILE]
[OPTIONS] are:
-h, --help              print this help information
-v, --version           print version
-o, --out=[FILE]        output file
"""

def build( kickstart, filename ):
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

        inFile = args[0]
	try:
		ks = parser.parseKickstartXmlSource( inFile )
	except DuplicationError , e:
		log.print_error( e.msg )
		sys.exit(1)
        ks.srcDir= getAbsDir( inFile )

        if outFile == None:
                outFile = ks.srcDir + "/" + ks.name + ".cfg"
	build(ks, outFile )

if __name__ == "__main__":
	main()
