import xml.dom.minidom

def parseKickstartNode( node ):
    ks = Kickstart( "demo")
    parseCommands( ks, node )
    return ks

def parseCommands( ks, node ):
    command = parseCommand( node )
    ks.addCommand( command )
    
def parseCommand( node ):
    command = Command( "mockCommand" )
    return command

def parseKickstartXmlSource( filename ):
    doc = xml.dom.minidom.parse( filename )
    return parseKickstart( doc.documentElement )
    

