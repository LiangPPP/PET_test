from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER,SENSITIVE_ATTRIBUTE,IDENTIFIER
originalData = "data/sport_new/raw_data_utf8_SingleLegBalanceRight_original.csv"
anonymizedData = "data/anony9.csv"
dataHierarchy = "data/sport_new/sport_hierarchy"

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
k = PETValidation(originalData, anonymizedData, "k-anonymity", attributeTypes=attributeTypes, k=10)
# a = PETValidation(
#     originalData, anonymizedData,
#     "Ambiguity",
#     dataHierarchy=dataHierarchy,
#     attributeTypes=attributeTypes
# )
# P = PETValidation(
#     originalData, anonymizedData,
#     "Precision",
#     dataHierarchy=dataHierarchy,
#     attributeTypes=attributeTypes
# )
# e = PETValidation(
#     originalData, anonymizedData,
#     "Non-Uniform Entropy",
#     dataHierarchy=dataHierarchy,
#     attributeTypes=attributeTypes
# )
# aecs = PETValidation(
#     originalData, anonymizedData,
#     "AECS",
#     attributeTypes=attributeTypes
# )
# d = PETValidation(originalData, anonymizedData, "d-presence", dataHierarchy=dataHierarchy, attributeTypes=attributeTypes, dMin=1/2, dMax=2/3)
# PRO = PETValidation(
#     originalData,
#     anonymizedData,
#     "profitability",
#     dataHierarchy=dataHierarchy,
#     attributeTypes=attributeTypes,
#     allowAttack=True,
#     adversaryCost=4,
#     adversaryGain=300,
#     publisherLost=300,
#     publisherBenefit=1200
# )
# ld = PETValidation(originalData, anonymizedData, "l-diversity", attributeTypes=attributeTypes, l=3)

# print("l-diversity")
# report(ld, "json")
# print("pro")
# report(PRO, "json")
# print("d")
# report(d, "json")
# print("aecs")
# report(aecs, "json")
# print("e")
# report(e, "json")
# print("P")
# report(P, "json")
print("K")
report(k, "json")
# print("a")
# report(a, "json")
