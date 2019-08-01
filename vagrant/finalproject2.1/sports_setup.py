import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Catagory(Base):
    __tablename__ = 'catagory'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class equipment(Base):
    __tablename__ = 'equipment_item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    Catagory_id = Column(Integer,ForeignKey('catagory.id'))
    catagory = relationship(Catagory)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):

       return {
           'name': self.name,
           'description': self.description,
           'id': self.id,
           'price': self.price,

       }


engine = create_engine('sqlite:///sport.db')


Base.metadata.create_all(engine)
