#set PYTHONPATH=.

''' Module for Services models and schemas '''
from sqlalchemy import (Column, String, Integer, DateTime, func, Sequence, ForeignKey, Table)
from labio.database import Base
from sqlalchemy.orm import relationship


class Services_List(Base):
    __tablename__ = 'service_list'
    id = Column(Integer, primary_key=True)
    url = Column(String)

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    entrypoint = Column(String)
    base_url = Column(String)
    doc_url = Column(String)
    svc_end = relationship("Endpoint") 
    svc_sim = relationship("Similar")
    svc_tag = relationship("Tag")
    svc_filter = relationship("Filters")
   
class Endpoints_List(Base):
    __tablename__ = 'endpoints_list'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    service_name = Column(String)
    service_id = Column(Integer,ForeignKey('service.id'))

class Endpoint(Base):
    __tablename__ = 'endpoint'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    label = Column(String)
    template = Column(String)
    description = Column(String)
    parameters = Column(String)
    service_name = Column(String)
    service_id = Column(Integer,ForeignKey('service.id'))

class Similar(Base):
    __tablename__ = 'similar'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    service_id = Column(Integer,ForeignKey('service.id'))

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    service_id = Column(Integer,ForeignKey('service.id'))

class Logs(Base):
    __tablename__ = 'log'
    log_id = Column(Integer, Sequence('log_id_seq'), primary_key=True)
    log_name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    log_status = Column(String) # nao iniciado, rodando, finalizado com sucesso, finalizado com erro
    log_details = relationship("Details")

class Details(Base):
    __tablename__ = 'detail'
    detail_id = Column(Integer, Sequence('detail_id_seq'), primary_key=True)
    detail_name = Column(String, primary_key=True)
    detail_description = Column(String)
    log_id = Column(Integer,ForeignKey('log.log_id'))

class Filters(Base):
    __tablename__ = 'filter'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    description = Column(String)
    service_id = Column(Integer,ForeignKey('service.id'))