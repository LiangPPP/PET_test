import pandas as pd
from PETWorks.autoturn import findQualifiedAnonymityConfigs
from PETWorks.autoturn import generateAnonymityConfigs
from PETWorks.autoturn import calculateThresholds
from PETWorks.attributetypes import *
from PETWorks import PETValidation,report
import random



def twoMinuteStepTest(data: pd.DataFrame) -> float:
    return data["achievement_count"].astype(float).mean()

def filter_originalData_by_age_and_gender(
    data: pd.DataFrame, range1: int, range2: int, gender: str
):
    if gender is None:
        return data[
            (data["birth_year"].astype(int) >= range1)
            & (data["birth_year"].astype(int) < range2)
        ]
    return data[
        (data["birth_year"].astype(int) >= range1)
        & (data["birth_year"].astype(int) < range2)
        & (data["gender"].astype(str) == gender)
    ]


def filter_anonymizedData_by_age_and_gender(data: pd.DataFrame, range1: int,range2: int, gender: str):
    
    if gender is None:
        try:
            data = data[
            (data["birth_year"].astype(int) >= range1)
            & (data["birth_year"].astype(int) < range2)
        ]
            return data
        except:
            data = data[data["birth_year"].astype(str) == f"[{range1}-{range2}]"]
            
            return data
    
    try:
        data = data[
        (data["birth_year"].astype(int) >= range1)
        & (data["birth_year"].astype(int) < range2)
        & (data["gender"].astype(str) == gender)
        ]
        return data
    except:
        data = data[
        (data["birth_year"].astype(str) == f"[{range1}-{range2}]")&(data["gender"].astype(str) == gender)
    ]
        
        return data





def analyze(originalData: pd.DataFrame, anonymizedData: pd.DataFrame ,error:int):                            
    age_ranges = [(1930, 1940), (1940, 1950), (1950, 1960), (1960, 1970)]
    genders = ['女', '男', None]
    tests = [
        twoMinuteStepTest,
    ]
    
    for age_range in age_ranges:
            
        for gender in genders:
            print(gender)
            print(age_range)
            od_filtered = filter_originalData_by_age_and_gender(originalData,age_range[0],age_range[1],gender)
            print("od_filtere")
            print(od_filtered)
            ad_filtered = filter_anonymizedData_by_age_and_gender(anonymizedData,age_range[0],age_range[1],gender)
            print("ad_filtered")
            print(ad_filtered)
            
            
            for test in tests:
                
                od_result = test(od_filtered)
                print("OD:")
                print(od_result)
                ad_result = test(ad_filtered)
                print("AD:")
                print(ad_result)
                
                difference = abs(od_result - ad_result)
                
                bias = 10
                
                
                    
                if difference < bias:
                    print(f"{test.__name__} {gender}{age_range} pass")
                    print(f"{od_result} - {ad_result} = {difference}")                    
                    continue
                else:
                    print(f"{test.__name__} {gender}{age_range} fail")
                    print(f"{od_result} - {ad_result} = {difference}")
                    return False
    return True
                

# generateAnonymityConfigs(
#     originalData="data/sport_new/raw_data_utf8_2MinuteStepTest_original.csv",
#     dataHierarchy="data/sport_new/sport_hierarchy",
#     output="combination.csv",
#     firstSampleCount=10,
#     secondSampleCount=10
# )

originalDataList = ["data/sport_new/raw_data_utf8_2MinuteStepTest_original.csv",
                    "data/sport_new/raw_data_utf8_8FootUpAndGoTest_original.csv",
                    "data/sport_new/raw_data_utf8_30SecondArmCurlTest_original.csv",
                    "data/sport_new/raw_data_utf8_ChairStandTest_original.csv",
                    "data/sport_new/raw_data_utf8_RightHandGripStrengthTest_original.csv",
                    "data/sport_new/raw_data_utf8_SingleLegBalanceLeft_original.csv",
                    "data/sport_new/raw_data_utf8_SingleLegBalanceRight_original.csv"]

findQualifiedAnonymityConfigs(
    originalData="data/sport_new/raw_data_utf8_2MinuteStepTest_original.csv",
    dataHierarchy="data/sport_new/sport_hierarchy",
    anonymityConfigs="combination_.csv",
    attributeTypes={
        "_id": SENSITIVE_ATTRIBUTE,
        "achievement_count": SENSITIVE_ATTRIBUTE,
        "birth_year": QUASI_IDENTIFIER,
        "city": SENSITIVE_ATTRIBUTE,
        "elapsed_time": SENSITIVE_ATTRIBUTE,
        "gender": SENSITIVE_ATTRIBUTE,
        "main_type": SENSITIVE_ATTRIBUTE,
        "start_date": QUASI_IDENTIFIER,
        "subtype": SENSITIVE_ATTRIBUTE,
        "type": SENSITIVE_ATTRIBUTE,
        "upper_extremity_muscle_strength": SENSITIVE_ATTRIBUTE,
        "user_id": IDENTIFIER,
    },
    analysisFunction=analyze, 
    bias = 4, 
    output = "result.csv"
)
result = "result.csv"
ot = "result.json"
calculateThresholds(
    result, ot
)

