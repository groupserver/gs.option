# coding=utf-8
import zope.component
import zope.interface
import zope.interface.declarations
import zope.schema
import interfaces
from zope.component.factory import IFactory
from zope.component import queryUtility
from gs.option.option import OptionLookupError

class GSOptionConverterFactory(object):
    """ Returns an option converter using optionID and StorageOption as descriminators.
    
        StorageOption is necessary to determine what kind of backend storage we are dealing with.
    
    """
    zope.interface.implements(IFactory)
    
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
        return zope.interface.declarations.Implements([interfaces.IGSOptionConverter])

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

class GSBoolConverterBasic(GSBaseConverter):
    """ A data converter for booleans.
    
    """
    errorMessage = u'The value was not a valid boolean literal.'
    
class GSIntConverterBasic(GSBaseConverter):
    """ A data converter for integers.
    
    """    
    errorMessage = u'The value was not a valid integer literal.'
    
class GSFloatConverterBasic(GSBaseConverter):
    """ A data converter for floats.
    
    """
    errorMessage = u'The value was not a valid float literal.'

class GSTextConverterBasic(GSBaseConverter):
    """ A data converter for unicode. The text must be in unicode,
        not as a byte stream.
    
    """
    errorMessage = u'The value was not valid text.'

