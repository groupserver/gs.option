from unittest import main, makeSuite, TestCase

from zope.interface import implements
from zope.schema import Int
from zope.component import getMultiAdapter
from gs.option.converter import BaseRDBOption, GSIntegerConverter
from gs.option.interfaces import IGSOptionConverter
from zope.component import provideAdapter

class IntTest(TestCase):
    def setUp(self):
        provideAdapter(GSIntegerConverter)
        self.int = Int()
        self.baseRDBOption = BaseRDBOption()
        self.convert = getMultiAdapter((self.int,self.baseRDBOption), IGSOptionConverter)

    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.convert.toSchemaValue('1')), int)
        
    def testConvertToStorageValue(self):
        self.assertEqual(type(self.convert.toStorageValue(1)), unicode)

def test_suite():
    return makeSuite(IntTest)

if __name__ == '__main__':
    main(defaultTest='test_suite')
