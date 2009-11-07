import unittest

class TestBase(unittest.TestCase):

    def assertTrue( self, value ):
        """
        back porting assertTrue for python 2.3
        """
        s = super( TestBase, self)
        if hasattr( s, 'assertTrue'):
            s.assertTrue( value )
        else:
            self.assertNotEquals( False, value )

    def assertFalse( self, value ):
        """
        back porting assertFalse for python 2.3
        """
        s = super( TestBase, self)
        if hasattr( s, 'assertFalse'):
            s.assertFalse( value )
        else:
            self.assertEquals( False, value )

    def assertOnlyItemInSet( self, item, itemSet ):
        self.assertEquals( len( itemSet ), 1 )
        self.assertTrue( item in itemSet )

