from unittest import main, TestSuite, makeSuite, TestCase

import zope.interface
from zope.schema import *
from zope.schema.interfaces import WrongType
from gs.option.converter import *
from gs.option.interfaces import IGSOptionConverter, IGSOptionConverterFactory, IGSOption
from zope.component.factory import IFactory
from zope.component import provideAdapter, getMultiAdapter, getGlobalSiteManager, queryUtility
from zope.app.testing.setup import placefulSetUp, placefulTearDown
from Products.ZSQLAlchemy.ZSQLAlchemy import manage_addZSQLAlchemy
import Products.Five
import gs.option
from Products.Five import zcml
from zope.site.folder import Folder, rootFolder

from Testing.ZopeTestCase import ZopeTestCase
from gs.option import queries

import random

from database_setup import *

class ITestOptions(zope.interface.Interface):
    text_id = Text()
    int_id = Int()
    bool_id = Bool()
    float_id = Float()
    
class ITestOptions2(zope.interface.Interface):
    int_id = Int()

class TestOptionsFactory(GSOptionConverterFactory):
    interface = ITestOptions

class TestOptionsFactory2(GSOptionConverterFactory):
    interface = ITestOptions2

class RDBTest(ZopeTestCase):
    def afterSetUp(self):
        dbsetup()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', gs.option)
        
        alchemy_adaptor = manage_addZSQLAlchemy(self.folder, 'zalchemy')
        
        alchemy_adaptor.manage_changeProperties(hostname='localhost',
                                                port=5432,
                                                username=DATABASE_USER,
                                                password='',
                                                dbtype='postgres',
                                                database=DATABASE_NAME)
        
        self.da = alchemy_adaptor
        self.componentId = 'component_id'
        self.optionId = 'option_id'
        
    def testOptionQuery(self):
        optionQuery = queries.OptionQuery(self.da,
                                          self.componentId,
                                          self.optionId)
        
    def testSetGetOption(self):
        optionQuery = queries.OptionQuery(self.da,
                                          self.componentId,
                                          self.optionId)
        rid1 = unicode(random.random())
        rid2 = unicode(random.random())
        rid3 = unicode(random.random())
        
        optionQuery.set(rid1)
        optionQuery.set(rid2,'site')
        optionQuery.set(rid3,'site','group')
        
        self.assertEqual(optionQuery.get(),rid1)
        self.assertEqual(optionQuery.get('site'),rid2)
        self.assertEqual(optionQuery.get('site','group'),rid3)
    
    def beforeTearDown(self):
        dbteardown()
    
class ConverterTest(TestCase):
    def setUp(self):
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(factory=GSOptionFactory, provided=IGSOption)
        self.gsm.registerUtility(factory=TestOptionsFactory, provided=IGSOptionConverter, name="gs.option.tests.options")
        self.gsm.registerUtility(factory=TestOptionsFactory2, provided=IGSOptionConverter, name="gs.option.tests2.options")
        provideAdapter(GSIntConverterRDB)
        provideAdapter(GSTextConverterRDB)
        
    def testOptionFactoryUtility(self):
        optionFactory = queryUtility(IGSOption)
        assert isinstance(optionFactory, GSOptionFactory)
        
    def testOptionConverterFactory(self):
        optionFactory = queryUtility(IGSOption)
        option = optionFactory(None, 'gs.option.tests2', 'int_id', None, None)
        
        optionConverterFactory = queryUtility(IGSOptionConverter, name="gs.option.tests.options")
        assert isinstance(optionConverterFactory(None, 'text_id', option), GSTextConverterRDB)
        
        optionConverterFactory = queryUtility(IGSOptionConverter, name="gs.option.tests.options")
        assert isinstance(optionConverterFactory(None, 'int_id', option), GSIntConverterRDB)
    
    def testOptionConverterFromOption(self):
        optionFactory = queryUtility(IGSOption)
        option = optionFactory(None, 'gs.option.tests', 'int_id', None, None)
        assert isinstance(option.converter, GSIntConverterRDB)

    def testOptionFactoryFailedComponentLookup(self):
        # returns None if the component doesn't exist
        self.assertEquals(queryUtility(IGSOptionConverter, name="gs.option.tests.thisdoesntexist"),
                          None)
        
        optionFactory = queryUtility(IGSOption)
        
        self.assertRaises(OptionLookupError,
                          optionFactory, None, 'gs.option.tests.nomodule', 'thisdoesntexist', None, None)
  
class BaseConverterTest(TestCase):
    def setUp(self):
        provideAdapter(GSBoolConverterRDB)
        provideAdapter(GSFloatConverterRDB)
        provideAdapter(GSIntConverterRDB)
        provideAdapter(GSTextConverterRDB)
        
        gsm = getGlobalSiteManager()
        gsm.registerUtility(factory=GSOptionFactory, provided=IGSOption)
        gsm.registerUtility(factory=TestOptionsFactory, provided=IGSOptionConverter, name="gs.option.tests.options")
        optionFactory = queryUtility(IGSOption)

        self._setupOption(optionFactory)
  
class IntTest(BaseConverterTest):
    def _setupOption(self, optionFactory):
        self.option = optionFactory(None, 'gs.option.tests', 'int_id', None, None)
  
    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('1')), int)
        self.assertEqual(type(self.option.converter.toSchemaValue('1'*100)), long)
        
    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(1)), unicode)
        self.assertEqual(type(self.option.converter.toStorageValue(10**100)), unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1.0)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, '1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, u'1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, [1,2,3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue, (1,2,3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue, {'1':2})
        
class BoolTest(BaseConverterTest):
    def _setupOption(self, optionFactory):
        self.option = optionFactory(None, 'gs.option.tests', 'bool_id', None, None)
        
    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('True')), bool)
        self.assertEqual(type(self.option.converter.toSchemaValue('False')), bool)
        
    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(True)), unicode)
        self.assertEqual(type(self.option.converter.toStorageValue(False)), unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1.0)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, '1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, u'1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, [1,2,3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue, (1,2,3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue, {'1':2})
        
class FloatTest(BaseConverterTest):
    def _setupOption(self, optionFactory):
        self.option = optionFactory(None, 'gs.option.tests', 'float_id', None, None)
        
    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('1.0')), float)
        self.assertEqual(type(self.option.converter.toSchemaValue('1'*100+'.0')), float)
        
    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(1.0)), unicode)
        self.assertEqual(type(self.option.converter.toStorageValue(10.0**100)), unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, '1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, u'1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, [1,2,3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue, (1,2,3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue, {'1':2})

class TextTest(BaseConverterTest):
    def _setupOption(self, optionFactory):
        self.option = optionFactory(None, 'gs.option.tests', 'text_id', None, None)
                
    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue(u'This is some text')), unicode)
        
    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(u'this is some text')), unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 'non-unicode text')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, True)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1.0)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, [1,2,3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue, (1,2,3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue, {'1':2})

def test_suite():
   suite = TestSuite()
   #suite.addTest(makeSuite(ConverterTest))
   #suite.addTest(makeSuite(BoolTest))
   #suite.addTest(makeSuite(FloatTest))
   #suite.addTest(makeSuite(IntTest))
   #suite.addTest(makeSuite(TextTest))
   suite.addTest(makeSuite(RDBTest))
   
   return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')
