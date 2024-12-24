from pydantic import BaseModel
from typing import Optional


class DistrictDetailsResponse(BaseModel):
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


class DistrictResponse(BaseModel):
    district_id: int
    district_name: Optional[str]


class DistrictsResponse(DistrictResponse):
    pass


class HouseholdTypeResponse(BaseModel):
    household_id: Optional[int]
    household_type: Optional[str]


class ResidentsByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ResidentsResponse(ResidentsByDistrictResponse):
    pass


class BirthsByDistrictResponse(BaseModel):
    year: int
    district_id: int
    births: Optional[int]
    birth_rate: Optional[float]


class BirthsResponse(BirthsByDistrictResponse):
    pass


class AgeGroupsOfResidentsResponse(BaseModel):
    year: int
    age_under_18: Optional[int]
    age_18_to_under_30: Optional[int]
    age_30_to_under_45: Optional[int]
    age_45_to_under_65: Optional[int]
    age_65_to_under_80: Optional[int]
    age_80_and_above: Optional[int]


class AgeRatioByDistrictResponse(BaseModel):
    year: int
    district_id: int
    quotient: Optional[float]


class AgeRatioResponse(AgeRatioByDistrictResponse):
    pass


class AgeGroupsOfResidentsByDistrictResponse(BaseModel):
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


class AgeGroupsOfResidentsByDistrictResponse(AgeGroupsOfResidentsByDistrictResponse):
    pass


class ChildrenAgeUnder18ByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ChildrenAgeUnder18Response(ChildrenAgeUnder18ByDistrictResponse):
    pass


class ResidentsAge18ToUnder65ByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ResidentsAge18ToUnder65Response(ResidentsAge18ToUnder65ByDistrictResponse):
    pass


class ResidentsAge65AndAboveByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class ResidentsAge65AndAboveResponse(ResidentsAge65AndAboveByDistrictResponse):
    pass


class MigrationBackgroundByDistrictResponse(BaseModel):
    year: int
    district_id: int
    foreign_citizenship: Optional[int]
    german_citizenship: Optional[int]


class MigrationBackgroundResponse(MigrationBackgroundByDistrictResponse):
    pass


class NonGermanNationalsResidenceStatusResponse(BaseModel):
    year: Optional[int]
    permanent_residency: Optional[int]
    permanent_residency_according_eu_freedom_movement_act: Optional[int]
    permanent_residency_third_country_nationality: Optional[int]
    without_permanent_residency: Optional[int]
    asylum_seeker: Optional[int]
    suspension_of_deportation: Optional[int]


class EmployedWithPensionInsuranceByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]
    employment_rate: Optional[float]


class EmployedWithPensionInsuranceResponse(EmployedWithPensionInsuranceByDistrictResponse):
    pass


class UnemployedResidentsByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class UnemployedResidentsResponse(UnemployedResidentsByDistrictResponse):
    pass


class UnemployedResidentsCategorizedByDistrictResponse(BaseModel):
    year: int
    district_id: Optional[int]
    unemployed_total: Optional[int]
    percentage_of_total: Optional[float]
    percentage_sgb_iii: Optional[float]
    percentage_sgb_ii: Optional[float]
    percentage_foreign_citizenship: Optional[float]
    percentage_female: Optional[float]
    percentage_age_under_25: Optional[float]


class UnemployedCategorizedResidentsResponse(UnemployedResidentsCategorizedByDistrictResponse):
    pass


class HousingBenefitByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class HousingBenefitResponse(HousingBenefitByDistrictResponse):
    pass


class HousingAssistanceCasesByDistrictResponse(BaseModel):
    year: int
    district_id: int
    general_consulting: Optional[int]
    notices_of_rent_arrears: Optional[int]
    termination_rent_arrears: Optional[int]
    termination_for_conduct: Optional[int]
    action_for_eviction: Optional[int]
    eviction_notice: Optional[int]
    eviction_carried: Optional[int]


class HousingAssistanceCasesResponse(HousingAssistanceCasesByDistrictResponse):
    pass


class HouseholdsRiskOfHomelessnessByDistrictResponse(BaseModel):
    year: Optional[int]
    district_id: int
    residents: Optional[int]


class HouseholdsAtRiskOfHomelessnessResponse(HouseholdsRiskOfHomelessnessByDistrictResponse):
    pass


class BeneficiariesAge15ToUnder65ByDistrictResponse(BaseModel):
    year: int
    district_id: Optional[int]
    percentage_of_total_residents: Optional[float]
    employable_with_benefits: Optional[int]
    unemployment_benefits: Optional[int]
    basic_income: Optional[int]
    assisting_benefits: Optional[int]


class BeneficiariesAge15ToUnder65Response(BeneficiariesAge15ToUnder65ByDistrictResponse):
    pass


class BeneficiariesByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class BeneficiariesResponse(BeneficiariesByDistrictResponse):
    pass


class BeneficiariesCharacteristicsByDistrictResponse(BaseModel):
    year: int
    district_id: Optional[int]
    unemployability: Optional[int]
    employability: Optional[int]
    percentage_females: Optional[float]
    percentage_single_parents: Optional[float]
    percentage_foreign_citizenship: Optional[float]


class BeneficiariesCharacteristicsResponse(BeneficiariesCharacteristicsByDistrictResponse):
    pass


class InactiveBeneficiariesInHouseholdsByDistrictResponse(BaseModel):
    year: int
    district_id: int
    residents: Optional[int]


class InactiveBeneficiariesInHouseholdsResponse(InactiveBeneficiariesInHouseholdsByDistrictResponse):
    pass


class BasicBenefitsIncomeByDistrictResponse(BaseModel):
    year: int
    district_id: Optional[int]
    male: Optional[int]
    female: Optional[int]
    age_18_to_under_65: Optional[int]
    age_65_and_above: Optional[int]


class BasicBenefitsIncomeResponse(BasicBenefitsIncomeByDistrictResponse):
    pass


class DebtCounselingOfResidentsResponse(BaseModel):
    year: int
    household_type_id: Optional[int]
    residents: Optional[int]


class ChildEducationSupportResponse(BaseModel):
    year: int
    educational_assistance: Optional[int]
    parenting_counselor: Optional[int]
    pedagogical_family_assistance: Optional[int]
    child_day_care_facility: Optional[int]
    full_time_care: Optional[int]
    residential_education: Optional[int]
    integration_assistance: Optional[int]
    additional_support: Optional[int]
