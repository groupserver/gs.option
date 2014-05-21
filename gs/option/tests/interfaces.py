# -*- coding: utf-8 -*-
import zope.interface
from zope.schema import Text, Int, Bool, Float
from gs.option.converter import GSOptionConverterFactory


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
