#!/usr/bin/python -t
import sys,os
from rhks import parser,components

def print_usage():
	print "usage: ksxml2cfg <xml file>"

def build( kickstart, filename ):
    file = open(filename, "w" )
    for command in kickstart.commands:
        file.write( command.compile() + "\n" )
    file.close

def main():
	if len(sys.argv) < 2:
		print_usage()
		sys.exit(1)
        inFile = sys.argv[1]
	ks = parser.parseKickstartXmlSource( inFile )
	build(ks, os.path.dirname( inFile ) + "/" + ks.name + ".cfg" )

if __name__ == "__main__":
	main()
