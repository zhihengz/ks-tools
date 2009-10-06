#!/usr/bin/python -t
import sys,os
from rhks import parser,components

def print_usage():
	print "usage: ksxml2cfg <xml file>"

def build( kickstart, filename ):
    file = open(filename, "w" )
    for command in kickstart.commands:
        file.write( command.compile() + "\n" )
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
	if len(sys.argv) < 2:
		print_usage()
		sys.exit(1)
        inFile = sys.argv[1]
	ks = parser.parseKickstartXmlSource( inFile )
        ks.srcDir= getAbsDir( inFile )
	build(ks, ks.srcDir + "/" + ks.name + ".cfg" )

if __name__ == "__main__":
	main()
