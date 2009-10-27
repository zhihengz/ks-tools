from rhks.components import *
from rhks.parser import *
import unittest
import xml.dom.minidom
import os

class parserTest(unittest.TestCase):


    def assertTrue( self, value ):
        """
        back porting assertTrue for python 2.3
        """
        s = super( parserTest, self)
        if hasattr( s, 'assertTrue'):
            s.assertTrue( value )
        else:
            self.assertNotEquals( False, value )

    def assertFalse( self, value ):
        """
        back porting assertFalse for python 2.3
        """
        s = super( parserTest, self)
        if hasattr( s, 'assertFalse'):
            s.assertFalse( value )
        else:
            assertEquals( False, value )

    def setUp( self ):
        self.ksXmlWithCommand =  """
<kickstart name="test">
<command>
<lang>us</lang>
</command>
</kickstart>
"""
        self.ksXmlWithPackages = """
<kickstart name="test">
<packages resolvedeps="yes">
<group>base</group>
<addpackage>gcc</addpackage>
<rmpackage>ftp</rmpackage>
</packages>
</kickstart>
"""
        self.ksXmlWithActions = """
<kickstart name="test">
<pre interpreter="/usr/bin/python">
<include src="test.tmp"/>
</pre>
<post interpreter="/usr/bin/python">
<include src="test.tmp"/>
</post>
</kickstart>
"""
        self.ksXmlWithIncludes = """
<kickstart name="test">
<include>/tmp/network.ks</include>
</kickstart>
"""
    def createNode( self, xmlText ):
        doc = xml.dom.minidom.parseString( xmlText )
        return doc.documentElement

    def testParseCommandWithValue( self ):
        node = self.createNode( "<lang>us</lang>")
        command = parseCommand( node )
        self.assertEquals( command.name, "lang" )
        self.assertEquals( command.value, "us" )

    def testParseCommand( self ):
        node = self.createNode( "<cdrom/>")
        command = parseCommand( node )
        self.assertEquals( command.name, "cdrom" )
        self.assertEquals( command.value, None )

    def testParseCommandWithOption( self ):
        node = self.createNode( "<hello test='yes'>world</hello>")
        command = parseCommand( node )
        self.assertEquals( command.name, "hello" )
        self.assertEquals( command.value, "world" )
        self.assertEquals( command.options["test"], "yes" )

    def testParseCommands( self ):
        node = self.createNode( "<command><lang/></command>")
        ks = Kickstart( "test" )
        parseCommands( ks, node )
        self.assertOnlyItemInSet( Command( "lang" ), ks.commands )

    def testParseIncludes( self ):
        node = self.createNode( "<include>/tmp/network.ks</include>" )
        inc = parseIncludeMacro( node )
        self.assertInclude( inc )

    def testParsePackages( self ):
        xmldata = """<packages resolvedeps="yes">
<group>base</group>
<addpackage>gcc</addpackage>
<rmpackage>ftp</rmpackage>
</packages>
"""
        node = self.createNode( xmldata )
        packages = parsePackages( node )
        self.assertPackages( packages )

    def testParseActionOnly( self ):
        xmldata = """<pre interpreter="/usr/bin/python">
</pre>
"""
        node = self.createNode( xmldata )
        action = parseAction( node )
        self.assertEquals( action.name, "pre" )
        self.assertEquals( action.options[ "interpreter" ],
                           "/usr/bin/python" )

    def testParseActionWithInclude( self ):
        xmldata = """<pre interpreter="/usr/bin/python">
<include src="test.tmp"/>
</pre>
"""
        node = self.createNode( xmldata )
        action = parseAction( node )
        self.assertAction( action, "pre" )

    def testParseKickstart( self ):
        node = self.createNode( "<kickstart name='test'></kickstart>" )
        ks = parseKickstart( node )
        self.assertEquals( ks.name, "test" )

    def testParseNonameKickstart( self ):
        node = self.createNode( "<kickstart></kickstart>" )
        ks = parseKickstart( node )
        self.assertNotEquals( ks, None )

    def testParseKickstartWithCommands( self ):
        node = self.createNode( self.ksXmlWithCommand )
        ks = parseKickstart( node )
        self.assertCommandInKickstartParse( ks )

    def testParseKickstartWithPackages( self ):
        node = self.createNode( self.ksXmlWithPackages )
        ks = parseKickstart( node )
        self.assertPackages( ks.packages )

    def testParseKickstartWithActions( self ):
        node = self.createNode( self.ksXmlWithActions )
        ks = parseKickstart( node )
        self.assertAction( ks.preAction, "pre" )
        self.assertAction( ks.postActions[0], "post" )

    def testParseKickstartWithIncludes( self ):
        node = self.createNode( self.ksXmlWithIncludes )
        ks= parseKickstart( node )
        self.assertEquals( len( ks.includes ), 1 )
        self.assertIncludes( ks.includes )

    def testParseKickstartWithMultipleDepthIncludes( self ): 
        xmldata = """
<kickstart name="test">
<include>/tmp/network.ks</include>
<pre>
<include src="test"/>
</pre>
</kickstart>
"""
        node = self.createNode( xmldata )
        ks= parseKickstart( node )
        self.assertEquals( len( ks.includes ), 1 )
        self.assertIncludes( ks.includes )

    def testParseKickstartXmlSource( self ):
        ks = self.parseKickstartFromXmlSource( self.ksXmlWithCommand )
        self.assertCommandInKickstartParse( ks )
        ks = self.parseKickstartFromXmlSource( self.ksXmlWithPackages )
        self.assertPackages( ks.packages )
        ks = self.parseKickstartFromXmlSource( self.ksXmlWithActions )
        self.assertAction( ks.preAction, "pre" )
        self.assertAction( ks.postActions[0], "post" )
        ks = self.parseKickstartFromXmlSource( self.ksXmlWithIncludes )
        self.assertIncludes( ks.includes )
    def parseKickstartFromXmlSource( self, xmldata ):
        file = open( "test.xml", "w" )
        file.write( xmldata )
        file.close()
        ks = parseKickstartXmlSource( "test.xml" )
        os.remove( "test.xml" )
        return ks

    def assertCommandInKickstartParse( self, ks ):

        expected = Command( "lang" )
        expected.value = "us"
        self.assertOnlyItemInSet( expected, ks.commands )

    def assertPackages( self, packages ):
        self.assertEquals( packages.options[ "resolvedeps" ], "yes" )
        self.assertTrue( "base" in packages.groups )
        self.assertTrue( "gcc" in packages.addpkgs )
        self.assertTrue( "ftp" in packages.rmpkgs )

    def assertAction( self, action, name ):
        self.assertEquals( action.name, name )
        self.assertEquals( action.options[ "interpreter" ],
                           "/usr/bin/python" )
        self.assertOnlyItemInSet( "test.tmp", action.includes )
        
    def assertInclude( self, include ):
        self.assertEquals( include.value, "/tmp/network.ks" )

    def assertIncludes( self, includeSet ):
        inc = IncludeMacro()
        inc.value = "/tmp/network.ks"
        self.assertOnlyItemInSet( inc, includeSet )

    def assertOnlyItemInSet( self, item, itemSet ):
        self.assertEquals( len( itemSet ), 1 )
        self.assertTrue( item in itemSet )

if __name__ == '__main__':
    unittest.main()
