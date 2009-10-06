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
        for pkgsNode in node.getElementsByTagName( "packages" ):
            ks.setPackages( parsePackages( pkgsNode ) )
 
        return ks
    else:
        return None

def parseCommands( ks, node ):
    for childNode in node.childNodes:
        if childNode.nodeType == childNode.ELEMENT_NODE:
            command = parseCommand( childNode )
            ks.addCommand( command )

def parseDirectiveOptions( directive, node ):
    for attrName in node.attributes.keys():
        directive.addOption( attrName, node.attributes[ attrName ].value )

def parsePackages( node ):
    packages = Packages()
    parseDirectiveOptions( packages, node )
    for groupNode in node.getElementsByTagName( "group" ):
        packages.addGroup( getNodeText( groupNode ) )
    for pkgNode in node.getElementsByTagName( "addpackage" ):
        packages.addPkg( getNodeText( pkgNode ) )
    for pkgNode in node.getElementsByTagName( "rmpackage" ):
        packages.deletePkg( getNodeText( pkgNode ) )
    return packages

def parseCommand( node ):
    command = Command( node.localName )
    command.value = getNodeText( node )
    parseDirectiveOptions( command, node )
    return command

def parseKickstartXmlSource( filename ):
    doc = xml.dom.minidom.parse( filename )
    return parseKickstart( doc.documentElement )
    

