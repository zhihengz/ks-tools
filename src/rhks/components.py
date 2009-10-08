from error import *

def escapeValue( value ):
    ret = value
    if value.find( " " ) > 0 :
        ret = "\"" + value + "\""
    return ret

def addItemWithoutDuplicate( item, itemSet, what ):
    if item in itemSet:
        raise DuplicationError( what + " is duplicated" )
    itemSet.add( item )

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

def compilePackageGroup( gName ):
    return "@ " + gName

def compileAddPackage( pName ):
    return pName

def compileDeletePackage( pName ):
    return "-" + pName

class Packages(Directive):
    def __init__(self):
        Directive.__init__(self,"packages")
        self.groups=set([])
        self.rmpkgs=set([])
        self.addpkgs=set([])

    def addGroup(self,groupName):
        addItemWithoutDuplicate( groupName, self.groups, "group " + groupName )

    def addPkg(self,pkgName):
        addItemWithoutDuplicate( pkgName, self.addpkgs, 
                                 "adding package " + pkgName )

    def deletePkg(self, pkgName ):
        addItemWithoutDuplicate( pkgName, self.rmpkgs, 
                                 "deleting package " + pkgName )

    def compile(self):
        ret = "%" + self.name + self.compileOptions() + "\n"
        for gName in self.groups:
            ret += compilePackageGroup( gName ) + "\n"
        for pName in self.addpkgs:
            ret += compileAddPackage( pName ) + "\n"
        for pName in self.rmpkgs:
            ret += compileDeletePackage( pName ) + "\n"
        return ret

    def merge(self, pkgs):
        for group in pkgs.groups:
            self.addGroup( group )
        for pkg in pkgs.addpkgs:
            self.addPkg( pkg )
        for pkg in pkgs.rmpkgs:
            self.deletePkg( pkg )

class Action(Directive):
    def __init__( self, name ):
        Directive.__init__( self, name )
        self.includes=set([])
        
    def include( self, filePath ):
        self.includes.add( filePath )

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
        self.commands = set([])
        self.packages = None
        self.preAction = None
        self.postAction = None
        self.includes= set([])
        self.srcDir=None

    def addCommand( self, command ):
        addItemWithoutDuplicate( command, 
                                 self.commands, 
                                 "command " + command.name )
    def addPackages( self, packages):
        if self.packages == None:
            self.packages = packages
        else:
            self.packages.merge( packages )

    def addInclude( self, include ):

        addItemWithoutDuplicate( include, self.includes, 
                                 include.value + " inclusion" )

    def merge( self, ks ):
        
        for command in ks.commands:
            self.addCommand( command )

        for include in ks.includes:
            self.addInclude( include )

        self.addPackages( ks.packages )
