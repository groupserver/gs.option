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
from zope.schema.interfaces import WrongType
from zope.component import getGlobalSiteManager, createObject
import Products.Five
from Zope2.App import zcml
import gs.option
from gs.option import ComponentOptions
from gs.option.converter import GSIntConverterBasic
from gs.option.interfaces import IGSOptionConverter, IGSOption
from gs.option.option import GSRAMOptionFactory
from .interfaces import (TestOptionsFactory, TestOptionsFactory2)


class BasicOptionTest(TestCase):
    def setUp(self):
        self.gsm = getGlobalSiteManager()

        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', gs.option)

        self.gsm.registerUtility(factory=GSRAMOptionFactory,
                                    name="groupserver.Option")
        self.gsm.registerUtility(factory=TestOptionsFactory,
                                    name="gs.option.tests.options")
        self.gsm.registerUtility(factory=TestOptionsFactory2,
                                    name="gs.option.tests2.options")

    def test_01_OptionConverterFromOption(self):
        option = createObject("groupserver.Option", None, 'gs.option.tests',
                                'int_id')
        self.assertIsInstance(option.converter, GSIntConverterBasic)

    def test_03_OptionFactoryFailedComponentLookup(self):
        self.assertRaises(ValueError, createObject,
                            "groupserver.Option", None,
                            "gs.option.tests.thisdoesntexist", "int_id")

    def test_04_OptionStorageNoQualifiers(self):
        option = createObject("groupserver.Option", None, 'gs.option.tests',
                                'int_id')

        self.assertEquals(option.get(), None)
        self.assertEquals(option.set(21), None)
        self.assertEquals(option.get(), 21)

    def test_05_OptionStorageQualified(self):
        option = createObject("groupserver.Option", None, 'gs.option.tests',
                                'int_id')

        self.assertEquals(option.get('someSite'), None)
        self.assertEquals(option.get('someSite', 'someGroup'), None)

        self.assertEquals(option.set(42, 'someSite'), None)
        self.assertEquals(option.set(84, 'someSite', 'someGroup'), None)

        self.assertEquals(option.get('someSite'), 42)
        self.assertEquals(option.get('someSite', 'someGroup'), 84)

        # because we don't reset the storage between tests, this should return
        # the result of the set in test_04.
        self.assertEquals(option.get(), 21)

    def test_06_OptionConverter(self):
        option = createObject("groupserver.Option", None, 'gs.option.tests',
                                'int_id')

        self.assertRaises(WrongType, option.set, '42', None)


class ComponentOptionsHelperTest(TestCase):
    def setUp(self):
        self.gsm = getGlobalSiteManager()

        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', gs.option)

        self.gsm.registerUtility(factory=GSRAMOptionFactory, provided=IGSOption)
        self.gsm.registerUtility(factory=TestOptionsFactory,
                provided=IGSOptionConverter, name="gs.option.tests.options")
        self.gsm.registerUtility(factory=TestOptionsFactory2,
                provided=IGSOptionConverter, name="gs.option.tests2.options")

    def test_01_OptionsGet(self):
        options = ComponentOptions(None, "gs.option.tests")
        # set in previous test set
        self.assertEquals(options.get("int_id"), 21)
        self.assertEquals(options.set(42, "int_id"), None)
        self.assertEquals(options.get("int_id"), 42)
