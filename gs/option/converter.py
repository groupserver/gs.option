import zope.component
import zope.interface
import zope.schema
from z3c.form.i18n import MessageFactory as _
import interfaces

class BaseRDBOption(object):
    zope.interface.implements(interfaces.IGSStorageOption)
    def __init__(self, value):
        self.value = value
    
class GSIntegerConverter(object):
    """ A data converter for integers.
    
    """
    zope.interface.implements(interfaces.IGSOptionConverter)
    zope.component.adapts(
        zope.schema.interfaces.IInt, interfaces.IGSStorageOption)
    
    schemaType = int
    storageType = unicode
    errorMessage = _('The value was not a valid integer literal.')
    def __init__(self, schemaoption, storageoption):
        self.schemaoption = schemaoption
        self.storageoption = storageoption

    def toStorageValue(self, value):
        return self.storageType(value)

    def toSchemaValue(self, value):
        return self.schemaType(value)
    
