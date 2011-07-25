# coding=utf-8
from converter import OptionLookupError

# Helpers for common modalities
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
    
