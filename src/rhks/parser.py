import xml.dom.minidom
from components import *
import log

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
    

def parseKickstart( node ):
    if node.localName == 'kickstart':
        ks = Kickstart( node.attributes["name"].value )
        for cmdNode in node.getElementsByTagName( "command" ):
            parseCommands( ks, cmdNode )
        return ks
    else:
        return None

def parseCommands( ks, node ):
    for childNode in node.childNodes:
        if childNode.nodeType == childNode.ELEMENT_NODE:
            command = parseCommand( childNode )
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
    

