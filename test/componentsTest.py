from rhks.components import *
import unittest

class componentsTest(unittest.TestCase):
    def testCompileNameOnlyCommand(self):
        command = Command( "hello" )
        self.assertEqual( command.compile(), "hello")
        
    def testCompileCommandWithValue(self):
        command = Command( "hello" )
        command.value = "world"
        self.assertEquals( command.compile(), "hello world")

    def testCompileCommandWithOption(self):
        command = Command( "hello" )
        command.addOption( "config", "test.conf")
        self.assertEquals( command.compile(), "hello --config test.conf")

    def testCompileCommandWithOptions(self):
        command = Command( "hello" )
        command.addOption( "config", "test.conf")
        command.addOption( "out", "test.out")
        self.assertEquals( command.compile(), 
                           "hello --config test.conf --out test.out")

    def testCompileCommandWithFlatOption( self ):
        command = Command( "hello" )
        command.addOption( "debug", "yes" )
        self.assertEquals( command.compile(), "hello --debug" )
        command = Command( "hello" )
        command.addOption( "debug", "no" )
        self.assertEquals( command.compile(), "hello" )

    def testCompileCommandWithSpaceEscape( self ):
        command = Command( "hello" )
        command.addOption( "name", "hello world" )
        self.assertEquals( command.compile(), "hello --name \"hello world\"" )

    def testAddPkgGroup(self):
        packages = Packages()
        packages.addGroup( "group_a" )
        self.assertEquals( packages.groups[0], "group_a" )

    def testAddPkg(self):
        packages = Packages()
        packages.addPkg( "pkg_a" )
        self.assertEquals( packages.addpkgs[0], "pkg_a" )

    def testDeletePkg(self):
        packages = Packages()
        packages.deletePkg( "pkg_a" )
        self.assertEquals( packages.rmpkgs[0], "pkg_a" )

if __name__ == '__main__':
    unittest.main()
