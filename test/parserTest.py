from rhks.components import *
from rhks.parser import *
import unittest
import xml.dom.minidom
import os

class parserTest(unittest.TestCase):

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
        self.assertEquals( len(ks.commands), 1 )
        command = ks.commands[0]
        self.assertEquals( command.name, "lang" )

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

    def testParseKickstart( self ):
        node = self.createNode( "<kickstart name='test'></kickstart>" )
        ks = parseKickstart( node )
        self.assertEquals( ks.name, "test" )

    def testParseKickstartWithCommands( self ):
        node = self.createNode( self.ksXmlWithCommand )
        ks = parseKickstart( node )
        self.assertCommandInKickstartParse( ks )

    def testParseKickstartWithPackages( self ):
        node = self.createNode( self.ksXmlWithPackages )
        ks = parseKickstart( node )
        self.assertPackages( ks.packages )
        
    def testParseKickstartXmlSource( self ):
        ks = self.parseKickstartFromXmlSource( self.ksXmlWithCommand )
        self.assertCommandInKickstartParse( ks )
        ks = self.parseKickstartFromXmlSource( self.ksXmlWithPackages )
        self.assertPackages( ks.packages )

    def parseKickstartFromXmlSource( self, xmldata ):
        file = open( "test.xml", "w" )
        file.write( xmldata )
        file.close()
        ks = parseKickstartXmlSource( "test.xml" )
        os.remove( "test.xml" )
        return ks

    def assertCommandInKickstartParse( self, ks ):

        self.assertEquals( len( ks.commands ), 1 )
        command = ks.commands[0]
        self.assertEquals( command.name, "lang" )
        self.assertEquals( command.value, "us" )

    def assertPackages( self, packages ):
        self.assertEquals( packages.options[ "resolvedeps" ], "yes" )
        self.assertEquals( packages.groups[0], "base" )
        self.assertEquals( packages.addpkgs[0], "gcc" )
        self.assertEquals( packages.rmpkgs[0], "ftp" )

if __name__ == '__main__':
    unittest.main()
