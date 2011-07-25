# coding=utf-8
import sqlalchemy as sa
from sqlalchemy.exceptions import SQLError

class OptionQuery(object):
    def __init__(self, da, componentId, optionId):
        self.optionTable = da.createTable('option')
        self.componentId = componentId
        self.optionId = optionId
        
    def get(self, groupId=None, siteId=None):
        ot = self.optionTable
        s = ot.select()
        
        groupId = groupId or ""
        siteId = siteId or ""
        
        s.append_whereclause(ot.c.component_id==self.componentId)
        s.append_whereclause(ot.c.option_id==self.optionId)
        s.append_whereclause(ot.c.group_id==groupId)
        s.append_whereclause(ot.c.site_id==siteId)
        
        r = s.execute()
        assert (r.rowcount <= 1), "More than one option found matching criteria"
        
        retval = None 
        if r.rowcount:
            retval = unicode(r.fetchone()['value'], "UTF-8")
        
        assert isinstance(retval, unicode)
        
        return retval
        
    def set(self, value, groupId=None, siteId=None):
        assert isinstance(value, unicode), "Value must be unicode"
        
        ot = self.optionTable
        i = ot.insert()
        groupId = groupId or ""
        siteId = siteId or ""
        try:
            i.execute(component_id=self.componentId,
                      option_id=self.optionId,
                      group_id=groupId,
                      site_id=siteId,
                      value=value)
        except SQLError:
            u = ot.update(sa.and_(ot.c.component_id==self.componentId,
                      ot.c.option_id==self.optionId,
                      ot.c.group_id==groupId,
                      ot.c.site_id==siteId))
            u.execute(value=value)