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


class ComponentOptions(object):
    def __init__(self, context, component_id):
        self.context = context
        self.component_id = component_id

    def get(self, option_id, site_id=None, group_id=None):
        option = createObject("groupserver.Option",
                              self.context, self.component_id, option_id)
        return option.get(site_id, group_id)

    def set(self, value, option_id, site_id=None, group_id=None):
        option = createObject("groupserver.Option",
                              self.context, self.component_id, option_id)
        return option.set(value, site_id, group_id)
