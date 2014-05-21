# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals

DATABASE_USER = "gstestdbbeta3pre1user"  # Can these be made random?
DATABASE_NAME = "gstestdbbeta3pre1"

dbSetupDone = False

from commands import getstatusoutput as execute
import sys
import os


def dbsetup():
    m = "setting up database {0} with user {1}\n"
    msg = m.format(DATABASE_NAME, DATABASE_USER)
    sys.stdout.write(msg)
    code, result = execute("createdb -U%s %s" % (DATABASE_USER, DATABASE_NAME))
    if code:
        m = "{0}\nDatabase either already existed, or some other error "\
            "occurred.\n"
        msg = m.format(m)
        sys.stdout.write(msg)
        sys.exit(1)


def dbTable(module, filename, dropTables=[]):
    path = module.__path__[0]
    sql_filepath = os.path.join(path, filename)
    for table in dropTables:
        msg = "dropping table %s\n" % table
        sys.stdout.write(msg)
        c = "echo 'drop table {0}' | psql -U{1} {2}"
        command = c.format(table, DATABASE_USER, DATABASE_NAME)
        execute(command)
    sys.stdout.write("setting up table\n")
    code, result = execute("cat %s | psql -U%s %s" % (sql_filepath,
                                                DATABASE_USER, DATABASE_NAME))
    if code:
        m = "{0}\nDatabase either already existed, or some other error "\
            "occurred.\n"
        msg = m.format(m)
        sys.stdout.write(msg)
        sys.exit(2)


def dbteardown():
    msg = "destroying database %s\n" % DATABASE_NAME
    sys.stdout.write(msg)
    code, result = execute("dropdb -U%s %s" % (DATABASE_USER, DATABASE_NAME))
    if code:
        m = "{0}\nDatabase already destroyed, or some other error occurred.\n"
        msg = m.format(m)
        sys.stdout.write(msg)
        sys.exit(3)
