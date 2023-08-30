from typing import Optional
from pydantic import BaseModel


class District(BaseModel):
    district_id: Optional[int]
    district_name: Optional[str]


class Districts(District):
    districts: Optional[District]


class HouseholdType(BaseModel):
    id: Optional[int]
    label: Optional[str]


class ResidentsByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class BirthsByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    births: Optional[int]
    birth_rate: Optional[float]


class AgeGroupsOfResidents(BaseModel):
    id: Optional[int]
    year: int
    age_under_18: Optional[int]
    age_18_to_under_30: Optional[int]
    age_30_to_under_45: Optional[int]
    age_45_to_under_65: Optional[int]
    age_65_to_under_80: Optional[int]
    age_80_and_above: Optional[int]


class AgeRatioByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    quotient: Optional[int]


class AgeGroupsOfResidentsByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    age_under_18: Optional[int]
    age_18_to_under_30: Optional[int]
    age_30_to_under_45: Optional[int]
    age_45_to_under_65: Optional[int]
    age_65_to_under_80: Optional[int]
    age_80_and_older: Optional[int]
    age_0_to_under_7: Optional[int]
    age_60_and_older: Optional[int]


class ChildrenAgeUnder18ByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class ResidentsAge18ToUnder65ByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class ResidentsAge65AndAboveByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class MigrationBackgroundByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    foreign_citizenship: Optional[int]
    german_citizenship: Optional[int]


class NonGermanNationalsResidenceStatus(BaseModel):
    id: Optional[int]
    year: Optional[int]
    permanent_residency: Optional[int]
    permanent_residency_according_eu_freedom_movement_act: Optional[int]
    permanent_residency_third_country_nationality: Optional[int]
    without_permanent_residency: Optional[int]
    asylum_seeker: Optional[int]
    suspension_of_deportation: Optional[int]


class EmployedWithPensionInsuranceByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]
    employment_rate: Optional[float]


class UnemployedResidentsByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class UnemployedResidentsByDistrictsCategorized(BaseModel):
    id: Optional[int]
    year: Optional[int]
    district_id: Optional[int]
    total: Optional[int]
    unemployed_total: Optional[int]
    percentage_of_total: Optional[float]
    percentage_sgb_iii: Optional[float]
    percentage_sgb_ii: Optional[float]
    percentage_foreign_citizenship: Optional[float]
    percentage_female: Optional[float]
    percentage_age_under_25: Optional[float]


class HousingBenefitByDistricts(BaseModel):
    id: Optional[int]
    year: Optional[int]
    district_id: Optional[int]
    residents: Optional[int]


class HousingAssistanceCasesByDistricts(BaseModel):
    id: Optional[int]
    year: Optional[int]
    district_id: Optional[int]
    general_consulting: Optional[int]
    notices_of_rent_arrears: Optional[int]
    termination_rent_arrears: Optional[int]
    termination_for_conduct: Optional[int]
    action_for_eviction: Optional[int]
    eviction_notice: Optional[int]
    eviction_carried: Optional[int]


class HouseholdsAtRiskOfHomelessnessByDistricts(BaseModel):
    id: Optional[int]
    year: Optional[int]
    district_id: Optional[int]
    residents: Optional[int]


class BeneficiariesAge15ToUnder65ByDistricts(BaseModel):
    id: Optional[int]
    year: Optional[int]
    district_id: Optional[int]
    total: Optional[int]
    percentage_of_total_residents: Optional[float]
    employable_with_benefits: Optional[int]
    unemployment_benefits: Optional[int]
    basic_income: Optional[int]
    assisting_benefits: Optional[int]


class BeneficiariesByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class BeneficiariesCharacteristicsByDistricts(BaseModel):
    id: Optional[int]
    district_id: Optional[int]
    year: Optional[int]
    unemployability: Optional[int]
    employability: Optional[int]
    percentage_females: Optional[float]
    percenatage_single_parents: Optional[float]
    percentage_foreign_citizenship: Optional[float]


class InactiveBeneficiariesInHouseholdsByDistricts(BaseModel):
    id: Optional[int]
    year: int
    district_id: Optional[int]
    residents: Optional[int]


class BasicBenefitsIncomeByDistricts(BaseModel):
    id: Optional[int]
    year: Optional[int]
    district_id: Optional[int]
    male: Optional[int]
    female: Optional[int]
    age_18_to_under_65: Optional[int]
    age_65_and_above: Optional[int]


class DebtCounselingResidents(BaseModel):
    id: Optional[int]
    year: Optional[int]
    household_type_id: Optional[int]
    residents: Optional[int]


class ChildEducationSupport(BaseModel):
    id: Optional[int]
    year: Optional[int]
    educational_assistance: Optional[int]
    parenting_counselor: Optional[int]
    pedagogical_family_assistance: Optional[int]
    child_day_care_facility: Optional[int]
    full_time_care: Optional[int]
    residential_education: Optional[int]
    integration_assistance: Optional[int]
    additional_support: Optional[int]
