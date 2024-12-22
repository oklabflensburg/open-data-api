from sqlalchemy import CheckConstraint, Column, ForeignKey, Index, Integer, SmallInteger, Numeric, String, TIMESTAMP, Date, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()
metadata = Base.metadata



class Vg250Gem(Base):
    __tablename__ = 'vg250_gem'

    id = Column(Integer, primary_key=True, nullable=False)
    objid = Column(String)
    beginn = Column(TIMESTAMP(timezone=True))
    ade = Column(SmallInteger)
    gf = Column(SmallInteger)
    bsg = Column(SmallInteger)
    ars = Column(String)
    ags = Column(String)
    sdv_ars = Column(String)
    gen = Column(String)
    bez = Column(String)
    ibz = Column(SmallInteger)
    bem = Column(String)
    nbd = Column(String)
    sn_l = Column(String)
    sn_r = Column(String)
    sn_k = Column(String)
    sn_v1 = Column(String)
    sn_v2 = Column(String)
    sn_g = Column(String)
    fk_s3 = Column(String)
    nuts = Column(String)
    ars_0 = Column(String)
    ags_0 = Column(String)
    wsk = Column(TIMESTAMP(timezone=True))
    ewz = Column(Integer)
    kfl = Column(Numeric)
    dlm_id = Column(String)
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))



class DwdStationReference(Base):
    __tablename__ = 'dwd_station_reference'

    id = Column(Integer, primary_key=True)
    station_name = Column(String, nullable=False)
    station_id = Column(String, nullable=False, unique=True)
    identifier = Column(String, nullable=False)
    station_code = Column(String, nullable=False)
    station_latitude = Column(Numeric)
    station_longitude = Column(Numeric)
    station_elevation = Column(Integer)
    river_basin_id = Column(Integer)
    state_name = Column(String, nullable=False)
    recording_start = Column(Date)
    recording_end = Column(Date)
    wkb_geometry = Column(Geometry('POINT', srid=4326))



class WeatherStation(Base):
    __tablename__ = 'de_weather_stations'

    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False, unique=True)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    station_elevation = Column(Integer)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    station_name = Column(String)
    state_name = Column(String)
    submission = Column(String)
    wkb_geometry = Column(Geometry('POINT', srid=4326))



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



class Monument(Base):
    __tablename__ = 'sh_monuments'

    id = Column(Integer, primary_key=True)
    object_id = Column(String)
    address = Column(String)
    image_url = Column(String)
    designation = Column(String)
    description = Column(String)
    administrative = Column(String)
    monument_type = Column(String)
    postal_code = Column(String)
    place_name = Column(String)
    wkb_geometry = Column(Geometry)



# District Model
class District(Base):
    __tablename__ = 'fl_district'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    wkb_geometry = Column(Geometry('POLYGON', srid=4326))

    # Relationships
    residents_by_district = relationship('ResidentsByDistrict', back_populates='district')
    basic_benefits_income_by_district = relationship('BasicBenefitsIncomeByDistrict', back_populates='district')
    births_by_district = relationship('BirthsByDistrict', back_populates='district')
    age_ratios_by_district = relationship('AgeRatioByDistrict', back_populates='district')
    children_age_under_18_by_district = relationship('ChildrenAgeUnder18ByDistrict', back_populates='district')
    risk_homelessness_by_district = relationship('HouseholdsRiskOfHomelessnessByDistrict', back_populates='district')
    housing_benefit_by_district = relationship('HousingBenefitByDistrict', back_populates='district')
    beneficiaries_age_15_to_under_65_by_district = relationship('BeneficiariesAge15ToUnder65ByDistrict', back_populates='district')
    beneficiaries_characteristics_by_district = relationship('BeneficiariesCharacteristicsByDistrict', back_populates='district')


# Household Type Model
class HouseholdType(Base):
    __tablename__ = 'fl_household_type'

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)


# Residents by District Model
class ResidentsByDistrict(Base):
    __tablename__ = 'fl_residents_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District', back_populates='residents_by_district')


# Basic Benefits Income by Districts Model
class BasicBenefitsIncomeByDistrict(Base):
    __tablename__ = 'fl_basic_benefits_income_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    male = Column(Integer)
    female = Column(Integer)
    age_18_to_under_65 = Column(Integer)
    age_65_and_above = Column(Integer)

    district = relationship('District', back_populates='basic_benefits_income_by_district')


# Children Age Under 18 by Districts Model
class ChildrenAgeUnder18ByDistrict(Base):
    __tablename__ = 'fl_children_age_under_18_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District', back_populates='children_age_under_18_by_district')


# Births by District Model
class BirthsByDistrict(Base):
    __tablename__ = 'fl_births_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    births = Column(Integer)
    birth_rate = Column(Numeric)

    district = relationship('District', back_populates='births_by_district')


# Housing Benefit by Districts Model
class HousingBenefitByDistrict(Base):
    __tablename__ = 'fl_housing_benefit_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District', back_populates='housing_benefit_by_district')


# Age Groups of Residents Model
class AgeGroupsOfResidents(Base):
    __tablename__ = 'fl_age_groups_of_residents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    age_under_18 = Column(Integer)
    age_18_to_under_30 = Column(Integer)
    age_30_to_under_45 = Column(Integer)
    age_45_to_under_65 = Column(Integer)
    age_65_to_under_80 = Column(Integer)
    age_80_and_above = Column(Integer)


# Age Ratio by District Model
class AgeRatioByDistrict(Base):
    __tablename__ = 'fl_age_ratio_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'), nullable=True)
    quotient = Column(Numeric)

    district = relationship('District', back_populates='age_ratios_by_district')


# Households at Risk of Homelessness by Districts Model
class HouseholdsRiskOfHomelessnessByDistrict(Base):
    __tablename__ = 'fl_risk_homelessness_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District', back_populates='risk_homelessness_by_district')


# Beneficiaries Age 15 to Under 65 by Districts Model
class BeneficiariesAge15ToUnder65ByDistrict(Base):
    __tablename__ = 'fl_beneficiaries_age_15_to_under_65_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    total = Column(Integer)
    percentage_of_total_residents = Column(Numeric)
    employable_with_benefits = Column(Integer)
    unemployment_benefits = Column(Integer)
    basic_income = Column(Integer)
    assisting_benefits = Column(Integer)

    district = relationship('District', back_populates='beneficiaries_age_15_to_under_65_by_district')


# Beneficiaries Characteristics by Districts Model
class BeneficiariesCharacteristicsByDistrict(Base):
    __tablename__ = 'fl_beneficiaries_characteristics_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    unemployability = Column(Integer)
    employability = Column(Integer)
    percentage_females = Column(Numeric)
    percentage_single_parents = Column(Numeric)
    percentage_foreign_citizenship = Column(Numeric)

    district = relationship('District', back_populates='beneficiaries_characteristics_by_district')


# Unemployed Residents Categorized by District Model
class UnemployedResidentsCategorizedByDistrict(Base):
    __tablename__ = 'fl_unemployed_residents_categorized_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    unemployed_total = Column(Integer)
    percentage_of_total = Column(Numeric)
    percentage_sgb_iii = Column(Numeric)
    percentage_sgb_ii = Column(Numeric)
    percentage_foreign_citizenship = Column(Numeric)
    percentage_female = Column(Numeric)
    percentage_age_under_25 = Column(Numeric)

    district = relationship('District')


# Inactive Beneficiaries in Households by Districts Model
class InactiveBeneficiariesInHouseholdsByDistrict(Base):
    __tablename__ = 'fl_inactive_beneficiaries_in_households_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District')


# Beneficiaries by Districts Model
class BeneficiariesByDistrict(Base):
    __tablename__ = 'fl_beneficiaries_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District')


# Age Groups of Residents by District Model
class AgeGroupsOfResidentsByDistrict(Base):
    __tablename__ = 'fl_age_groups_of_residents_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    age_under_18 = Column(Integer)
    age_18_to_under_30 = Column(Integer)
    age_30_to_under_45 = Column(Integer)
    age_45_to_under_65 = Column(Integer)
    age_65_to_under_80 = Column(Integer)
    age_80_and_above = Column(Integer)
    age_0_to_under_7 = Column(Integer)
    age_60_and_above = Column(Integer)

    district = relationship('District')


# Residents Age 65 and Above by District Model
class ResidentsAge65AndAboveByDistrict(Base):
    __tablename__ = 'fl_residents_age_65_and_above_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District')


# Residents Age 18 and Under 65 by District Model
class ResidentsAge18ToUnder65ByDistrict(Base):
    __tablename__ = 'fl_residents_age_18_to_under_65_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'), nullable=False)
    residents = Column(Integer, nullable=True)

    district = relationship('District')


# Migration Background by District Model
class MigrationBackgroundByDistrict(Base):
    __tablename__ = 'fl_migration_background_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    foreign_citizenship = Column(Integer)
    german_citizenship = Column(Integer)

    district = relationship('District')


# Non-German Nationals Residence Status Model
class NonGermanNationalsResidenceStatus(Base):
    __tablename__ = 'fl_non_german_nationals_residence_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    permanent_residency = Column(Integer)
    permanent_residency_according_eu_freedom_movement_act = Column(Integer)
    permanent_residency_third_country_nationality = Column(Integer)
    without_permanent_residency = Column(Integer)
    asylum_seeker = Column(Integer)
    suspension_of_deportation = Column(Integer)


# Employed with Pension Insurance by District Model
class EmployedWithPensionInsuranceByDistrict(Base):
    __tablename__ = 'fl_employed_with_pension_insurance_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)
    employment_rate = Column(Numeric)

    district = relationship('District')


# Unemployed Residents by District Model
class UnemployedResidentsByDistrict(Base):
    __tablename__ = 'fl_unemployed_residents_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    residents = Column(Integer)

    district = relationship('District')


# Housing Assistance Cases by Districts Model
class HousingAssistanceCasesByDistrict(Base):
    __tablename__ = 'fl_housing_assistance_cases_by_district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey('fl_district.id'))
    general_consulting = Column(Integer)
    notices_of_rent_arrears = Column(Integer)
    termination_rent_arrears = Column(Integer)
    termination_for_conduct = Column(Integer)
    action_for_eviction = Column(Integer)
    eviction_notice = Column(Integer)
    eviction_carried = Column(Integer)

    district = relationship('District')


# Debt Counseling Residents Model
class DebtCounselingOfResidents(Base):
    __tablename__ = 'fl_debt_counseling_residents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    household_type_id = Column(Integer, ForeignKey('fl_household_type.id'))
    residents = Column(Integer)

    household_type = relationship('HouseholdType')


# Child Education Support Model
class ChildEducationSupport(Base):
    __tablename__ = 'fl_child_education_support'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    educational_assistance = Column(Integer)
    parenting_counselor = Column(Integer)
    pedagogical_family_assistance = Column(Integer)
    child_day_care_facility = Column(Integer)
    full_time_care = Column(Integer)
    residential_education = Column(Integer)
    integration_assistance = Column(Integer)
    additional_support = Column(Integer)
