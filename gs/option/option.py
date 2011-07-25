# coding=utf-8
import zope.component
import zope.interface
import zope.schema
import interfaces
from zope.component import queryUtility, createObject
from zope.component.interfaces import ComponentLookupError
from zope.component.factory import IFactory
from queries import OptionQuery

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
        ##    raise ComponentLookupError("No utility registered: %s.options" % self.componentId)
        ##
        ##return converterFactory(self.context, self.optionId, self)
    
    def get(self, siteId=None, groupId=None):
        raise NotImplementedError

    def set(self, value, siteId=None, groupId=None):
        raise NotImplementedError
        
class GSRDBOption(GSBaseOption):
    """ An option class using a relational backend.
    
    """
    zope.interface.implements(interfaces.IGSRDBOption)
    
    def get(self, siteId=None, groupId=None):
        da = getattr(self.context, 'zsqlalchemy')
        optionRDB = OptionQuery(da, self.componentId, self.optionId)
        value = optionRDB.get(siteId, groupId)
        if value:
            value = self.converter.toSchemaValue(value)
            
        return value
            
    def set(self, value, siteId=None, groupId=None):
        da = getattr(self.context, 'zsqlalchemy')
        optionRDB = OptionQuery(da, self.componentId, self.optionId)
        value = self.converter.toStorageValue(value)
        optionRDB.set(value, siteId, groupId)
        
class GSRAMOption(GSBaseOption):
    """ An option class using a RAM backend. Changes will be lost 
    between restarts.
    
    """
    _backend_dict = {}

    zope.interface.implements(interfaces.IGSRAMOption)    
    def __init__(self, context, componentId, optionId):
        GSBaseOption.__init__(self, context, componentId, optionId)

    def get(self, siteId=None, groupId=None):
        key = (self.componentId, self.optionId, siteId, groupId)
        value = self._backend_dict.get(key)
        if value != None:
            value = self.converter.toSchemaValue(value)
            
        return value
    
    def set(self, value, siteId=None, groupId=None):
        key = (self.componentId, self.optionId, siteId, groupId)
        value = self.converter.toStorageValue(value)
        self._backend_dict[key] = value
    
class GSBaseOptionFactory(object):
    zope.interface.implements(IFactory)
    backend = None
    def __call__(self, context, componentId, optionId):
        return self.backend(context, componentId, optionId)

    def getInterfaces(self):
        return zope.interface.implementedBy(self.backend)

class GSRDBOptionFactory(GSBaseOptionFactory):
    backend = GSRDBOption
    
class GSRAMOptionFactory(GSBaseOptionFactory):
    backend = GSRAMOption
