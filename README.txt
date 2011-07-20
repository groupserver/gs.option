Option Lookup
-------------

There are two interfaces involved in an option lookup:

    IGSOption
    IGSOptionConverter

First, an example. To lookup the option "app_id", used by the component
"gs.profile.signup.facebook" we first instantiate an option instance for the
component and option identifier: 

   >>> option = createObject("groupserver.Option",
                             context,
                             'gs.profile.signup.facebook',
                             'app_id')
   >>> value = option.get()
   None
   >>> option.set(21)
   >>> option.get()
   21   
   
Optionally, the get and set methods may also take site and group identifiers,
both of which are independently optional:

   >>> option.get(site_id)
   None
   >>> option.get(site_id, group_id)
   None
   >>> option.set(42, site_id)
   >>> option.set(84, site_id, group_id)
   >>> option.get(site_id, group_id)
   84
   >>> option.get(site_id)
   42
   >>> option.get()
   21

Behind the scenes, gs.profile.signup.facebook.options is a utility defined by:

    from gs.option.converter import GSOptionConverterFactory
    import zope.schema
    import zope.interface

    class IGSProfileSignupFacebookOptions(zope.interface.Interface):
        app_id = zope.schema.Text()
    
    class GSPSFOFactory(GSOptionConverterFactory):
        interface = IGSProfileSignupFacebookOptions
   
With a supporting configure.zcml:

       <utility 
         factory=".interfaces.GSPSFOFactory"
         name="gs.profile.signup.facebook.options" />
         
When the IGSOption utility is instantiated, it locates the named utility matching
the component ID "gs.profile.signup.facebook". The ".options" is appended internally,
and is purely to provide a distinct namespace. This utility locates the schema
matching the option ID (or raises an OptionError), and automatically converts
between the schema type (for example Int), and the backend database type (which
will often be unicode unicode). It also validates the input when converting for
robustness.

The heavy lifting is carried out by the IGSOption utility, using a back end class
where necessary.