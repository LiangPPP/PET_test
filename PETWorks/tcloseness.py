import pandas as pd

from PETWorks.arx import (
    loadDataHierarchyNatively,
    getAttributeNameByType,
)
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER
import numpy as np
import pandas as pd
from math import fabs


def _computeHierarchicalDistance(
    dataDistribution: dict[str, float],
    groupDistribution: dict[str, float],
    sensitiveHierarchy: np.chararray,
) -> float:
    hierarchyWidth, hierarchyHeight = sensitiveHierarchy.shape

    extraArray = np.zeros((hierarchyWidth, hierarchyHeight), dtype=np.float32)
    costArray = np.zeros((hierarchyWidth, hierarchyHeight), dtype=np.float32)

    # loop through hierarchy height from 0
    for currentHeight in range(hierarchyHeight):
        for rowIndex in range(hierarchyWidth):
            # if leaf
            if currentHeight == 0:
                costArray[rowIndex, currentHeight] = 0.0

                value = sensitiveHierarchy[rowIndex, 0]
                extra = groupDistribution.get(value, 0) - dataDistribution.get(
                    value, 0
                )
                extraArray[rowIndex, currentHeight] = extra
                continue

            # if not leaf
            uniqueValues = np.unique(sensitiveHierarchy[:, currentHeight])
            for value in uniqueValues:
                rowIndicesWithMatchedValue = np.where(
                    sensitiveHierarchy[:, currentHeight] == value
                )[0]
                extraSubset = extraArray[
                    rowIndicesWithMatchedValue, currentHeight - 1
                ]
                maskForPositiveExtras = extraSubset > 0
                maskForNegativeExtras = extraSubset < 0

                positiveExtrasSum = np.sum(extraSubset[maskForPositiveExtras])
                negativeExtrasSum = -1 * np.sum(
                    extraSubset[maskForNegativeExtras]
                )

                extraArray[rowIndicesWithMatchedValue[0], currentHeight] = (
                    positiveExtrasSum - negativeExtrasSum
                )

                cost = float(currentHeight) * min(
                    positiveExtrasSum, negativeExtrasSum
                )
                cost /= hierarchyHeight - 1
                costArray[rowIndicesWithMatchedValue[0], currentHeight] = cost

    return float(np.sum(costArray))

def _computeEqualDistance(
        dataDistribution: dict[str, float],
        groupDistribution: dict[str, float],
) -> float:
    numRows = len(dataDistribution)
    extraList = [
        float(groupDistribution.get(value, 0) - dataDistribution.get(value, 0))
        for value in dataDistribution.keys()
    ]

    distance = 0.0
    for index in range(numRows):
        distance += fabs(extraList[index])
    distance /= 2

    return distance


def _computeNumericalDistance(
    dataDistribution: dict[str, float],
    groupDistribution: dict[str, float],
) -> float:
    sortedDataDistribution = {key: dataDistribution[key] for key in sorted(
        dataDistribution, key=lambda x: float("inf") if x=="" else float(x) 
    )}

    numRows = len(dataDistribution)

    extraList = [
        float(groupDistribution.get(key, 0) - dataDistribution.get(key, 0))
        for key in sortedDataDistribution.keys()
    ]

    distance = 0.0
    sum = 0.0
    for index in range(numRows - 1):
        sum += extraList[index]
        distance += fabs(sum)
    distance /= numRows - 1
    print(distance)
    return distance


def _computeTCloseness(
    originalData: pd.DataFrame,
    anonymizedData: pd.DataFrame,
    sensitiveAttributeName: str,
    qiNames: list[str],
    sensitiveHierarchy: np.chararray,
) -> float:
    # originalData = originalData.dropna()
    # anonymizedData = anonymizedData.dropna()
    
    
    

    dataDistribution = dict(
        originalData[sensitiveAttributeName].value_counts() / len(originalData)
    )
    
    anonymizedGroups = anonymizedData.groupby(qiNames)

    maxHierarchicalDistance = float("-inf")
    for _, group in anonymizedGroups:
        groupDistribution = dict(
            group[sensitiveAttributeName].value_counts() / len(group)
        )
        
        isNumeral = False
        #for 運動數據
        NumeralList = ["achievement_count", "elapsed_time","upper_extremity_muscle_strength"]
        for NumeralName in NumeralList:
            if sensitiveAttributeName == NumeralName:
                isNumeral = True
        
        # try:
        #     float(anonymizedData[sensitiveAttributeName].iloc[0])
        #     isNumeral = True
        # except ValueError:
        #     pass
        if isNumeral:
            distance = _computeNumericalDistance(
                dataDistribution,
                groupDistribution,
            )
        elif sensitiveHierarchy is not None:
            distance = _computeHierarchicalDistance(
                dataDistribution, groupDistribution, originalData[sensitiveAttributeName],
            )
        elif sensitiveHierarchy is None:
            distance = _computeEqualDistance(
                dataDistribution, groupDistribution, 
            )

        if distance > maxHierarchicalDistance:
            maxHierarchicalDistance = distance

    return maxHierarchicalDistance


def measureTCloseness(
    originalData: pd.DataFrame,
    anonymizedData: pd.DataFrame,
    sensitiveAttributeName: str,
    qiNames: list[str],
    sensitiveHierarchy: np.chararray,
) -> float:
    isNumerical = True
    # try:
    #     float(sensitiveHierarchy[0, 0])
    # except ValueError:
    #     isNumerical = False

    # if isNumerical:
    #     return _computeTCloseness(
    #         originalData, anonymizedData, sensitiveAttributeName, qiNames, None
    #     )

    return _computeTCloseness(
        originalData,
        anonymizedData,
        sensitiveAttributeName,
        qiNames,
        sensitiveHierarchy,
    )


def _validateTCloseness(tFromData: float, tLimit: float) -> bool:
    return tFromData < tLimit


def PETValidation(
    original, anonymized, _, dataHierarchy, attributeTypes, tLimit, **other
):
    tLimit = float(tLimit)

    dataHierarchy = loadDataHierarchyNatively(dataHierarchy, ";")
    originalData = pd.read_csv(original, sep=";", skipinitialspace=True)
    anonymizedData = pd.read_csv(anonymized, sep=";", skipinitialspace=True)

    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
    sensitiveAttributes = getAttributeNameByType(
        attributeTypes, SENSITIVE_ATTRIBUTE
    )

    tList = [
        measureTCloseness(
            originalData,
            anonymizedData,
            sensitiveAttribute,
            qiNames,
            dataHierarchy.get(sensitiveAttribute, None),
        )
        for sensitiveAttribute in sensitiveAttributes
    ]

    fullfilTCloseness = all(_validateTCloseness(t, tLimit) for t in tList)

    return {"t": tLimit, "fullfil t-closeness": fullfilTCloseness, "actual": max(tList)}