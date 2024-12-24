from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class EnergySourceMeta(Base):
    __tablename__ = 'de_energy_source_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class EnergyCountryMeta(Base):
    __tablename__ = 'de_energy_country_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class NetworkOperatorAuditMeta(Base):
    __tablename__ = 'de_network_operator_audit_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class EnergyLocationMeta(Base):
    __tablename__ = 'de_energy_location_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class EnergySupplyMeta(Base):
    __tablename__ = 'de_energy_supply_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class TurbineManufacturerMeta(Base):
    __tablename__ = 'de_turbine_manufacturer_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class PowerLimitationMeta(Base):
    __tablename__ = 'de_power_limitation_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class PowerTechnologyMeta(Base):
    __tablename__ = 'de_power_technology_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class MainOrientationMeta(Base):
    __tablename__ = 'de_main_orientation_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class OrientationTiltAngleMeta(Base):
    __tablename__ = 'de_orientation_tilt_angle_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class UsageAreaMeta(Base):
    __tablename__ = 'de_usage_area_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class OperationalStatusMeta(Base):
    __tablename__ = 'de_operational_status_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class BiomassTypeMeta(Base):
    __tablename__ = 'de_biomass_type_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)


class PrimaryFuelMeta(Base):
    __tablename__ = 'de_primary_fuel_meta'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
