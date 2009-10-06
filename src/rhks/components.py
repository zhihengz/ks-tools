
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

class Command(Directive):
    def __init__(self, name ):
        Directive.__init__(self,name)
        self.value=None

    def compile(self):
        ret = self.name + self.compileOptions()
        if not self.value == None:
            ret += " " + self.value
        return ret

    def addOption( self, optionName, optionValue ):
        self.options[ optionName ] = optionValue

class Packages(Directive):
    def __init__(self):
        Directive.__init__(self,"packages")
        self.groups=[]
        self.rmpkgs=[]
        self.addpkgs=[]

    def addGroup(self,groupName):
        self.groups.append( groupName )

    def addPkg(self,pkgName):
        self.addpkgs.append( pkgName )

    def deletePkg(self, pkgName ):
        self.rmpkgs.append( pkgName )

class Kickstart:
    def __init__(self, name ):
        self.name = name
        self.commands = []
        self.packages = None

    def addCommand( self, command ):
        self.commands.append( command )

    def setPackages( self, packages):
        self.packages = packages
