# coding=utf-8
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession

class OptionQuery(object):
    def __init__(self, componentId, optionId):
        self.optionTable = getTable('option')
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

        session = getSession()
        r = session.execute(s)
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
        session = getSession()
        try:
            session.begin(subtransactions=True)
            session.execute(i,
                   params={'component_id': self.componentId,
                           'option_id': self.optionId,
                           'group_id': groupId,
                           'site_id': siteId,
                           'value': value})
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            session = getSession()
            session.begin(subtransactions=True)
            u = ot.update(sa.and_(ot.c.component_id==self.componentId,
                      ot.c.option_id==self.optionId,
                      ot.c.group_id==groupId,
                      ot.c.site_id==siteId))

            session.execute(u, params={'value': value})
            session.commit()

