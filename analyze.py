import pandas as pd
from PETWorks.autoturn import findQualifiedAnonymityConfigs
from PETWorks.autoturn import generateAnonymityConfigs
from PETWorks.autoturn import calculateThresholds
from PETWorks.attributetypes import *
from PETWorks import PETValidation,report
import random



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
                    print("pass")          
                    continue
                else:
                    print(f"{test.__name__} {gender}{age_range} fail")
                    print(f"{od_result} - {ad_result} = {difference}")
                    return False
    # CSVNAME = "data/test/anony" + str(count) + ".csv"
    # anonymizedData.to_csv(CSVNAME,index=False)        
    return True
                
##測試用的註解



originalData = pd.read_csv("data/sport/sport_prepossed.csv",sep=";")
anontizedDate = pd.read_csv("data/anony62.csv", sep=',')
analyze(originalData,anontizedDate,4)
dataHierarchy="data/sport/sport_hierarchy"
anonymityConfigs="combination.csv"
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
}
