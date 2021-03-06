# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2012 NTT DOCOMO, INC.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Session Handling for SQLAlchemy backend."""

from nova.db.sqlalchemy import session as nova_session
from nova.openstack.common import cfg

opts = [
    cfg.StrOpt('baremetal_sql_connection',
               default='sqlite:///$state_path/baremetal_$sqlite_db',
               help='The SQLAlchemy connection string used to connect to the '
                    'bare-metal database'),
    ]

CONF = cfg.CONF
CONF.register_opts(opts)
CONF.import_opt('sqlite_db', 'nova.db.sqlalchemy.session')
CONF.import_opt('state_path', 'nova.config')

_ENGINE = None
_MAKER = None


def get_session(autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy session."""
    global _MAKER

    if _MAKER is None:
        engine = get_engine()
        _MAKER = nova_session.get_maker(engine, autocommit, expire_on_commit)

    session = _MAKER()
    session = nova_session.wrap_session(session)
    return session


def get_engine():
    """Return a SQLAlchemy engine."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = nova_session.create_engine(CONF.baremetal_sql_connection)
    return _ENGINE
