from rhks.components import *
from rhks.error import *
import unittest
import os
from rhksTestBase import *

tmpFile="test.tmp"
def createTmpFile( data ):
    file = open( tmpFile, "w" )
    file.write(data)
    file.close()
    
def createIncludeMacro( value ):
    inc = IncludeMacro( )
    inc.value = value
    return inc

class componentsTest(TestBase):

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
        inc = createIncludeMacro( "/tmp/network.ks" )
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

    def testIncludeInPkg(self):
        packages = Packages()
        packages.addInclude( createIncludeMacro( "/tmp/test.part" ) )
        self.assertOnlyItemInSet( createIncludeMacro( "/tmp/test.part" ),
                                  packages.includes )

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
        inc1 = createIncludeMacro( "test" )
        self.assertFalse( inc1 == None )
        inc2 = createIncludeMacro( "test" )
        self.assertTrue( inc1 == inc2 )
        self.assertEquals( inc2, inc1 )
        inc2.value ="other"
        self.assertFalse( inc1 == inc2 )
        
    def testCompareIncludeMacro( self ):
        cmd1 = Command( "cmd1" )
        self.assertFalse( cmd1 == None )
        cmd2 = Command( "cmd2" )
        self.assertFalse( cmd1 == cmd2 )
        self.assertNotEquals( cmd1, cmd2 )
        cmd3 = Command( "cmd1" )
        self.assertTrue( cmd1 == cmd3 )
        self.assertEquals( cmd1, cmd3 )
        cmd1.addOption( "hello", "world" )
        cmd3.addOption( "hello", "anotherWorld" )
        self.assertTrue( cmd1 == cmd3 )
        self.assertEquals( cmd1, cmd3 )
        
    def testDuplicatedKickstartIncludes( self ):
        ks = Kickstart( "test" )
        ks.addInclude( createIncludeMacro( "test" ) )
        try:
            ks.addInclude( createIncludeMacro( "test" ) )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )  
    def testDuplicatedCommands( self ):
        ks = Kickstart( "test" )
        ks.addCommand( Command( "test" ) )
        try:
            ks.addCommand( Command( "test" ) )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )

    def testInvalidRepoCommand( self ):
        ks = Kickstart( "test" )
        try:
            ks.addCommand( Command( "repo" ) )
        except InvalidCommandError:
            pass
        else:
            self.fail( "repo command has niehter baseurl or mirrorlist" );
        ks = Kickstart( "test" )
        repoCmd = Command( "repo" )
        repoCmd.addOption( "baseurl", "cdrom" )
        repoCmd.addOption( "mirrorlist", "mirrorlist" )
        try:
            ks.addCommand( Command( "repo" ) )
        except InvalidCommandError:
            pass
        else:
            self.fail( "repo command has either baseurl or mirrorlist" );

    def testMultipleRepoCommands( self ):
        ks = Kickstart( "test" )
        repoCmd1 = Command( "repo" )
        repoCmd1.addOption( "baseurl", "cdrom" )
        repoCmd2 = Command( "repo" )
        repoCmd2.addOption( "baseurl", "cdrom2" )
        ks.addCommand( repoCmd1 )
        try:
            ks.addCommand( repoCmd2 )
        except DuplicationError:
            self.fail( "multipe repos are allowed" )
        else:
            pass

    def testDuplicatedRepoCommands( self ):
        ks = Kickstart( "test" )
        repoCmd1 = Command( "repo" )
        repoCmd1.addOption( "baseurl", "cdrom" )
        repoCmd2 = Command( "repo" )
        repoCmd2.addOption( "baseurl", "cdrom" )
        ks.addCommand( repoCmd1 )
        try:
            ks.addCommand( repoCmd2 )
        except DuplicationError:
            pass
        else:
            self.fail( "multipe repos are allowed" )
        
    def testDuplicatedIncludesInAction( self ):
        preAction = Action( "pre" )
        preAction.include ( "file_a" )
        try:
            preAction.include( "file_a" )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )

    def testDuplicatedPackages( self ):
        pkgs = Packages()
        pkgs.addGroup( "group1" )
        pkgs.addPkg( "pkg1" )
        pkgs.deletePkg( "pkg2" )
        pkgs.addInclude( createIncludeMacro( "/tmp/test.part" ) )
        
        try:
            pkgs.addGroup( "group1" )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )
        try:
            pkgs.addPkg( "pkg1" )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )
        try:
            pkgs.deletePkg( "pkg2" )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )
        try:
            pkgs.addInclude( createIncludeMacro( "/tmp/test.part") )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication error" )


    def testMergeKickstartWithCommands( self ):
        ks1 = Kickstart( "test" )
        ks2 = Kickstart( "test2" )
        ks2.addCommand( Command( "test" ) )
        ks1.merge( ks2 )
        self.assertOnlyItemInSet( Command( "test" ), ks1.commands )

    def testMergeKickstartWithDupCommands( self ):
        ks1 = Kickstart( "test1" )
        ks1.addCommand( Command( "test" ) )
        ks2 = Kickstart( "test2" )
        ks2.addCommand( Command( "test" ) )
        try:
            ks1.merge( ks2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication command error" )

    def testMergeKickstartWithIncludes( self ):
        inc = createIncludeMacro( "test" )
        ks1 = Kickstart( "test" )
        ks2 = Kickstart( "test2" )
        ks2.addInclude( inc )
        ks1.merge( ks2 )
        self.assertOnlyItemInSet( inc, ks1.includes )

    def testMergeKickstartWithDupIncludes( self ):
        inc = createIncludeMacro( "test" )
        ks1 = Kickstart( "test" )
        ks1.addInclude( inc )
        ks2 = Kickstart( "test2" )
        ks2.addInclude( inc )
        
        try:
            ks1.merge( ks2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication include error" )
        
    def testMergePackages( self ):
        pkgs1 = Packages()
        pkgs2 = Packages()
        pkgs2.addGroup( "base" )
        pkgs2.addPkg( "pkgadd" )
        pkgs2.deletePkg( "pkgdel" )
        pkgs1.merge( pkgs2 )
        self.assertOnlyItemInSet( "base", pkgs1.groups )
        self.assertOnlyItemInSet( "pkgadd", pkgs1.addpkgs )
        self.assertOnlyItemInSet( "pkgdel", pkgs1.rmpkgs ) 
   
    def testMergeNonePackages( self ):
        pkgs1 = Packages()
        pkgs2 = None
        pkgs1.addGroup( "base" )
        pkgs1.merge( pkgs2 )
        self.assertOnlyItemInSet( "base", pkgs1.groups )

    def testMergeDuplicatePackageGroup( self ):
        pkgs1 = Packages()
        pkgs1.addGroup( "base" )
        pkgs2 = Packages()
        pkgs2.addGroup( "base" )
        try:
            pkgs1.merge( pkgs2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication package group error" )

    def testMergeDuplicateAddPackage( self ):
        pkgs1 = Packages()
        pkgs1.addPkg( "base" )
        pkgs2 = Packages()
        pkgs2.addPkg( "base" )
        try:
            pkgs1.merge( pkgs2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication package add error" )

    def testMergeDuplicateDeletePackage( self ):
        pkgs1 = Packages()
        pkgs1.deletePkg( "base" )
        pkgs2 = Packages()
        pkgs2.deletePkg( "base" )
        try:
            pkgs1.merge( pkgs2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication package delete error" )

    def testMergeKickstartWithPreAction( self ):
        ks1 = Kickstart( "test1" )
        ks2 = Kickstart( "test2" )
        ks2.preAction = Action( "pre" )
        ks1.merge( ks2 )
        self.assertNotEquals( ks1.preAction, None )
        try :
            ks1.merge( ks2 )
        except DuplicationError:
            pass
        else:
            self.fail( "expected duplication pre action error" )

    def testMergeKickstartWithPostAction( self ):
        ks1 = Kickstart( "test1" )
        ks2 = Kickstart( "test2" )
        ks2.addPostAction( Action( "post" ) )
        ks1.merge( ks2 )
        self.assertEquals( len( ks1.postActions ) , 1 )
        ks1.merge( ks2 )
        self.assertEquals( len( ks1.postActions ), 2 )
        
    def testRepoOptions( self ):

        self.assertFalse( isValidRepoOptions( {} ) );
        options = {}
        options [ "baseurl" ] = "cdrom"
        options [ "mirrorlist" ] = "mirror"
        self.assertFalse( isValidRepoOptions( options ) );
        options = {}
        options [ "baseurl" ] = "cdrom"
        self.assertTrue( isValidRepoOptions( options ) );
        options = {}
        options [ "mirrorlist" ] = "mirror"
        self.assertTrue( isValidRepoOptions( options ) );

    def testSameBaseUrlRepoOptions( self ):
        options1 = {}
        options1 [ "baseurl" ] = "cdrom"
        options2 = {}
        options2 [ "baseurl" ] = "cdrom"
        self.assertTrue( isSameRepo( options1, options2 ) )        
        options1 = {}
        options1 [ "baseurl" ] = "cdrom"
        options2 = {}
        options2 [ "baseurl" ] = "cdrom2"
        self.assertFalse( isSameRepo( options1, options2 ) )

    def testSameMirrorListRepoOptions( self ):
        options1 = {}
        options1 [ "mirrorlist" ] = "mirror"
        options2 = {}
        options2 [ "mirrorlist" ] = "mirror"
        self.assertTrue( isSameRepo( options1, options2 ) )        
        options1 = {}
        options1 [ "mirrorlist" ] = "mirror"
        options2 = {}
        options2 [ "mirrorlist" ] = "mirror2"
        self.assertFalse( isSameRepo( options1, options2 ) )

    def testDiffRepoOptions( self ):
        options1 = {}
        options1 [ "mirrorlist" ] = "mirror"
        options2 = {}
        options2 [ "baseurl" ] = "cdrom"
        self.assertFalse( isSameRepo( options1, options2 ) ) 
        
if __name__ == '__main__':
    unittest.main()
