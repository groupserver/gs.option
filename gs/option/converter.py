import zope.component
import zope.interface
import zope.schema
import interfaces
from zope.component.factory import IFactory
from zope.component import queryUtility
from gs.option.option import OptionLookupError

class GSOptionConverterFactory(object):
    """ Returns an option converter using optionID and StorageOption as descriminators.
    
        StorageOption is necessary to determine what kind of backend storage we are dealing with.
    
    """
    title = u'GroupServer Option Converter Factory'
    description = u'Creates a GroupServer option converter for a given component and optionId'
    interface = None

    def __call__(self, context, optionId, storageOption):
        # we don't currently use context, but potentially it could be used.
        option = self.interface.get(optionId)
        if option == None:
            raise OptionLookupError("No such option %s" % optionId)
        
        return zope.component.getMultiAdapter((option, storageOption),
                                              interfaces.IGSOptionConverter)
        
    def getInterfaces(self):
        return [self.interface]

class GSBaseConverter(object):
    """ A standard data converter for non-tricky types.
    
    """
    zope.interface.implements(interfaces.IGSOptionConverter)
    
    def __init__(self, schemaoption, storageoption):
        self.schemaoption = schemaoption
        self.storageoption = storageoption

    def toStorageValue(self, value):
        self.schemaoption.validate(value)
        
        return unicode(value)

    def toSchemaValue(self, value):
        value = self.schemaoption.fromUnicode(value)
        
        self.schemaoption.validate(value)
        
        return value

class GSBoolConverterRDB(GSBaseConverter):
    """ A data converter for booleans.
    
    """
    zope.component.adapts(zope.schema.interfaces.IBool,
                          interfaces.IGSRDBOption)
    
    errorMessage = u'The value was not a valid boolean literal.'

    
class GSIntConverterRDB(GSBaseConverter):
    """ A data converter for integers.
    
    """
    zope.component.adapts(zope.schema.interfaces.IInt,
                          interfaces.IGSRDBOption)
    
    errorMessage = u'The value was not a valid integer literal.'
    
class GSFloatConverterRDB(GSBaseConverter):
    """ A data converter for floats.
    
    """
    zope.component.adapts(zope.schema.interfaces.IFloat,
                          interfaces.IGSRDBOption)
    
    errorMessage = u'The value was not a valid float literal.'

class GSTextConverterRDB(GSBaseConverter):
    """ A data converter for unicode. The text must be in unicode,
        not as a byte stream.
    
    """
    zope.component.adapts(zope.schema.interfaces.IText,
                          interfaces.IGSRDBOption)
    
    errorMessage = u'The value was not valid text.'
