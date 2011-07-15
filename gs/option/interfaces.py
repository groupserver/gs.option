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

class IGSStorageOption(zope.interface.Interface):
    value = zope.schema.Text()