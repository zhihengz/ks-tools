import xml.dom.minidom
from components import *

def getNodeText( aNode):
    """get node text
    
    Arguments:
    - `aNode`:
    """
    if aNode.nodeType == aNode.TEXT_NODE:
        return aNode.nodeValue
    if aNode.nodeType == aNode.ELEMENT_NODE:
        for childNode in aNode.childNodes:
            childNodeText = getNodeText( childNode )
            if not childNodeText == None:
                return childNodeText

    return None
    

def parseKickstartNode( node ):
    ks = Kickstart( "demo")
    parseCommands( ks, node )
    return ks

def parseCommands( ks, node ):
    command = parseCommand( node )
    ks.addCommand( command )
    
def parseCommand( node ):
    command = Command( node.localName )
    command.value = getNodeText( node )
    for attrName in node.attributes.keys():
        command.addOption( attrName, node.attributes[ attrName ].value )
    return command

def parseKickstartXmlSource( filename ):
    doc = xml.dom.minidom.parse( filename )
    return parseKickstart( doc.documentElement )
    

