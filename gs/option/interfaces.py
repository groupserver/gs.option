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
from zope.interface import Interface, Attribute


class IGSOptionConverter(Interface):
    def toStorageValue():
        """ Converts a schema value to a value suitable for storage in
            the backend database.

            This method *should* also validate the value prior to conversion
            against the schema field.

            If the conversion fails, a ``ValueError`` *must* be raised. If
            the validation fails, a ``ValidationError`` *must* be raised.
        """

    def toSchemaValue():
        """ Converts a value from the backend storage into a value
            acceptable for the schema.

            This methods *must* also validate the converted value against the
            field.

            If the conversion fails, a ``ValueError`` *must* be raised. If
            the validation fails, a ``ValidationError`` *must* be raised.
        """


class IGSOption(Interface):
    context = Attribute("The context in which the option is being used.")
    componentId = Attribute("The componentId of the option.")
    optionId = Attribute("The optionId of the option.")

    def get(self, siteId=None, groupId=None):
        """ Fetch the value of the option, further descriminating by the siteId
            and groupId.
        """

    def set(self, value, siteId=None, groupId=None):
        """ Set the value of the option, further descriminating by the siteId
            and groupId.

            This must both insert missing options, and update options that
            exist.
        """


class IGSRDBOption(IGSOption):
    pass


class IGSRAMOption(IGSOption):
    pass
