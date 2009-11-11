from rhks.comps import *
from rhksTestBase import *

def createNode( xmlText ):
    doc = xml.dom.minidom.parseString( xmlText )
    return doc.documentElement

class compsTest(TestBase ):
    def testParseSinglePackageInSingeGroup( self ):
        xmldata = """
<group>
<id>bar</id>
<packagereq>foo</packagereq>
</group>
"""
        node = createNode( xmldata )
        comps = Comps()
        parsePackagesInGroupNode( node , comps )
        self.assertOnlyItemInSet( "bar", comps.packages[ "foo" ] )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar" ] )

    def testParseGroupWoId( self ):
        xmldata = """
<group>
<packagereq>foo</packagereq>
</group>
"""
        node = createNode( xmldata )
        comps = Comps()
        parsePackagesInGroupNode( node , comps )
        self.assertEquals( len( comps.packages ), 0 )
        self.assertEquals( len( comps.groups ), 0 )

    def testParseGroupWithMultipleIds( self ):
        xmldata = """
<group>
<id>bar</id>
<id>bar2</id>
<packagereq>foo</packagereq>
</group>
"""
        node = createNode( xmldata )
        comps = Comps()
        parsePackagesInGroupNode( node , comps )
        self.assertEquals( len( comps.packages[ "foo" ] ), 1 )
        self.assertEquals( len( comps.groups ), 1 )

    def testParseCompsWithSingleGroup( self ):
        xmldata = """<comps>
<group>
<id>bar</id>
<packagereq>foo</packagereq>
</group>
</comps>
"""
        node = createNode( xmldata )
        comps = parseComps( node )
        self.assertOnlyItemInSet( "bar", comps.packages[ "foo" ] )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar" ] )

    def testParseCompsWithMultipleGroups( self ):
        xmldata = """<comps>
<group>
<id>bar</id>
<packagereq>foo</packagereq>
</group>
<group>
<id>bar2</id>
<packagereq>foo</packagereq>
</group>
</comps>
"""
        node = createNode( xmldata )
        comps = parseComps( node )
        self.assertTrue( "bar" in comps.packages[ "foo" ] )
        self.assertTrue( "bar2" in comps.packages[ "foo" ] )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar" ] )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar2" ] )

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

    def testAddSinglePackageInSingleGroup( self ):
        comps = Comps()
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        self.assertOnlyItemInSet( "bar", comps.groups.keys() )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar" ] )
        self.assertOnlyItemInSet( "foo", comps.packages.keys() )
        self.assertOnlyItemInSet( "bar", comps.packages [ "foo" ] )

    def testAddPackagesInExistedGroup( self ):
        comps = Comps()
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        comps.addPackagesInGroup( "bar", [ "hello" ] )
        self.assertOnlyItemInSet( "bar", comps.packages[ "hello" ] )
        self.assertOnlyItemInSet( "bar", comps.packages[ "foo" ] )
        self.assertEquals( len( comps.groups[ "bar" ] ), 2 )
        self.assertTrue( "foo" in comps.groups[ "bar" ] )
        self.assertTrue( "hello" in comps.groups[ "bar" ] )

    def testAddDuplicatedPackagesInGroup( self ):
        comps = Comps()
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        self.assertOnlyItemInSet( "bar", comps.groups.keys() )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar" ] )
        self.assertOnlyItemInSet( "foo", comps.packages.keys() )
        self.assertOnlyItemInSet( "bar", comps.packages [ "foo" ] )

    def testAddPackagesInMultipleGroup( self ):
        comps = Comps()
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        comps.addPackagesInGroup( "hello", [ "foo" ] )
        self.assertEquals( len( comps.groups ), 2 )
        self.assertOnlyItemInSet( "foo", comps.groups[ "hello" ] )
        self.assertOnlyItemInSet( "foo", comps.groups[ "bar" ] )
        self.assertOnlyItemInSet( "foo", comps.packages.keys() )
        self.assertEquals( len( comps.packages[ "foo" ] ), 2 )
        self.assertTrue(  "bar" in comps.packages[ "foo" ] )
        self.assertTrue(  "hello" in comps.packages[ "foo" ] )


if __name__ == '__main__':
    unittest.main()
