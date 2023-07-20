from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER,SENSITIVE_ATTRIBUTE,IDENTIFIER
originalData = "data/sport/sport2.csv"
anonymizedData = "data/sport/sport_anony.csv"
dataHierarchy = "data/sport/sport_hierarchy"

attributeTypes={
        "_id": IDENTIFIER,
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
        "user_id": SENSITIVE_ATTRIBUTE,
    }

t = PETValidation(originalData,anonymizedData,"t-closeness",dataHierarchy=dataHierarchy,attributeTypes=attributeTypes,tLimit = 3)
print("t-closeness")
report(t,"json")