import xml.dom.minidom
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
def getAllPackages( node ):
    pkgset=[]
    if node.localName == 'comps':
        for pkgreqNode in node.getElementsByTagName( 'packagereq' ):
          pkg = parsePackageReq( pkgreqNode )
          if not pkg in pkgset:
              pkgset.append( pkg )

    return pkgset

def parsePackageReq( node ):
    return getNodeText( node )
        
