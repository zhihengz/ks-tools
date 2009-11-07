import xml.dom.minidom
import log
import os, rpm

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
    if node.localName == 'comps':
        for pkgreqNode in node.getElementsByTagName( 'packagereq' ):
          pkg = parsePackageReq( pkgreqNode )
          if not pkg in pkgset:
              pkgset.append( pkg )

    return pkgset

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

def findMissedPackages( pkgSet, expectedPkgSet ):
    missed = []
    for pkg in expectedPkgSet:
        if not pkg in pkgSet:
            missed.append( pkg )
    return missed


