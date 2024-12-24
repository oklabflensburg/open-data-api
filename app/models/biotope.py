from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class ShBiotopeOrigin(Base):
    __tablename__ = 'sh_biotope_origin'
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    description = Column(String, nullable=True)
    remark = Column(String, nullable=True)


class DeHabitatTypes(Base):
    __tablename__ = 'de_habitat_types'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    priority = Column(Boolean, nullable=False)
    description = Column(String, nullable=True)
    label = Column(String, nullable=True)