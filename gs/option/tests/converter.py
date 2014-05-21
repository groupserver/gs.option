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
import sys
if (sys.version_info < (3, )):
    longInt = long
    unicodeStr = unicode
else:
    longInt = int
    unicodeStr = str
from unittest import TestCase
from zope.component import (getGlobalSiteManager, createObject)
from zope.schema.interfaces import WrongType
import Products.Five
from Zope2.App import zcml
import gs.option
from gs.option.converter import (GSIntConverterBasic, GSTextConverterBasic)
import gs.option.sql
from .interfaces import (TestOptionsFactory, TestOptionsFactory2)


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

    def test_OptionConverterFactory(self):
        option = createObject('groupserver.Option', None, 'gs.option.tests2',
                                'int_id')

        optionConverter = createObject("gs.option.tests.options", None,
                                        "text_id", option)
        self.assertIsInstance(optionConverter, GSTextConverterBasic)

        optionConverter = createObject("gs.option.tests.options", None,
                                        "int_id", option)
        self.assertIsInstance(optionConverter, GSIntConverterBasic)

    def test_OptionConverterFromOption(self):
        option = createObject('groupserver.Option', None, 'gs.option.tests',
                                'int_id')
        self.assertIsInstance(option.converter, GSIntConverterBasic)


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


WRONG_VALUES = [[1, 2, 3], (1, 2, 3), {'1': 2}]


class IntTest(BaseConverterTest):
    def _setupOption(self):
        self.option = createObject('groupserver.Option', None,
                                    'gs.option.tests', 'int_id')

    def testConvertToSchemaValue(self):
        self.assertEqual(type(self.option.converter.toSchemaValue('1')), int)
        self.assertEqual(type(self.option.converter.toSchemaValue('1' * 100)),
                            longInt)

    def testConvertToStorageValue(self):
        self.assertEqual(type(self.option.converter.toStorageValue(1)),
                        unicodeStr)
        self.assertEqual(type(self.option.converter.toStorageValue(10 ** 100)),
                            unicodeStr)

    def testFailValidation(self):
        for wv in WRONG_VALUES + [1.0, '1']:
            self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                wv)


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
                            unicodeStr)
        self.assertEqual(type(self.option.converter.toStorageValue(False)),
                            unicodeStr)

    def testFailValidation(self):
        for wv in WRONG_VALUES + [1.0, '1']:
            self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                wv)


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
                            unicodeStr)
        r = self.option.converter.toStorageValue(10.0 ** 100)
        self.assertEqual(type(r), unicodeStr)

    def testFailValidation(self):
        for wv in WRONG_VALUES + ['1']:
            self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                wv)


class TextTest(BaseConverterTest):
    def _setupOption(self):
        self.option = createObject('groupserver.Option', None,
                                    'gs.option.tests', 'text_id')

    def off_testConvertToSchemaValue(self):
        r = self.option.converter.toSchemaValue('This is some text')
        self.assertEqual(type(r), unicodeStr)

    def off_testConvertToStorageValue(self):
        r = self.option.converter.toStorageValue('this is some text')
        self.assertEqual(type(r), unicodeStr)

    def testFailValidation(self):
        for wv in WRONG_VALUES + [1.0, 1, True]:
            self.assertRaises(WrongType, self.option.converter.toStorageValue,
                                wv)
