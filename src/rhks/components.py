
def escapeValue( value ):
    ret = value
    if value.find( " " ) > 0 :
        ret = "\"" + value + "\""
    return ret

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
        self.groups.add( groupName )

    def addPkg(self,pkgName):
        self.addpkgs.add( pkgName )

    def deletePkg(self, pkgName ):
        self.rmpkgs.add( pkgName )

    def compile(self):
        ret = "%" + self.name + self.compileOptions() + "\n"
        for gName in self.groups:
            ret += compilePackageGroup( gName ) + "\n"
        for pName in self.addpkgs:
            ret += compileAddPackage( pName ) + "\n"
        for pName in self.rmpkgs:
            ret += compileDeletePackage( pName ) + "\n"
        return ret

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

class Kickstart:
    def __init__(self, name ):
        self.name = name
        self.commands = []
        self.packages = None
        self.preAction = None
        self.postAction = None
        self.includes= []
        self.srcDir=None

    def addCommand( self, command ):
        self.commands.append( command )

    def setPackages( self, packages):
        self.packages = packages
