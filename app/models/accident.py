from sqlalchemy import Column, Integer, String 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



# Accident Meta Model
class DeAccidentMeta(Base):
    __tablename__ = 'de_accident_meta'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
