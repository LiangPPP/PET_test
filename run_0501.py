from PETWorks.autoturn import generateAnonymityConfigs

generateAnonymityConfigs(
    originalData="data/sport/sport_prepossed.csv",
    dataHierarchy="data/sport/sport_hierarchy",
    output="combination.csv",
    firstSampleCount=10000,
    secondSampleCount=10000
)