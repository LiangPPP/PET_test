import pandas as pd
from PETWorks.autoturn import findQualifiedAnonymityConfigs
from PETWorks.autoturn import generateAnonymityConfigs
from PETWorks.autoturn import calculateThresholds
from PETWorks.attributetypes import *
from PETWorks import PETValidation,report
import random



def twoMinuteStepTest(data: pd.DataFrame) -> float:
    return data["2MinuteStepTest"].astype(float).mean()


def armCurlTest(data: pd.DataFrame):
    return data["30SecondArmCurlTest"].astype(float).mean()


def charStandTest(data: pd.DataFrame):
    return data["ChairStandTest"].astype(float).mean()


def footUpAndGoTest(data: pd.DataFrame):
    return data["8FootUpAndGoTest"].astype(float).mean()


def rightHand(data: pd.DataFrame):
    return data["RightHandGripStrengthTest"].astype(float).mean()


def singleLegBalanceRight(data: pd.DataFrame):
    return data["SingleLegBalanceRight"].astype(float).mean()


def singleLegBalanceLeft(data: pd.DataFrame):
    return data["SingleLegBalanceLeft"].astype(float).mean()

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
        except:
            data = data[data["birth_year"].astype(str) == f"[{range1}-{range2}]"]
        return data
    
    try:
        data = data[
        (data["birth_year"].astype(int) >= range1)
        & (data["birth_year"].astype(int) < range2)
        & (data["gender"].astype(str) == gender)
        ]
    except:
        data = data[
        (data["birth_year"].astype(str) == f"[{range1}-{range2}]")&(data["gender"].astype(str) == gender)
    ]
    return data





def analyze(originalData: pd.DataFrame, anonymizedData: pd.DataFrame ,error:int):                            
    count = random.randrange(1,5000000)
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
            ad_filtered = filter_anonymizedData_by_age_and_gender(anonymizedData,age_range[0],age_range[1],gender)
            
            
            for test in tests:
                
                od_result = test(od_filtered)
                ad_result = test(ad_filtered)
                
                difference = abs(od_result - ad_result)
                
                bias = 4
                
                if test.__name__ == "twoMinuteStepTest":
                    bias = 10
                    
                if difference < bias:  
                    print(f"{test.__name__} {gender}{age_range} pass")
                    print(f"{od_result} - {ad_result} = {difference}")          
                    continue
                else:
                    print(f"{test.__name__} {gender}{age_range} fail")
                    print(f"{od_result} - {ad_result} = {difference}")
                    return False
    CSVNAME = "data/test/anony" + str(count) + ".csv"
    anonymizedData.to_csv(CSVNAME,index=False)        
    return True
                

generateAnonymityConfigs(
    originalData="data/sport_new/raw_data_utf8_All_original.csv",
    dataHierarchy="data/sport_new/sport_hierarchy",
    output="combination.csv",
    firstSampleCount=1000,
    secondSampleCount=1000
)

findQualifiedAnonymityConfigs(
    originalData="data/sport_new/raw_data_utf8_All_original.csv",
    dataHierarchy="data/sport_new/sport_hierarchy",
    anonymityConfigs="combination.csv",
    attributeTypes={
        "_id": SENSITIVE_ATTRIBUTE,
        "birth_year": QUASI_IDENTIFIER,
        "gender": SENSITIVE_ATTRIBUTE,
        "start_date": QUASI_IDENTIFIER,
        "user_id": IDENTIFIER,
        "2MinuteStepTest":SENSITIVE_ATTRIBUTE,
        "30SecondArmCurlTest":SENSITIVE_ATTRIBUTE,
        "8FootUpAndGoTest":SENSITIVE_ATTRIBUTE,
        "ChairStandTest":SENSITIVE_ATTRIBUTE,
        "RightHandGripStrengthTest":SENSITIVE_ATTRIBUTE,
        "SingleLegBalanceLeft":SENSITIVE_ATTRIBUTE,
        "SingleLegBalanceRight":SENSITIVE_ATTRIBUTE,
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

