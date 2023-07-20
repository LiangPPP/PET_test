import pandas as pd
from PETWorks.autoturn import findQualifiedAnonymityConfigs
from PETWorks.autoturn import generateAnonymityConfigs
from PETWorks.attributetypes import *

# generateAnonymityConfigs(
#     originalData="data/sport/sport_prepossed.csv",
#     dataHierarchy="data/sport/sport_hierarchy",
#     output="combination_.csv",
#     firstSampleCount=3,
#     secondSampleCount=3
# )


def twoMinuteStepTest(data: pd.DataFrame) -> float:
    return data.loc[data["subtype"] == "2MinuteStepTest"][
        "achievement_count"
    ].astype(int).mean()


def armCurlTest(data: pd.DataFrame):
    return data.loc[data["subtype"] == "30SecondArmCurlTest"][
        "achievement_count"
    ].astype(int).mean()


def charStandTest(data: pd.DataFrame):
    return data.loc[data["subtype"] == "ChairStandTest"][
        "achievement_count"
    ].astype(int).mean()


def footUpAndGoTest(data: pd.DataFrame):
    return data.loc[data["subtype"] == "8FootUpAndGoTest"][
        "elapsed_time"
    ].astype(float).mean()


def rightHand(data: pd.DataFrame):
    return data.loc[data["subtype"] == "RightHandGripStrengthTest"][
        "upper_extremity_muscle_strength"
    ].astype(float).mean()


def singleLegBalanceRight(data: pd.DataFrame):
    return data.loc[data["subtype"] == "SingleLegBalanceRight"][
        "elapsed_time"
    ].astype(float).mean()


def singleLegBalanceLeft(data: pd.DataFrame):
    return data.loc[data["subtype"] == "SingleLegBalanceLeft"][
        "elapsed_time"
    ].astype(float).mean()

def filter_originalData_by_age_and_gender(
    data: pd.DataFrame, range1: int, range2: int, gender: str
):
    if gender is None:
        return data[
            (data["birth_year"].astype(int) >= range1)
            & (data["birth_year"].astype(int) <= range2)
        ]
    return data[
        (data["birth_year"].astype(int) >= range1)
        & (data["birth_year"].astype(int) <= range2)
        & (data["gender"].astype(str) == gender)
    ]


def filter_anonymizedData_by_age_and_gender(
    data: pd.DataFrame, age_range: str, gender: str
):
    if gender is None:
        return data[
            (data["birth_year"].astype(str) == age_range)
        ]
    return data[
        (data["birth_year"].astype(str) == age_range) & (data["gender"].astype(str) == gender)
    ]


def analyze(
    originalData: pd.DataFrame, anonymizedData: pd.DataFrame ,error:int
):                            
    FT = 1                                 
    originalData.columns = originalData.columns.str.strip()
    
    for column in originalData.columns:
        if originalData[column].dtype == 'object':
            originalData[column] = originalData[column].str.strip()
    
    age_ranges = [(1930, 1940), (1940, 1950), (1950, 1960), (1960, 1970)]
    genders = ['女', '男', None]
    tests = [
        twoMinuteStepTest,
        armCurlTest,
        charStandTest,
        footUpAndGoTest,
        rightHand,
        singleLegBalanceRight,
        singleLegBalanceLeft,
    ]
    
    for age_range in age_ranges:
            
        for gender in genders:
            
            od_filtered = filter_originalData_by_age_and_gender(originalData,age_range[0],age_range[1],gender)
            ad_filtered = filter_anonymizedData_by_age_and_gender(anonymizedData,f"[{age_range[0]}-{age_range[1]}]",gender)
            
            
            for test in tests:
                od_result = test(od_filtered)
                ad_result = test(ad_filtered)
                
                difference = abs(od_result - ad_result)
                
                bias = 4
                
                if test.__name__ == "twoMinuteStepTest":
                    bias = 10
                    
                if difference < bias:
                    print(f"{test.__name__} pass for age range {age_range} and gender {gender if gender is not None else 'All'}")
                else:
                    print(f"{test.__name__} {gender} fail")
                    print(f"{od_result} - {ad_result} = {difference}")
                    print(bias)
                    

                
original = pd.read_csv("test_od.csv",sep=',')
anonymized = pd.read_csv("test_ad.csv",sep=',')
print(analyze(original,anonymized,4))
    # originalData1950.to_csv('test0509.csv',index=False)




# findQualifiedAnonymityConfigs(
#     originalData="data/sport/sport_prepossed.csv",
#     dataHierarchy="data/sport/sport_hierarchy",
#     anonymityConfigs="combination.csv",
#     attributeTypes={
#         "_id": IDENTIFIER,
#         "achievement_count": SENSITIVE_ATTRIBUTE,
#         "birth_year": QUASI_IDENTIFIER,
#         "city": SENSITIVE_ATTRIBUTE,
#         "elapsed_time": SENSITIVE_ATTRIBUTE,
#         "gender": SENSITIVE_ATTRIBUTE,
#         "main_type": SENSITIVE_ATTRIBUTE,
#         "start_date": QUASI_IDENTIFIER,
#         "subtype": SENSITIVE_ATTRIBUTE,
#         "type": SENSITIVE_ATTRIBUTE,
#         "upper_extremity_muscle_strength": SENSITIVE_ATTRIBUTE,
#         "user_id": SENSITIVE_ATTRIBUTE,
#     },
#     analysisFunction=analyze, 
#     bias = 4, 
#     output = "result.csv"
# )