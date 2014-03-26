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
from zope.component import createObject
from zope.component.factory import IFactory
from zope.component.interfaces import ComponentLookupError
from zope.interface import implements, implementedBy
from .interfaces import IGSRDBOption, IGSRAMOption
from .queries import OptionQuery


class OptionLookupError(Exception):
    pass


class GSBaseOption(object):
    def __init__(self, context, componentId, optionId):
        self.context = context
        self.componentId = componentId
        self.optionId = optionId

        self.converter = self._getConverter()

    def _getConverter(self):
        #converterFactory = queryUtility(interfaces.IGSOptionConverter,
        #                                name="%s.options" % self.componentId)
        return createObject("%s.options" % self.componentId,
                                           self.context,
                                           self.optionId,
                                           self)
        ##if not converterFactory:
        ##    m = "No utility registered: %s.options"
        ##    msg = m % self.componentId
        ##    raise ComponentLookupError(msg)
        ##
        ##return converterFactory(self.context, self.optionId, self)

    def get(self, siteId=None, groupId=None):
        raise NotImplementedError

    def set(self, value, siteId=None, groupId=None):
        raise NotImplementedError


class GSRDBOption(GSBaseOption):
    """ An option class using a relational backend.

    """
    implements(IGSRDBOption)

    def get(self, siteId=None, groupId=None):
        optionRDB = OptionQuery(self.componentId, self.optionId)
        value = optionRDB.get(siteId, groupId)
        if value:
            value = self.converter.toSchemaValue(value)

        return value

    def set(self, value, siteId=None, groupId=None):
        optionRDB = OptionQuery(self.componentId, self.optionId)
        value = self.converter.toStorageValue(value)
        optionRDB.set(value, siteId, groupId)


class GSRAMOption(GSBaseOption):
    """ An option class using a RAM backend. Changes will be lost
    between restarts."""
    _backend_dict = {}
    implements(IGSRAMOption)

    def __init__(self, context, componentId, optionId):
        GSBaseOption.__init__(self, context, componentId, optionId)

    def get(self, siteId=None, groupId=None):
        key = (self.componentId, self.optionId, siteId, groupId)
        value = self._backend_dict.get(key)
        if value is not None:
            value = self.converter.toSchemaValue(value)

        return value

    def set(self, value, siteId=None, groupId=None):
        key = (self.componentId, self.optionId, siteId, groupId)
        value = self.converter.toStorageValue(value)
        self._backend_dict[key] = value


class GSBaseOptionFactory(object):
    implements(IFactory)
    backend = None

    def __call__(self, context, componentId, optionId):
        assert self.backend, 'No backend for the option!'
        try:
            retval = self.backend(context, componentId, optionId)
        except ComponentLookupError as cle:
            m = 'Could not find the option "%s" for the component "%s" '\
                'Is the Utility set up correctly?\n%s' % \
                (optionId, componentId, cle)
            raise ValueError(m)
        return retval

    def getInterfaces(self):
        return implementedBy(self.backend)


class GSRDBOptionFactory(GSBaseOptionFactory):
    backend = GSRDBOption


class GSRAMOptionFactory(GSBaseOptionFactory):
    backend = GSRAMOption
