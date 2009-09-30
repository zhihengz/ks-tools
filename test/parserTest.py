from rhks.components import *
from rhks.parser import *
import unittest
import xml.dom.minidom

class parserTest(unittest.TestCase):

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

    def testParseKickstart( self ):
        node = self.createNode( "<kickstart name='test'></kickstart>" )
        ks = parseKickstart( node )
        self.assertEquals( ks.name, "test" )

    def testParseKickstartWithCommands( self ):
        xmlData = """
<kickstart name="test">
<command>
<lang>us</lang>
</command>
</kickstart>
"""
        node = self.createNode( xmlData )
        ks = parseKickstart( node )
        self.assertEquals( len( ks.commands ), 1 )
        command = ks.commands[0]
        self.assertEquals( command.name, "lang" )
        self.assertEquals( command.value, "us" )

if __name__ == '__main__':
    unittest.main()
