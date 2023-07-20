import pandas as pd
from PETWorks.autoturn import findQualifiedAnonymityConfigs
from PETWorks.autoturn import generateAnonymityConfigs
from PETWorks.autoturn import calculateThresholds
from PETWorks.attributetypes import *
from PETWorks import PETValidation,report

generateAnonymityConfigs(
    originalData="data/sport/sport_prepossed.csv",
    dataHierarchy="data/sport/sport_hierarchy",
    output="combination.csv",
    firstSampleCount=100,
    secondSampleCount=100
)