from random import randint
def makeListOfDictionaries(numOfPeople):
    data = []
    Countries = ['Japan', 'Israel', 'India','Switzerland', 'Spain']

    f = open("adult.data", "r")
    if f.mode == 'r':
        arrayOfStrings = f.readlines()
        primaryKey = {'value': 0}
        for line in arrayOfStrings:
            v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 = line.split(',')
            v1 = float(v1.replace(' ', ''))  # age
            v3 = float(v3.replace(' ', ''))  # fnlwgt
            v5 = float(v5.replace(' ', ''))  # educationNum
            v11 = float(v11.replace(' ', ''))  # capitalGain
            v12 = float(v12.replace(' ', ''))  # capitalLoss
            v13 = float(v13.replace(' ', ''))  # hoursPerWeek
            v14 = Countries[randint(0, Countries.__len__()-1)]

            Person = {'primaryKey': primaryKey['value'],
                      'clusterPointer': None,
                      'age': v1,
                      'workclass': v2,
                      'fnlwgt': v3,
                      'education': v4,
                      'educationNum': v5,
                      'maritalStatus': v6,
                      'occupation': v7,
                      'relationship': v8,
                      'race': v9,
                      'sex': v10,
                      'capitalGain': v11,
                      'capitalLoss': v12,
                      'hoursPerWeek': v13,
                      'nativeCountry': v14,
                      'salaryPerYear': v15}
            primaryKey['value'] = primaryKey['value'] + 1
            data.append(Person)

            if primaryKey['value'] == numOfPeople:
                break
    f.close()
    return data
