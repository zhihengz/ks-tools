from rhks.comps import *
from rhksTestBase import *

def createNode( xmlText ):
    doc = xml.dom.minidom.parseString( xmlText )
    return doc.documentElement

class compsTest(TestBase ):

    def assertChildGroupNode( self, node, groupName ):
        for groupNode in getAllGroupChildNodes( node ):
            for idNode in getAllIdChildNodes( groupNode ):
                idName = getNodeText( idNode )
                if idName == groupName:
                    return
        self.fail( "no group " + groupName + " found" )

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

    def testFindEmptyGroupWoId( self ):
        xmldata = """<comps>
<group>
<hello></hello>
</group>
</comps>
"""
        node = createNode( xmldata )
        groups = findAllGroups( node )
        self.assertEquals( len( groups ), 0 )   

    def testFindSingleGroupWithMultipleIds( self ):
        xmldata = """<comps>
<group>
<id>foo</id>
<id>bar</id>
</group>
</comps>
"""
        node = createNode( xmldata )
        groups = findAllGroups( node )
        self.assertEquals( len( groups ), 1 )

    def testFindSingleGroupWithSingleId( self ):
        xmldata = """<comps>
<group>
<id>foo</id>
</group>
</comps>
"""
        node = createNode( xmldata )
        groups = findAllGroups( node )
        self.assertOnlyItemInSet( "foo", groups )

    def testFindSingleGroupWithDuplicateGroupName( self ):
        xmldata = """<comps>
<group>
<id>foo</id>
</group>
<group>
<id>foo</id>
</group>
</comps>
"""
        node = createNode( xmldata )
        groups = findAllGroups( node )
        self.assertOnlyItemInSet( "foo", groups )

    def testCompsMerge( self ):

        xmldata = """<comps>
<group>
<id>foo</id>
</group>
</comps>
"""
        node = createNode( xmldata )
        compsMerge = CompsMerge( node )
        self.assertChildGroupNode( compsMerge.compsNode, "foo" )
        self.assertOnlyItemInSet( "foo", compsMerge.groups )

    def testMergeComps( self ):

        xmldata1 = """<comps>
<group>
<id>foo</id>
</group>
</comps>
"""     
        xmldata2 = """<comps>
<group>
<id>bar</id>
</group>
</comps>
"""
        compsMerge1 = CompsMerge( createNode( xmldata1 ) )
        compsMerge2 = CompsMerge( createNode( xmldata2 ) )
        compsMerge1.merge( compsMerge2 )
        self.assertEquals( len( compsMerge1.groups ), 2 )
        self.assertTrue( "bar" in compsMerge1.groups )
        self.assertTrue( "foo" in compsMerge1.groups )
        self.assertTrue( "bar" in compsMerge1.groups )
        self.assertChildGroupNode( compsMerge1.compsNode, "bar" )
        self.assertChildGroupNode( compsMerge1.compsNode, "foo" )

    def testMergeDuplicateComps( self ):

        xmldata1 = """<comps>
<group>
<id>foo</id>
</group>
</comps>
"""     
        xmldata2 = """<comps>
<group>
<id>foo</id>
</group>
</comps>
"""
        compsMerge1 = CompsMerge( createNode( xmldata1 ) )
        compsMerge2 = CompsMerge( createNode( xmldata2 ) )
        try:
            compsMerge1.merge( compsMerge2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expect duplication error" )


    def testMergeEmptyGroupComps( self ):

        xmldata1 = """<comps>
</comps>
"""     
        xmldata2 = """<comps>
<group>
<id>foo</id>
</group>
</comps>
"""
        compsMerge1 = CompsMerge( createNode( xmldata1 ) )
        compsMerge2 = CompsMerge( createNode( xmldata2 ) )
        compsMerge1.merge( compsMerge2 )
        self.assertOnlyItemInSet( "foo", compsMerge1.groups )
        self.assertChildGroupNode( compsMerge1.compsNode, "foo" )

        compsMerge1 = CompsMerge( createNode( xmldata1 ) )
        compsMerge2 = CompsMerge( createNode( xmldata2 ) )
        compsMerge2.merge( compsMerge1 )
        self.assertOnlyItemInSet( "foo", compsMerge2.groups )
        self.assertChildGroupNode( compsMerge2.compsNode, "foo" )

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

    def testFoundNothingWithIgnoredSet( self ):
        pkgset=[]
        expectedPkgSet= [ "foo" ]
        ignoredSet = [ "foo" ]
        missed = findMissedPackages( pkgset, expectedPkgSet, ignoredSet )
        self.assertEquals( len( missed ), 0 )

    def testFoundMissedWithIngoredSet( self ):
        pkgset = [ "foo" ]
        expectedPkgSet = [ "foo", "bar" ]
        ignoredSet = [ "foo" ]
        missed = findMissedPackages( pkgset, expectedPkgSet, ignoredSet )
        self.assertOnlyItemInSet( "bar", missed )

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

    def testFindNoPackagesInEmptyGroup( self ):
        comps = Comps( )
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        foundPkgs = comps.findAllPkgsInGroups( [] )
        self.assertEquals( len( foundPkgs ), 0 )

    def testFindNoPackagesInDiffGroup( self ):
        comps = Comps( )
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        foundPkgs = comps.findAllPkgsInGroups( [ "hello" ] )
        self.assertEquals( len( foundPkgs ), 0 )

    def testFindPackagesInGroup( self ):
        comps = Comps( )
        comps.addPackagesInGroup( "bar", [ "foo" ] )
        foundPkgs = comps.findAllPkgsInGroups( [ "bar" ] )
        self.assertOnlyItemInSet( "foo", foundPkgs )

        
if __name__ == '__main__':
    unittest.main()
