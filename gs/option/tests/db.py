# -*- coding: utf-8 -*-
import random
import sys
if (sys.version_info < (3, )):
    longInt = long
    unicodeStr = unicode
else:
    longInt = int
    unicodeStr = str
from zope.schema.interfaces import WrongType
from zope.component import getGlobalSiteManager, createObject
import Products.Five
from Products.ZSQLAlchemy.ZSQLAlchemy import manage_addZSQLAlchemy
from Testing.ZopeTestCase import ZopeTestCase
from Zope2.App import zcml
import gs.option
from gs.option import queries
import gs.option.sql
from . import database_setup as ds
from .interfaces import TestOptionsFactory


class RDBBaseTest(ZopeTestCase):
    def afterSetUp(self):
        if not ds.dbSetupDone:
            ds.dbteardown()
            ds.dbsetup()
            ds.dbSetupDone = True

        ds.dbTable(gs.option.sql, "01_option.sql", ["option"])
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', gs.option)

        gsm = getGlobalSiteManager()
        gsm.registerUtility(factory=TestOptionsFactory,
                            name="gs.option.tests.options")

        alchemy_adaptor = manage_addZSQLAlchemy(self.folder, 'zsqlalchemy')

        alchemy_adaptor.manage_changeProperties(hostname='localhost',
                                                port=5432,
                                                username=ds.DATABASE_USER,
                                                password='',
                                                dbtype='postgres',
                                                database=ds.DATABASE_NAME)

        self.da = alchemy_adaptor
        self.componentId = 'component_id'
        self.optionId = 'option_id'


class RDBBackendTest(RDBBaseTest):
    def test_01_OptionQuery(self):
        pass
        #optionQuery = queries.OptionQuery(self.da,
                                          #self.componentId,
                                          #self.optionId)

    def off_test_02_SetGetOption(self):
        optionQuery = queries.OptionQuery(self.da,
                                          self.componentId,
                                          self.optionId)
        rid1 = unicodeStr(random.random())
        rid2 = unicodeStr(random.random())
        rid3 = unicodeStr(random.random())

        optionQuery.set(rid1)
        optionQuery.set(rid2, 'site')
        optionQuery.set(rid3, 'site', 'group')

        self.assertEqual(optionQuery.get(), rid1)
        self.assertEqual(optionQuery.get('site'), rid2)
        self.assertEqual(optionQuery.get('site', 'group'), rid3)


class RDBOptionTest(RDBBaseTest):
    def test_01_OptionStorageNoQualifiers(self):
        option = createObject('groupserver.Option', self.folder,
                                'gs.option.tests', 'int_id')
        self.assertEquals(option.get(), None)
        self.assertEquals(option.set(21), None)
        self.assertEquals(option.get(), 21)

    def test_02_OptionStorageQualified(self):
        option = createObject('groupserver.Option', self.folder,
                                'gs.option.tests', 'int_id')

        self.assertEquals(option.get('someSite'), None)
        self.assertEquals(option.get('someSite', 'someGroup'), None)

        self.assertEquals(option.set(42, 'someSite'), None)
        self.assertEquals(option.set(84, 'someSite', 'someGroup'), None)

        self.assertEquals(option.get('someSite'), 42)
        self.assertEquals(option.get('someSite', 'someGroup'), 84)

        # note: we reset the table between tests, so this should return None
        self.assertEquals(option.get(), None)

    def test_03_OptionConverter(self):
        option = createObject('groupserver.Option', self.folder,
                                'gs.option.tests', 'int_id')

        self.assertRaises(WrongType, option.set, '42', None)
