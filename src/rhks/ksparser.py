from components import *
from parser import *

def build( kickstart, filename ):
    file = open(filename, "w" )
    for command in kickstart.commands:
        file.writelines( command.compile() )
    file.close

def parse( ksXmlFile ):
    ks = parseKickstartXmlSource( ksXmlFile )
    build( ks, ks.name + ".cfg" )
