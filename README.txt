Introduction
============

The ``gs.option`` module is in charge of getting and setting options:
values used by the various instances in GroupServer. The system may
seem complicated, but it is complication born from experience. (We
are fairly sure we did not succumb to the second-system effect!) In
this document we cover `option lookup`_, `declaring options`_, and
`storage and conversion`_.

Option Lookup
=============

An option is made up of three things:

#.  An identifier,
#.  A value, and
#.  A type.

To get a value for an option the code the system specifies the identifier
and the value is returned, set to the correct type.

An option identifier is made up of a module identifier and an
option identifier. These are used to create an instance that can
get the option. For example, to get the ``app_id`` option for the
``gs.profile.signup.facebook`` module the following would be called::

   >>> option = createObject("groupserver.Option",
                             context,
                             'gs.profile.signup.facebook',
                             'app_id')

This creates an ``option`` instance that can get and set values::

   >>> value = option.get()
   None
   >>> option.set(21)
   >>> option.get()
   21   

Option Hierarchy
----------------

Options can live in a hierarchy:

  * GroupServer
    
    + Site
    
      - Group

By default GroupServer options are returned, as in the example above. To
specify a site-specific option the identifier for the site is passed to
either the ``set`` or ``get`` method. For example, using the ``option``
instance that was crated earlier::

   >>> site_id = 'initial_site'
   >>> option.get(site_id)
   None
   >>> option.set(42, site_id)
   >>> option.get(site_id)
   42
   
To specify an option specific to a group the identifier for both the
site **and** group are passed in::

   >>> group_id = 'example_group'
   >>> option.get(site_id, group_id)
   None
   >>> option.set(84, site_id, group_id)
   >>> option.get(site_id, group_id)
   84


Options from different parts of the hierarchy can still be retrieved::

   >>> option.get(site_id)
   42
   >>> option.get()
   21

Component Options
-----------------

Sometimes it is more convenient to handle all the options for a module at
once. In this case the ``ComponentOptions`` can be used. It is similar to
the ``Option`` class except the option identifier is always passed in::

    >>> from gs.option import ComponentOptions
    >>> options = ComponentOptions(self.context, 'gs.profile.signup.facebook')
    >>> options.get('app_id')
    21
    >>> option.get('app_id', site_id)
    42
    >>> options.get('app_id', site_id, group_id)
    84
    >>> options.set('app_id', 9)
    >>> options.get('app_id')
    9

Internally, the ``ComponentOptions`` class uses the same option-factory
as above.

Declaring Options
=================

Each module specifies all the options that it requires. It does this by
`specifying a schema`_ and then `creating an option converter`_.

Specifying a Schema
-------------------

These are specified using standard `Zope schemas`_. For our Facebook
example the ``gs.profile.signup.facebook.options`` the schema starts
with the following::

    import zope.schema
    import zope.interface

    class IGSProfileSignupFacebookOptions(zope.interface.Interface):
        app_id = zope.schema.TextLine(
                    title=u"Application ID as supplied by Facebook",
                    required=True)
    
The same interfaces can be used to document the options, and provide
forms driven by the schemas and `zope.formlib`_ or `z3c.form`_.

Creating an Option Converter
----------------------------

A factory is declared that can return a value cast to the correct type::

    from gs.option.converter import GSOptionConverterFactory

    class GSPSFOFactory(GSOptionConverterFactory):
        interface = IGSProfileSignupFacebookOptions

The base class ``gs.option.converter.GSOptionConverterFactory`` is
used to perform the work of actually casting the value (see `storage
and conversion`_). Finally, some supporting ``ZCML`` turns the factory
into a utility::

       <utility 
         factory=".interfaces.GSPSFOFactory"
         name="gs.profile.signup.facebook.options" />

The name of the utility is looked up by the ``groupserver.Option``
factory, which was called in the first example (in `Option Lookup`_). It
takes the name of the module, such as ``gs.profile.signup.facebook``
and appends ``.options`` to the end to create the name of the utility
for the module.

Storage and Conversion
======================

**Note** For the most part module designers will not have to deal with
options at this level of detail.

Storage and conversion is carried out by the ``groupserver.Option``
class.  This class uses a relational-database backend for storage,
storing values in the ``option`` table as Unicode strings.

The ``groupserver.Option`` class then calls the option converter. The
example above uses the base ``GSOptionConverterFactory`` class to
perform the conversion. This looks up the option identifier in the schema
(specified by the ``interfaces`` class attribute). If the option cannot
be found it raises an ``OptionError``.

The ``GSOptionConverterFactory`` then calls a multi-adaptor to create
a class that can convert between the storage-values and the schema
values. Converters exist for all the standard ``Int``, ``Float``,
``Bool`` and ``Text`` types specified in ``zope.schema``.

.. _Zope schemas: http://docs.zope.org/zope.schema/
.. _zope.formlib: http://docs.zope.org/zope.formlib/
.. _z3c.form: http://plone.org/documentation/manual/plone-community-developer-documentation/forms/z3c.form
