from rhks.components import *
import unittest
import os

tmpFile="test.tmp"
def createTmpFile( data ):
    file = open( tmpFile, "w" )
    file.write(data)
    file.close()
    
class componentsTest(unittest.TestCase):

    def tearDown( self ):
        if os.path.exists( tmpFile ):
            os.remove( tmpFile )

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

    def testCompileIncludeMacro( self ):
        inc = IncludeMacro( )
        inc.value="/tmp/network.ks"
        self.assertEquals( inc.compile(), "%include /tmp/network.ks\n" )

    def testAddPkgGroup(self):
        packages = Packages()
        packages.addGroup( "group_a" )
        self.assertOnlyItemInSet( "group_a", packages.groups )

    def testAddPkg(self):
        packages = Packages()
        packages.addPkg( "pkg_a" )
        self.assertOnlyItemInSet( "pkg_a", packages.addpkgs )

    def testDeletePkg(self):
        packages = Packages()
        packages.deletePkg( "pkg_a" )
        self.assertOnlyItemInSet( "pkg_a", packages.rmpkgs )

    def testCompilePackageGroup(self):
        self.assertEquals( compilePackageGroup( "base" ), "@ base" )

    def testCompileAddPackage(self):
        self.assertEquals( compileAddPackage( "gcc" ), "gcc" )
    
    def testCompileDeletePackage( self ):
        self.assertEquals( compileDeletePackage( "gcc" ), "-gcc" )

    def testCompilePackageWithOption(self):
        packages = Packages()
        packages.addOption( "resolvedeps", "yes" )
        self.assertEquals( packages.compile(), "%packages --resolvedeps\n" )

    def testCompilePackageWithGroupOnly(self):
        packages = Packages()
        packages.addGroup( "base" )
        expected="""%packages
@ base
"""
        self.assertEquals( packages.compile(), expected )

    def testCompilePackageAddOnly(self):
        packages = Packages()
        packages.addPkg( "gcc" )
        expected="""%packages
gcc
"""
        self.assertEquals( packages.compile(), expected )

    def testCompilePackageDeleteOnly(self):
        packages = Packages()
        packages.deletePkg( "gcc" )
        expected="""%packages
-gcc
"""
        self.assertEquals( packages.compile(), expected )

    def testCompilePackageMixed(self):
        packages = Packages()
        packages.addGroup( "base" )
        packages.addGroup( "server" )
        packages.addPkg( "gcc" )
        packages.deletePkg( "ftp" )
        expected="""%packages
@ base
@ server
gcc
-ftp
"""
        self.assertEquals( packages.compile(), expected )

    def testActionInclude(self):
        preAction = Action( "pre" )
        preAction.include( "hello.txt" )
        self.assertOnlyItemInSet( "hello.txt", preAction.includes )

    def testCompileActionOnly( self ):
        preAction = Action( "pre" )
        preAction.addOption( "interpreter", "/usr/bin" )
        self.assertEquals( preAction.compile(), 
                           "%pre --interpreter /usr/bin\n" )

    def testCompileActionWithIncludeBase( self ):
        data ="hello world"
        createTmpFile( data )
        action= Action( "pre" )
        action.include( tmpFile )
        expected="""%pre
hello world
"""
        self.assertEquals( action.compile( os.path.abspath( os.path.dirname( tmpFile ) ) ), 
                           expected )

    def testCompileActionWithInclude( self ):
        data ="hello world"
        createTmpFile( data )
        action= Action( "pre" )
        action.include( tmpFile )
        expected="""%pre
hello world
"""
        self.assertEquals( action.compile(), expected )
   
    def testCompareIncludeMacro( self ):
        inc1 = IncludeMacro()
        inc1.value = "test"
        self.assertFalse( inc1 == None )
        inc2 = IncludeMacro()
        inc2.value = "test"
        self.assertTrue( inc1 == inc2 )
        self.assertEquals( inc2, inc1 )
        inc2.value ="other"
        self.assertFalse( inc1 == inc2 )
        
    def assertOnlyItemInSet( self, item, itemSet ):
        self.assertEquals( len( itemSet ), 1 )
        self.assertTrue( item in itemSet )
if __name__ == '__main__':
    unittest.main()
