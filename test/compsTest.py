from rhks.comps import *
from rhksTestBase import *

def createNode( xmlText ):
    doc = xml.dom.minidom.parseString( xmlText )
    return doc.documentElement

class compsTest(TestBase ):
    def testParseSinglePackage( self ):
        xmldata = """<comps>
<packagereq>foo</packagereq>
</comps>
"""
        node = createNode( xmldata )
        pkgset = getAllPackages( node )
        self.assertOnlyItemInSet( "foo", pkgset )

    def testParseDuplicatedPackages( self ):
        xmldata = """<comps>
<packagereq>foo</packagereq>
<packagereq>foo</packagereq>
</comps>
"""
        node = createNode( xmldata )
        pkgset = getAllPackages( node )
        self.assertOnlyItemInSet( "foo", pkgset )

    def testParseMultiplePackages( self ):
        xmldata = """<comps>
<packagereq>foo</packagereq>
<packagereq>bar</packagereq>
</comps>
"""
        node = createNode( xmldata )
        pkgset = getAllPackages( node )
        self.assertTrue( "foo" in pkgset )
        self.assertTrue( "bar" in pkgset )
        self.assertEquals( len( pkgset), 2 )

    def testFoundNothingInEmptyPkgSet( self ):
        pkgset = []
        expectedPkgSet = []
        missed = findMissedPackages( pkgset, expectedPkgSet )
        self.assertEquals( len( missed ), 0 )

    def testFoundMissedPackage( self ):
        pkgset = []
        expectedPkgSet = ["foo"]
        missed = findMissedPackages( pkgset, expectedPkgSet )
        self.assertTrue( "foo" in missed )

    def testFoundNothingInEmptyExpectedPkgSet( self ):
        pkgset = [ "foo"]
        expectedPkgSet = []
        missed = findMissedPackages( pkgset, expectedPkgSet )
        self.assertEquals( len( missed ), 0 )

if __name__ == '__main__':
    unittest.main()
