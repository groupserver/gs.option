# coding=utf-8
import zope.interface
import zope.schema

class IGSOptionConverter(zope.interface.Interface):
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

class IGSOption(zope.interface.Interface):
    context = zope.interface.Attribute("The context in which the option is being used.")
    componentId = zope.interface.Attribute("The componentId of the option.")
    optionId = zope.interface.Attribute("The optionId of the option.")
    
    def get(self, siteId=None, groupId=None):
        """ Fetch the value of the option, further descriminating by the siteId
            and groupId.
        """
        
    def set(self, value, siteId=None, groupId=None):
        """ Set the value of the option, further descriminating by the siteId
            and groupId.
            
            This must both insert missing options, and update options that exist.
        """

class IGSRDBOption(IGSOption):
    pass

class IGSRAMOption(IGSOption):
    pass

