from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional



class DwdStationReference(BaseModel):
    station_name: str
    station_id: str
    identifier: str
    station_code: str
    station_elevation: Optional[int] = None
    river_basin_id: Optional[int] = None
    state_name: str
    recording_start: Optional[str] = None
    recording_end: Optional[str] = None
    geojson: Optional[dict] = None



class WeatherStationResponse(BaseModel):
    station_id: str
    start_date: str
    end_date: str
    station_elevation: Optional[int]
    station_name: Optional[str]
    state_name: Optional[str]
    submission: Optional[str]
    geojson: dict



class DistrictDetails(BaseModel):
    district_name: str
    residents: Optional[int]
    births: int
    age_ratio: float
    age_to_under_18: int
    age_18_to_under_65: int
    age_65_and_above: int
    age_18_to_under_30: int
    age_30_to_under_45: int
    age_45_to_under_65: int
    age_65_to_under_80: int
    age_0_to_under_7: int
    age_60_and_above: int
    age_80_and_above: int
    employed_residents: int
    unemployed_residents: int
    percentage_sgb_iii: Optional[float]
    percentage_sgb_ii: Optional[float]
    percentage_foreign_citizenship: Optional[float]
    percentage_female: Optional[float]
    percentage_age_under_25: Optional[float]
    housing_benefit: int
    notices_of_rent_arrears: Optional[int]
    termination_rent_arrears: Optional[int]
    termination_for_conduct: Optional[int]
    action_for_eviction: Optional[int]
    eviction_notice: Optional[int]
    eviction_carried: Optional[int]
    risk_of_homelessness: Optional[int]
    employable_with_benefits: int
    unemployment_benefits: int
    basic_income: int
    assisting_benefits: int
    beneficiaries_sgbii: int
    unemployability: int
    employability: int
    percentage_females: Optional[float]
    percentage_single_parents: Optional[float]
    percentage_foreign_citizenship: Optional[float]
    unemployed_beneficiaries: int
    male_basic_beneficiaries: int
    female_basic_beneficiaries: int
    age_18_to_under_65_basic_beneficiaries: int
    age_65_and_above_basic_beneficiaries: int
    foreign_citizenship: int
    german_citizenship: int


class District(BaseModel):
    district_id: int
    district_name: Optional[str]


class Districts(District):
    districts: list[District]


class HouseholdType(BaseModel):
    household_id: Optional[int]
    household_type: Optional[str]


class HouseholdTypes(HouseholdType):
    pass


class ResidentsByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ResidentsByDistricts(ResidentsByDistrict):
    pass


class BirthsByDistrict(BaseModel):
    year: int
    district_id: int
    births: Optional[int]
    birth_rate: Optional[float]


class BirthsByDistricts(BirthsByDistrict):
    pass


class AgeGroupsOfResidents(BaseModel):
    year: int
    age_under_18: Optional[int]
    age_18_to_under_30: Optional[int]
    age_30_to_under_45: Optional[int]
    age_45_to_under_65: Optional[int]
    age_65_to_under_80: Optional[int]
    age_80_and_above: Optional[int]


class AgeRatioByDistrict(BaseModel):
    year: int
    district_id: int
    quotient: Optional[float]


class AgeRatioByDistricts(AgeRatioByDistrict):
    pass


class AgeGroupsOfResidentsByDistrict(BaseModel):
    year: int
    district_id: int
    age_under_18: Optional[int]
    age_18_to_under_30: Optional[int]
    age_30_to_under_45: Optional[int]
    age_45_to_under_65: Optional[int]
    age_65_to_under_80: Optional[int]
    age_80_and_above: Optional[int]
    age_0_to_under_7: Optional[int]
    age_60_and_above: Optional[int]


class AgeGroupsOfResidentsByDistrict(AgeGroupsOfResidentsByDistrict):
    pass


class ChildrenAgeUnder18ByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ChildrenAgeUnder18ByDistricts(ChildrenAgeUnder18ByDistrict):
    pass


class ResidentsAge18ToUnder65ByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ResidentsAge18ToUnder65ByDistricts(ResidentsAge18ToUnder65ByDistrict):
    pass


class ResidentsAge65AndAboveByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ResidentsAge65AndAboveByDistricts(ResidentsAge65AndAboveByDistrict):
    pass


class MigrationBackgroundByDistrict(BaseModel):
    year: int
    district_id: int
    foreign_citizenship: Optional[int]
    german_citizenship: Optional[int]


class MigrationBackgroundByDistricts(MigrationBackgroundByDistrict):
    pass


class NonGermanNationalsResidenceStatus(BaseModel):
    year: Optional[int]
    permanent_residency: Optional[int]
    permanent_residency_according_eu_freedom_movement_act: Optional[int]
    permanent_residency_third_country_nationality: Optional[int]
    without_permanent_residency: Optional[int]
    asylum_seeker: Optional[int]
    suspension_of_deportation: Optional[int]


class EmployedWithPensionInsuranceByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]
    employment_rate: Optional[float]


class EmployedWithPensionInsuranceByDistricts(EmployedWithPensionInsuranceByDistrict):
    pass


class UnemployedResidentsByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class UnemployedResidentsByDistricts(UnemployedResidentsByDistrict):
    pass


class UnemployedCategorizedResidentsByDistrict(BaseModel):
    year: int
    district_id: Optional[int]
    unemployed_total: Optional[int]
    percentage_of_total: Optional[float]
    percentage_sgb_iii: Optional[float]
    percentage_sgb_ii: Optional[float]
    percentage_foreign_citizenship: Optional[float]
    percentage_female: Optional[float]
    percentage_age_under_25: Optional[float]


class UnemployedCategorizedResidentsByDistricts(UnemployedCategorizedResidentsByDistrict):
    pass


class HousingBenefitByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class HousingBenefitByDistricts(HousingBenefitByDistrict):
    pass


class HousingAssistanceCasesByDistrict(BaseModel):
    year: int
    district_id: int
    general_consulting: Optional[int]
    notices_of_rent_arrears: Optional[int]
    termination_rent_arrears: Optional[int]
    termination_for_conduct: Optional[int]
    action_for_eviction: Optional[int]
    eviction_notice: Optional[int]
    eviction_carried: Optional[int]


class HousingAssistanceCasesByDistricts(HousingAssistanceCasesByDistrict):
    pass


class HouseholdsAtRiskOfHomelessnessByDistrict(BaseModel):
    year: Optional[int]
    district_id: int
    residents: Optional[int]


class HouseholdsAtRiskOfHomelessnessByDistricts(HouseholdsAtRiskOfHomelessnessByDistrict):
    pass


class BeneficiariesAge15ToUnder65ByDistrict(BaseModel):
    year: int
    district_id: Optional[int]
    percentage_of_total_residents: Optional[float]
    employable_with_benefits: Optional[int]
    unemployment_benefits: Optional[int]
    basic_income: Optional[int]
    assisting_benefits: Optional[int]


class BeneficiariesAge15ToUnder65ByDistricts(BeneficiariesAge15ToUnder65ByDistrict):
    pass


class BeneficiariesByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class BeneficiariesByDistricts(BeneficiariesByDistrict):
    pass


class BeneficiariesCharacteristicsByDistrict(BaseModel):
    year: int
    district_id: Optional[int]
    unemployability: Optional[int]
    employability: Optional[int]
    percentage_females: Optional[float]
    percentage_single_parents: Optional[float]
    percentage_foreign_citizenship: Optional[float]


class BeneficiariesCharacteristicsByDistricts(BeneficiariesCharacteristicsByDistrict):
    pass


class InactiveBeneficiariesInHouseholdsByDistrict(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class InactiveBeneficiariesInHouseholdsByDistricts(InactiveBeneficiariesInHouseholdsByDistrict):
    pass


class BasicBenefitsIncomeByDistrict(BaseModel):
    year: int
    district_id: Optional[int]
    male: Optional[int]
    female: Optional[int]
    age_18_to_under_65: Optional[int]
    age_65_and_above: Optional[int]


class BasicBenefitsIncomeByDistricts(BasicBenefitsIncomeByDistrict):
    pass


class DebtCounselingOfResidents(BaseModel):
    year: int
    household_type_id: Optional[int]
    residents: Optional[int]


class ChildEducationSupport(BaseModel):
    year: int
    educational_assistance: Optional[int]
    parenting_counselor: Optional[int]
    pedagogical_family_assistance: Optional[int]
    child_day_care_facility: Optional[int]
    full_time_care: Optional[int]
    residential_education: Optional[int]
    integration_assistance: Optional[int]
    additional_support: Optional[int]
