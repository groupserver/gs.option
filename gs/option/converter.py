# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2013, 2014 OnlineGroups.net and Contributors.
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
    u = unicode
else:
    u = str
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface.declarations import Implements
from zope.component.factory import IFactory
from .interfaces import IGSOptionConverter
from .option import OptionLookupError


class GSOptionConverterFactory(object):
    """ Returns an option converter using optionID and StorageOption as
    descriminators.

    StorageOption is necessary to determine what kind of backend storage
    we are dealing with.

    """
    implements(IFactory)
    title = 'GroupServer Option Converter Factory'
    description = 'Creates a GroupServer option converter for a given '\
                    'component and optionId'
    interface = None

    def __call__(self, context, optionId, storageOption):
        # we don't currently use context, but potentially it could be used.
        option = self.interface.get(optionId)
        if option is None:
            raise OptionLookupError("No such option %s" % optionId)
        retval = getMultiAdapter((option, storageOption), IGSOptionConverter)
        return retval

    def getInterfaces(self):
        retval = Implements([IGSOptionConverter])
        return retval


class GSBaseConverter(object):
    """ A standard data converter for non-tricky types."""
    implements(IGSOptionConverter)

    def __init__(self, schemaoption, storageoption):
        self.schemaoption = schemaoption
        self.storageoption = storageoption

    def toStorageValue(self, value):
        self.schemaoption.validate(value)
        retval = u(value)
        return retval

    def toSchemaValue(self, value):
        value = self.schemaoption.fromUnicode(value)

        self.schemaoption.validate(value)

        return value


class GSBoolConverterBasic(GSBaseConverter):
    """ A data converter for booleans.

    """
    errorMessage = 'The value was not a valid boolean literal.'


class GSIntConverterBasic(GSBaseConverter):
    """ A data converter for integers.

    """
    errorMessage = 'The value was not a valid integer literal.'


class GSFloatConverterBasic(GSBaseConverter):
    """ A data converter for floats."""
    errorMessage = 'The value was not a valid float literal.'


class GSTextConverterBasic(GSBaseConverter):
    """ A data converter for unicode. The text must be in unicode,
        not as a byte stream.

    """
    errorMessage = 'The value was not valid text.'
