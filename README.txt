OUT OF DATE. DOES NOT REFLECT SYSTEM.

Option Lookup
-------------

  gs.option.get(componentId, optionId, siteId=None, groupId=None, default=None)
  
  - lookup optionConverterFactory by componentId
    - call option converter as converter(context, optionId)
    - a failed componentId lookup will return no optionConverter, and the
      default is returned
    - a failed optionId lookup will return gs.option.OptionLookupError
    
  - lookup optionBackendFactory
    - fetch option from backend storage
   
  - convert option
  
  - return
  
  
