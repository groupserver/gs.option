# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from zope.component import (getGlobalSiteManager, createObject)
import zope.interface
from zope.schema import Text, Int, Bool, Float
from zope.schema.interfaces import WrongType
import Products.Five
from Zope2.App import zcml
import gs.option
from gs.option.converter import (GSOptionConverterFactory, GSIntConverterBasic,
    GSTextConverterBasic)
import gs.option.sql


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


class ConverterTest(TestCase):
    def setUp(self):
        self.gsm = getGlobalSiteManager()

        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', gs.option)

        self.gsm.registerUtility(factory=TestOptionsFactory,
                                    name="gs.option.tests.options")
        self.gsm.registerUtility(factory=TestOptionsFactory2,
                                    name="gs.option.tests2.options")

    def testOptionConverterFactory(self):
        option = createObject('groupserver.Option', None, 'gs.option.tests2',
                                'int_id')

        optionConverter = createObject("gs.option.tests.options", None,
                                        "text_id", option)
        assert isinstance(optionConverter, GSTextConverterBasic)

        optionConverter = createObject("gs.option.tests.options", None,
                                        "int_id", option)
        assert isinstance(optionConverter, GSIntConverterBasic)

    def testOptionConverterFromOption(self):
        option = createObject('groupserver.Option', None, 'gs.option.tests',
                                'int_id')
        assert isinstance(option.converter, GSIntConverterBasic)


class BaseConverterTest(TestCase):
    def setUp(self):
        # setup the converter adapters and option factory registered in the
        # gs.option -> configure.zcml
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', gs.option)

        # register an option converter factory for the test case
        gsm = getGlobalSiteManager()
        gsm.registerUtility(factory=TestOptionsFactory,
                            name="gs.option.tests.options")

        self._setupOption()


class IntTest(BaseConverterTest):
    def _setupOption(self):
        self.option = createObject('groupserver.Option', None,
                                    'gs.option.tests', 'int_id')

    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('1')), int)
        self.assertEqual(type(self.option.converter.toSchemaValue('1' * 100)),
                            long)

    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(1)), unicode)
        self.assertEqual(type(self.option.converter.toStorageValue(10 ** 100)),
                            unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1.0)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, '1')
        #self.assertRaises(WrongType, self.option.converter.toStorageValue,
        #                    u'1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                [1, 2, 3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                (1, 2, 3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                {'1': 2})


class BoolTest(BaseConverterTest):
    def _setupOption(self):
        self.option = createObject('groupserver.Option', None,
                                    'gs.option.tests', 'bool_id')

    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('True')),
                            bool)
        self.assertEqual(type(self.option.converter.toSchemaValue('False')),
                            bool)

    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(True)),
                            unicode)
        self.assertEqual(type(self.option.converter.toStorageValue(False)),
                            unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1.0)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, '1')
        #self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            #u'1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            [1, 2, 3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            (1, 2, 3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            {'1': 2})


class FloatTest(BaseConverterTest):
    def _setupOption(self):
        self.option = createObject('groupserver.Option', None,
                                    'gs.option.tests', 'float_id')

    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('1.0')),
                            float)
        r = self.option.converter.toSchemaValue('1' * 100 + '.0')
        self.assertEqual(type(r), float)

    def off_testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(1.0)),
                            unicode)
        r = self.option.converter.toStorageValue(10.0 ** 100)
        self.assertEqual(type(r), unicode)

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue, '1')
        #self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            #u'1')
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            [1, 2, 3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            (1, 2, 3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            {'1': 2})


class TextTest(BaseConverterTest):
    def _setupOption(self):
        self.option = createObject('groupserver.Option', None,
                                    'gs.option.tests', 'text_id')

    def off_testConvertToSchemaValue(self):
        r = self.option.converter.toSchemaValue('This is some text')
        self.assertEqual(type(r), unicode)  # Python 3 issues

    def off_testConvertToStorageValue(self):
        r = self.option.converter.toStorageValue('this is some text')
        self.assertEqual(type(r), unicode)  # Python 3 issues

    def testFailValidation(self):
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            'non-unicode text')
        self.assertRaises(WrongType, self.option.converter.toStorageValue, True)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1)
        self.assertRaises(WrongType, self.option.converter.toStorageValue, 1.0)
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            [1, 2, 3])
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            (1, 2, 3))
        self.assertRaises(WrongType, self.option.converter.toStorageValue,
                            {'1': 2})
