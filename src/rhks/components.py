from error import *


def escapeValue( value ):
    ret = value
    if value.find( " " ) > 0 :
        ret = "\"" + value + "\""
    return ret

def appendItemWoDuplicate( item, itemList, what ):
    if item in itemList:
        raise DuplicationError( what + " is duplicated" )
    itemList.append( item )

def isValidRepoOptions( options ):
    if options.has_key( "baseurl" ) == options.has_key( "mirrorlist" ):
        return False
    return not False

def isSameRepo( options1, options2 ):
    if options1.has_key( "baseurl" ) and options2.has_key( "baseurl" ):
        return options1[ "baseurl" ] == options2[ "baseurl" ]
    elif options1.has_key( "mirrorlist" ) and options2.has_key( "mirrorlist" ):
        return options1[ "mirrorlist" ] == options2[ "mirrorlist" ]
    else:
        return False

class Directive:
    def __init__(self, name):
        self.name = name;
        self.options={}
    
    def compileOptions(self):
        ret=""
        for key, value in self.options.iteritems():
            optionValue = " --" + key
            if value == "no":
                optionValue = ""
            elif not value == "yes":
                optionValue += " " + escapeValue( value )
            ret += optionValue
        return ret
    
    def compile(self):
        return name + compileOptions(self)

    def addOption( self, optionName, optionValue ):
        self.options[ optionName ] = optionValue

class Command(Directive):
    def __init__(self, name ):
        Directive.__init__(self,name)
        self.value=None

    def compile(self):
        ret = self.name + self.compileOptions()
        if not self.value == None:
            ret += " " + self.value
        return ret

    def __eq__(self, other ):
        if other == None:
            return False
        return self.name == other.name
            
    def __ne__(self, other ):
        if other == None:
            return False
        return not self.name == other.name

    def __hash__(self):
        if self.name == None:
            return None
        return self.name.__hash__()

    def compareOption( self, optionName, other ):
        return self.options[ optionName ] == other.options[ optionName ]

def compilePackageGroup( gName ):
    return "@ " + gName

def compileAddPackage( pName ):
    return pName

def compileDeletePackage( pName ):
    return "-" + pName

class Packages(Directive):
    def __init__(self):
        Directive.__init__(self,"packages")
        self.groups= []
        self.rmpkgs=[]
        self.addpkgs=[]
        self.includes=[]

    def addGroup(self,groupName):
        appendItemWoDuplicate( groupName, self.groups, "group " + groupName )

    def addPkg(self,pkgName):
        appendItemWoDuplicate( pkgName, self.addpkgs, 
                                 "adding package " + pkgName )

    def deletePkg(self, pkgName ):
        appendItemWoDuplicate( pkgName, self.rmpkgs, 
                                 "deleting package " + pkgName )

    def addInclude( self, include ):
        appendItemWoDuplicate( include, self.includes,
                               "inclusion " + include.value )

    def compile(self):
        ret = "%" + self.name + self.compileOptions() + "\n"
        for gName in self.groups:
            ret += compilePackageGroup( gName ) + "\n"
        for pName in self.addpkgs:
            ret += compileAddPackage( pName ) + "\n"
        for pName in self.rmpkgs:
            ret += compileDeletePackage( pName ) + "\n"
        for include in self.includes:
            ret += include.compile()

        return ret

    def merge(self, pkgs):
        
        if pkgs == None:
            return
        for group in pkgs.groups:
            self.addGroup( group )
        for pkg in pkgs.addpkgs:
            self.addPkg( pkg )
        for pkg in pkgs.rmpkgs:
            self.deletePkg( pkg )

class Action(Directive):
    def __init__( self, name ):
        Directive.__init__( self, name )
        self.includes=[]
        
    def include( self, filePath ):
        appendItemWoDuplicate( filePath, self.includes, 
                               "including source " + filePath )

    def compile( self, includeBaseDir=None ):
        ret= "%" + self.name + self.compileOptions() + "\n"
        for includeFile in self.includes:
            if includeBaseDir == None:
                filePath = includeFile
            else:
                filePath = includeBaseDir + "/" + includeFile
            file = open( filePath, "r" )
            ret += file.read()
            ret += "\n"

        return ret

class IncludeMacro(Directive):
    def __init__( self ):
        Directive.__init__( self, "include" )
        self.value = None

    def compile( self ):
        ret = "%" + self.name + " " + self.value + "\n"
        return ret
    
    def __eq__(self, other ):
        if other == None:
            return False
        return self.value == other.value

    def __ne__(self, other ):
        if other == None:
            return False
        return not self.value == other.value

    def __hash__(self):
        if self.value == None:
            return None
        return self.value.__hash__()

class Kickstart:
    def __init__(self, name ):
        self.name = name
        self.commands = []
        self.packages = None
        self.preAction = None
        self.postActions = []
        self.includes= []
        self.srcDir=None

    def addCommand( self, command ):

        if not self.isValidCommand( command ):
            raise InvalidCommandError( "command `" + 
                                       command.compile() + "' is invalid" )

        if command.name == "repo":
            self.appendRepoCommandWoDuplicate( command )
        else:
            appendItemWoDuplicate( command, 
                                   self.commands, 
                                   "command " + command.name )
    def addPackages( self, packages):
        if self.packages == None:
            self.packages = packages
        else:
            self.packages.merge( packages )

    def addInclude( self, include ):

        appendItemWoDuplicate( include, self.includes, 
                                 include.value + " inclusion" )

    def addPostAction( self, postAction ):
        self.postActions.append( postAction )

    def merge( self, ks ):
        
        for command in ks.commands:
            self.addCommand( command )

        for include in ks.includes:
            self.addInclude( include )

        self.addPackages( ks.packages )

        if self.preAction == None:
            self.preAction = ks.preAction
        elif not ks.preAction == None:
            raise DuplicationError( "pre action is duplicated" )
        
        self.postActions.extend( ks.postActions )

    def isValidCommand( self, command ):
        
        if command.name == "repo":
            return isValidRepoOptions( command.options )
        else:
            return not False

    def appendRepoCommandWoDuplicate( self, repoCommand ):
        
        for command in self.commands:
            if command.name == "repo" and isSameRepo( command.options, 
                                                      repoCommand.options ):
                raise DuplicationError( repoCommand.compile() + 
                                        " is duplicated" )
        
        self.commands.append( repoCommand )
