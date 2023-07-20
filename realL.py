from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER,SENSITIVE_ATTRIBUTE,IDENTIFIER
originalData = "data/sport/sport_prepossed.csv"
anonymizedData = "data/sport/sport_anony.csv"
dataHierarchy = "data/sport/sport_hierarchy"

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

ld = PETValidation(originalData, anonymizedData, "l-diversity", attributeTypes=attributeTypes, l=3)

print("l-diversity")
report(ld, "json")