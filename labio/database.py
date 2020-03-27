# -*- coding: utf-8 -*-
'''This module contains the database singleton.'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import as_declarative
from labio.config import config
from labio.serializer import setup_serializer

def init():
    ''' Runs all necessary database setup operations '''
    _connect()
    _upgrade_db()
    setup_serializer(Base)

def _connect():
    ''' Connects to the database '''
    global engine
    
    if engine is not None:
        Base.session.remove()
        engine.dispose()

    engine = create_engine(config.DB_SERVER, convert_unicode=True)
    Base.session.configure(bind=engine)

def get_metadata():
    '''Import all modules that define models here!
      Otherwise alembic won't be able to detect database changes automatically'''  
    #from models.models import Services_Final
    #from models.models import Services_Temp
    #from models.models import Endpoints_Final
    #from models.models import Endpoints_Temp
    #from models.models import Log
    #from models.models import Detail
    from models.models import Services_List
    from models.models import Service
    from models.models import Endpoints_List
    from models.models import Endpoint
    from models.models import Tag
    from models.models import Similar
    from models.models import Logs
    from models.models import Details
    from models.models import Filters
    return Base.metadata

def _upgrade_db():
    '''Invokes alembic to bring the database to the latest version'''
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes['configure_logger'] = False
    alembic_cfg.attributes['connection'] = engine
    command.upgrade(alembic_cfg, "head")

engine = None

@as_declarative()
class Base():
    ''' Class to Augment SQL Alchemy Base with utility functions '''

    session: scoped_session = scoped_session(
                                    sessionmaker(
                                        autocommit=False,
                                        autoflush=False,
                                        bind=None
                                    )
                                )
    query: scoped_session.query_property = session.query_property()

    def add(self):
        ''' Insert this object into the database '''
        self.query.session.add(self)

    def merge(self):
        ''' Merge this object into the database '''
        self.query.session.merge(self)

    def delete(self):
        ''' Deletes this object from the database '''
        self.query.session.delete(self)

    @classmethod
    def list_dumps(cls, data: list, *args, **kwargs):
        ''' Dump this list of obj as a string in JSON format '''
        return cls.__marshmallow__(many=True).dumps(data, *args, **kwargs).data

    @classmethod
    def list_dump(cls, data: list, *args, **kwargs):
        ''' Dump this list of obj as a dict '''
        return cls.__marshmallow__(many=True).dump(data, *args, **kwargs).data

    def dumps(self, *args, **kwargs):
        ''' Dump this object as a JSON string '''
        return self.__marshmallow__().dumps(self, *args, **kwargs).data

    def dump(self, *args, **kwargs):
        ''' Dump this object as a dict '''
        return self.__marshmallow__().dump(self, *args, **kwargs).data

    @classmethod
    def loads(cls, data: str, *args, **kwargs):
        ''' Load JSON string into object(s) '''
        return cls.__marshmallow__(many=kwargs.pop('many', False)).loads(data, *args, **kwargs).data

    @classmethod
    def load(cls, data: dict, *args, **kwargs):
        ''' Load dict into object(s) '''
        return cls.__marshmallow__(many=kwargs.pop('many', False)).load(data, *args, **kwargs).data
