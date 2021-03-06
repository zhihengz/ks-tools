import xml.dom.minidom
import log
import os, rpm
from error import *

def formatList( aList ):
    ret="["
    for item in aList:
        ret += item + ", "
    ret += "]"
    return ret

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
def getAllPackages( node ):
    pkgset=[]
    for pkgreqNode in node.getElementsByTagName( 'packagereq' ):
        pkg = parsePackageReq( pkgreqNode )
        if not pkg in pkgset:
            pkgset.append( pkg )
            
    return pkgset

def getAllGroupChildNodes( node ):
    return [ e for e in node.childNodes if e.nodeType == e.ELEMENT_NODE and e.localName == "group" ]

def parseComps( node ):
    comps = Comps()
    if node.localName == 'comps':
        for groupNode in getAllGroupChildNodes( node ):
            parsePackagesInGroupNode( groupNode, comps )

    return comps

def getAllIdChildNodes( node ):
   
    return [ e for e in node.childNodes if e.nodeType == e.ELEMENT_NODE and e.localName == "id" ]

def parsePackagesInGroupNode( node, comps ):
    
    pkgs = getAllPackages( node )
    idNodes = getAllIdChildNodes( node )
    if len ( idNodes ) == 0:
        log.print_warn( "no group id found for " + formatList( pkgs ) )
    else:
        groupName = getNodeText( idNodes[0] )
        if len( idNodes ) > 1:
            log.print_warn( "multiple group ids found for " + formatList( pkgs ) )
        comps.addPackagesInGroup( groupName, pkgs )        

def parseCompsXmlNode( filename ):
    doc = xml.dom.minidom.parse( filename )
    return doc.documentElement

def parsePackageReq( node ):
    return getNodeText( node )

def getRpmTagName( ts, rpmFile ):
    fdno = os.open( rpmFile, os.O_RDONLY)
    hdr = ts.hdrFromFdno( fdno )
    os.close( fdno )
    return hdr[ rpm.RPMTAG_NAME ]

def getAllRpmTagNamesInDir( dirname ):
    ts = rpm.TransactionSet()
    ts.setVSFlags( rpm._RPMVSF_NOSIGNATURES )
    rpmtagset=[]
    for f in os.listdir( dirname ):
        if os.path.isfile( os.path.join( dirname, f ) ) and f.endswith( "rpm" ):
            rpmtag = getRpmTagName( ts, os.path.join( dirname, f ) )
            if not rpmtag in rpmtagset:
                rpmtagset.append( rpmtag )
    return rpmtagset

def findMissedPackages( pkgSet, expectedPkgSet, ignoredSet=[] ):
    missed = []
    for pkg in expectedPkgSet:
        if ( not pkg in pkgSet ) and ( not pkg in ignoredSet ):
            missed.append( pkg )
    return missed

def findAllGroups( node ):
    groups = []
    for groupNode in getAllGroupChildNodes( node ):
        idNodes = getAllIdChildNodes( groupNode )
        if idNodes == None or len( idNodes ) == 0 :
            log.print_warn( "no group id found" )
        else:
            groupName = getNodeText( idNodes[0] )
            if not groupName in groups:
                groups.append( groupName )
            else:
                log.print_warn( "duplicated group name found for " + groupName )
            if len( idNodes ) > 1:
                log.print_warn( "multiple group ids found for %s" %(groupName ) )
    return groups

class Comps :
    def __init__(self):
        self.groups = {}
        self.packages = {}

    def addPackagesInGroup( self, group, packages ):
        if self.groups.has_key( group ):
            existedPackages = self.groups[ group ]
            for package in packages:
                if not package in existedPackages:
                    existedPackages.append( package )
        else:
            self.groups[ group ] = packages

        for package in packages:
            if self.packages.has_key( package ):
                existedGroups = self.packages[ package ]
                if not group in existedGroups:
                    existedGroups.append( group )
            else:
                self.packages[ package ] = [group]
        

    def findAllPkgsInGroups( self, groupNames ):
        pkgset = []
        for group in groupNames:
            if self.groups.has_key( group ):
                pkgsInGroup = self.groups [ group ]
                for pkg in pkgsInGroup:
                    if not pkg in pkgset:
                        pkgset.append( pkg )
        return pkgset

def parseCompsMerge( node ):
    if node.localName == 'comps':
        return CompsMerge( node )
    return None

class CompsMerge :
    def __init__(self, compsNode):
        self.compsNode = compsNode
        self.groups = findAllGroups( self.compsNode )

    def merge( self, aComps ):
        for group in aComps.groups:
            if not group in self.groups:
                self.groups.append( group )
            else:
                raise DuplicationError( "group %s is duplicated" %(group))
        
        for groupNode in getAllGroupChildNodes( aComps.compsNode ):
            self.compsNode.appendChild( groupNode )

    def output( self, outfile ):
        file = open( outfile, "w" )
        doc = xml.dom.minidom.Document( )
        doc.appendChild( self.compsNode )
        file.writelines( doc.toxml( ).encode('UTF-8') )
        file.close()
