from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER,SENSITIVE_ATTRIBUTE,IDENTIFIER,INSENSITIVE_ATTRIBUTE
originalData = "data/sport/sport_new_original_one.csv"
anonymizedData = "data/sport/sport_new_anonymity_one.csv"
dataHierarchy = "data/sport/sport_new_hierarchy"

attributeTypes={
        "_id": INSENSITIVE_ATTRIBUTE,
        "birth_year": QUASI_IDENTIFIER,
        "gender": QUASI_IDENTIFIER,
        "user_id": IDENTIFIER,
        "2MinuteStepTest":INSENSITIVE_ATTRIBUTE,
        "30SecondArmCurlTest":INSENSITIVE_ATTRIBUTE,
        "8FootUpAndGoTest":INSENSITIVE_ATTRIBUTE,
        "ChairStandTest":INSENSITIVE_ATTRIBUTE,
        "RightHandGripStrengthTest":INSENSITIVE_ATTRIBUTE,
        "SingleLegBalanceLeft":INSENSITIVE_ATTRIBUTE,
        "SingleLegBalanceRight":INSENSITIVE_ATTRIBUTE,
        
    }
k = PETValidation(originalData, anonymizedData, "k-anonymity", attributeTypes=attributeTypes, k=10)

ld = PETValidation(originalData, anonymizedData, "l-diversity", attributeTypes=attributeTypes, l=3)

print("l-diversity")
report(ld, "json")

print("K")
report(k, "json")

