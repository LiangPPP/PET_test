from typing import Dict
from PETWorks.arx import getAttributeNameByType
import pandas as pd

from itertools import combinations

from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE

def measureLDiversityRelaxed(
    anonymizedData: pd.DataFrame,
    attributeTypes: Dict[str, str],
) -> list[int]:
    
    anonymizedData = anonymizedData.fillna(0)
    anonymizedData = anonymizedData.drop('user_id',axis = 1)
    lValues = []

    grouping_columns = []

    for attribute, attr_type in attributeTypes.items():
        if attr_type == "quasi_identifier":
            grouping_columns.append(attribute)

    # 以 'birth_year' 和 'start_date' 分群
    groups = anonymizedData.groupby(grouping_columns)

    # 查看每個分群中的不重複資料數量
    for group_key, group in groups:
        unique_records = group.drop_duplicates().shape[0]  # 或者使用 len(group.drop_duplicates())
        # print(f"Birth Year: {birth_year}, Start Date: {start_date}")
        # print(f"Number of unique records: {unique_records}\n")
        lValues += [unique_records]
        
   
    l =[]
    l.append(min(lValues))

    return l


def measureLDiversity(
    anonymizedData: pd.DataFrame,
    attributeTypes: Dict[str, str],
) -> list[int]:
    
    anonymizedData = anonymizedData.fillna(0)
    anonymizedData = anonymizedData.drop('user_id',axis = 1)
    lValues = []
    grouping_columns = []

    for attribute, attr_type in attributeTypes.items():
        if attr_type == "quasi_identifier":
            grouping_columns.append(attribute)
    
    groups = anonymizedData.groupby(grouping_columns)

    # 查看每個分群中的每個欄位有多少種不同的資料
    for group_key, group in groups:
        unique_counts = group.nunique()
        unique_counts = unique_counts.drop(grouping_columns)
        min_unique_count = unique_counts.min()

        lValues += [int(min_unique_count)]
        
    
    l = []
    l.append(min(lValues))
   

    return l

def validateLDiversity(lValues: int, lLimit: int) -> bool:
    return lValues >= lLimit
    # return all(value >= lLimit for value in lValues)


def PETValidation(original, anonymized, _, attributeTypes, l):

    anonymizedDataFrame = pd.read_csv(anonymized, sep=";")

    lValues_strict = measureLDiversity(anonymizedDataFrame, attributeTypes)
    lValues_relax = measureLDiversityRelaxed(anonymizedDataFrame,attributeTypes)
    fulfillLDiversity = validateLDiversity(lValues_relax, l)

    return {"l": l, "fulfill l-diversity": fulfillLDiversity, "actual_strict": lValues_strict,"actual_relax": lValues_relax}
