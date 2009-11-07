from rhks.comps import *
from rhksTestBase import *

class compsTest( TestBase ):

    def testParsePackagesWoDuplication( self ):
        xmldata = """<comps>
<packagereq>foo</packagereq>
<packagereq>bar</packagereq>
</comps>
"""
