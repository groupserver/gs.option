from converter import OptionLookupError

def get(context, componentId, optionId, siteId=None, groupId=None, default=None):
    optionUtility = queryUtility(IGSOption)
    option = optionFactory(context, componentId, optionId, siteId, groupId)
    
    retval = default
    
    optionBackend = queryUtility(IGSOptionBackend)
    value = optionBackend.get(option)
    retval = converter.toSchemaValue(value)
  
    return retval

def set(componentId, optionId, siteId=None, groupId=None):
    pass