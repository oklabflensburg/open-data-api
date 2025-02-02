from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

Base = declarative_base()



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
