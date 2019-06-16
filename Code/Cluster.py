class Cluster:
    clusterIndex = 0
    # Persons = bintrees.AVLTree()
    Persons = {}
    Appearances = {}
    NumericFieldsRange = {}
    NumericFieldsSum = {}
    clusterSize = 0

    def __init__(self, clusterIndex):
        self.clusterIndex = clusterIndex

        self.Persons = {}

        self.Appearances = {'age': {}, 'workclass': {}, 'fnlwgt': {}, 'education': {},
                            'educationNum': {}, 'maritalStatus': {}, 'occupation': {},
                            'relationship': {}, 'race': {}, 'sex': {}, 'capitalGain': {},
                            'capitalLoss': {}, 'hoursPerWeek': {}, 'nativeCountry': {},
                            'salaryPerYear': {}}

        self.NumericFieldsRange = {'age': {}, 'fnlwgt': {}, 'educationNum': {}, 'capitalGain': {},
                                   'capitalLoss': {}, 'hoursPerWeek': {}}

        self.NumericFieldsSum = {'age': 0, 'fnlwgt': 0, 'educationNum': 0, 'capitalGain': 0,
                                 'capitalLoss': 0, 'hoursPerWeek': 0}

    def getClusterSize(self):
        return self.clusterSize

    # return Person[]
    def getPersons(self):
        PersonsList = []
        for pk in self.Persons.keys():
            PersonsList.append(self.Persons[pk])
        return PersonsList

    def getDiversity(self):
        output = len(self.Appearances['nativeCountry'].keys())

        # if output < 1:
        #     print("bug")

        return output


    # update one filed in the 'Cluster Data'
    def updateAppearances(self, field, fieldValue, addOrRemove):
        if addOrRemove == "add":
            if fieldValue not in self.Appearances[field]:
                self.Appearances[field].update({fieldValue: 1})
            else:
                newValue = self.Appearances[field][fieldValue] + 1
                self.Appearances[field].update({fieldValue: newValue})
        else:  # addOrRemove == "remove"
            if fieldValue not in self.Appearances[field]:
                raise Exception("Bug in removing person from Appearances")
            oldValue = self.Appearances[field][fieldValue]

            # delete the element from the dict in case it was the last appearance
            if oldValue == 1:
                # del self.Appearances[field][fieldValue]
                self.Appearances[field].pop(fieldValue)
            # decrease in 1 if it wasn't the last appearance
            else:
                self.Appearances[field].update({fieldValue: oldValue - 1})

    # update one filed in the 'Numeric Field Range'
    def updateNumericFieldRange(self, fieldName, Person, addOrRemove):
        personValue = Person[fieldName]
        if addOrRemove == "add":
            if self.clusterSize == 0:
                self.NumericFieldsRange[fieldName].update({'min': personValue})
                self.NumericFieldsRange[fieldName].update({'max': personValue})
            else:
                min = self.NumericFieldsRange[fieldName]['min']
                max = self.NumericFieldsRange[fieldName]['max']

                if personValue > max:
                    self.NumericFieldsRange[fieldName].update({'max': personValue})
                    return
                if personValue < min:
                    self.NumericFieldsRange[fieldName].update({'min': personValue})
                    return
        else:  # addOrRemove == "remove"
            min = self.NumericFieldsRange[fieldName]['min']
            max = self.NumericFieldsRange[fieldName]['max']

            if (min < personValue < max) or (
                    personValue in self.Appearances[fieldName] and self.Appearances[fieldName][Person[fieldName]] > 1):
                return
            else:
                if self.clusterSize == 0:
                    del self.NumericFieldsRange[fieldName]['min']
                    del self.NumericFieldsRange[fieldName]['max']
                    return

                keysList = list(self.Appearances[fieldName].keys())
                minVal = keysList[0]
                maxVal = minVal

                for key in self.Appearances[fieldName].keys():
                    key = float(key)
                    if key > maxVal:
                        maxVal = key
                    if key < minVal:
                        minVal = key

                self.NumericFieldsRange[fieldName].update({'min': minVal})
                self.NumericFieldsRange[fieldName].update({'max': maxVal})
                return

    # update all the numeric fileds in the 'Numeric Field Range'
    def updateNumericFieldsRange(self, Person, addOrRemove):
        self.updateNumericFieldRange('age', Person, addOrRemove)
        self.updateNumericFieldRange('fnlwgt', Person, addOrRemove)
        self.updateNumericFieldRange('educationNum', Person, addOrRemove)
        self.updateNumericFieldRange('capitalGain', Person, addOrRemove)
        self.updateNumericFieldRange('capitalLoss', Person, addOrRemove)
        self.updateNumericFieldRange('hoursPerWeek', Person, addOrRemove)

    def updateNumericFieldsSum(self, Person, addOrRemove):
        self.updateNumericFieldSum('age', Person, addOrRemove)
        self.updateNumericFieldSum('fnlwgt', Person, addOrRemove)
        self.updateNumericFieldSum('educationNum', Person, addOrRemove)
        self.updateNumericFieldSum('capitalGain', Person, addOrRemove)
        self.updateNumericFieldSum('capitalLoss', Person, addOrRemove)
        self.updateNumericFieldSum('hoursPerWeek', Person, addOrRemove)

    def updateNumericFieldSum(self, fieldName, Person, addOrRemove):
        personValue = float(Person[fieldName])
        if addOrRemove == "add":
            self.NumericFieldsSum[fieldName] += personValue
        else:  # addOrRemove == "remove"
            self.NumericFieldsSum[fieldName] -= personValue

    # add person to the Cluster
    def addPerson(self, Person):
        self.Persons.update({Person['primaryKey']: Person})
        self.updateNumericFieldsRange(Person, "add")
        self.updateNumericFieldsSum(Person, "add")
        self.clusterSize += 1
        Person['clusterPointer'] = self

        for key, value in Person.items():
            if (key != 'cluster' and key != 'primaryKey' and key != 'clusterPointer'):
                self.updateAppearances(key, value, "add")

    def removePerson(self, Person):
        self.updateClusterDataWithPerson(Person,"remove")

        # for key, value in Person.items():
        #     if (key != 'cluster' and key != 'primaryKey' and key != 'clusterPointer'):
        #         self.updateAppearances(key, value, "remove")

        self.clusterSize -= 1

        self.updateNumericFieldsRange(Person, "remove")
        self.Persons.pop(Person['primaryKey'])
        self.updateNumericFieldsSum(Person, "remove")

        Person['cluster'] = -1
        Person['clusterPointer'] = None

    def getNumericRange(self, fieldName):
        return [self.NumericFieldsRange[fieldName]['min'], self.NumericFieldsRange[fieldName]['max']]

    def calcLossforNumericField(self, fieldName, personValue):
        personValue = float(personValue)
        distanceFromAvg = abs(self.getAverage(fieldName) - personValue)
        RangeValues = self.getNumericRange(fieldName)
        minVal = RangeValues[0]
        maxVal = RangeValues[1]

        if minVal <= personValue <= maxVal:
            if distanceFromAvg <= 1:
                return 1
            else:
                return (1 / distanceFromAvg)
        else:  # not in range
            oldRangeSize = maxVal - minVal
            newRangeSize = 0
            if personValue < minVal:
                newRangeSize = maxVal - minVal
            if personValue > maxVal:
                newRangeSize = personValue - minVal

            if oldRangeSize == 0:
                oldRangeSize = 1

            return (-1) * (self.clusterSize / 10) * (newRangeSize / oldRangeSize)

    def calcLossforNonNumericField(self, fieldName, personValue):
        if personValue in self.Appearances[fieldName]:
            numOfSameValues = self.Appearances[fieldName][personValue] + 1
            return numOfSameValues / self.clusterSize
        else:
            numOfKeys = self.Appearances.keys().__len__()
            return (-1 / 10) * ((numOfKeys + 1) / numOfKeys) * (self.clusterSize)

    def matchingScoreByAddingPersonToCluster(self, Person):
        ageScore = self.calcLossforNumericField('age', Person['age'])
        workclassScore = self.calcLossforNonNumericField('workclass', Person['workclass'])
        fnlwgtScore = self.calcLossforNumericField('fnlwgt', Person['fnlwgt'])
        educationScore = self.calcLossforNonNumericField('education', Person['education'])
        educationNumScore = self.calcLossforNumericField('educationNum', Person['educationNum'])
        maritalStatusScore = self.calcLossforNonNumericField('maritalStatus', Person['maritalStatus'])
        occupationScore = self.calcLossforNonNumericField('occupation', Person['occupation'])
        relationshipScore = self.calcLossforNonNumericField('relationship', Person['relationship'])
        raceScore = self.calcLossforNonNumericField('race', Person['race'])
        sexScore = self.calcLossforNonNumericField('sex', Person['sex'])
        capitalGainScore = self.calcLossforNumericField('capitalGain', Person['capitalGain'])
        capitalLossScore = self.calcLossforNumericField('capitalLoss', Person['capitalLoss'])
        hoursPerWeekScore = self.calcLossforNumericField('hoursPerWeek', Person['hoursPerWeek'])
        salaryPerYearScore = self.calcLossforNonNumericField('salaryPerYear', Person['salaryPerYear'])

        totalLost = ageScore + workclassScore + fnlwgtScore + educationScore + educationNumScore + maritalStatusScore + occupationScore + relationshipScore + raceScore + sexScore + capitalGainScore + capitalLossScore + hoursPerWeekScore + salaryPerYearScore

        return totalLost

    def divOfClusterWithoutPeople(self, Person):
        personCountry = Person['nativeCountry']
        clusterDiversity = self.getDiversity()
        if (personCountry in self.Appearances['nativeCountry']) and (
                self.Appearances['nativeCountry'][personCountry]) > 1:
            return clusterDiversity
        else:
            return clusterDiversity - 1

    def divOfClusterWithPeople(self, Person):
        personCountry = Person['nativeCountry']
        clusterDiversity = self.getDiversity()
        if (personCountry in self.Appearances['nativeCountry']):
            return clusterDiversity

        return clusterDiversity + 1

    def divWithoutPersonIsLegal(self, Person, l):
        return self.divOfClusterWithoutPeople(Person) >= l

    def divWithPersonIsLegal(self, Person, l):
        return self.divOfClusterWithPeople(Person) > l

    def getAverage(self, fieldName):
        return self.NumericFieldsSum[fieldName] / self.clusterSize

    def divIsLegal(self, l):
        numOfUniqueValues = self.Appearances['nativeCountry'].__len__()
        return numOfUniqueValues >= l

    def appendCluster(self, Cluster):
        for Person in Cluster.Persons.values():
            self.addPerson(Person)


    def printCluster(self):
        print("Cluster index is: " + str(self.clusterIndex))
        print("Cluster size is: " + str(self.clusterSize))
        print()
        print("Numeric fileds range:")
        for numKey in self.NumericFieldsRange:
            print(numKey + ":")
            print(self.NumericFieldsRange[numKey])

        print()
        print("Non-Numeric fileds:")
        for key in self.Appearances:
            print(key + ":")
            print(self.Appearances[key])
        print("-----------------------------")

    def updateClusterDataWithPerson(self, Person, addOrRemove):
        if addOrRemove == 'add':
            self.updateAppearances('age', Person['age'], "add")
            self.updateAppearances('workclass', Person['workclass'], "add")
            self.updateAppearances('fnlwgt', Person['fnlwgt'], "add")
            self.updateAppearances('education', Person['education'], "add")
            self.updateAppearances('educationNum', Person['educationNum'], "add")
            self.updateAppearances('maritalStatus', Person['maritalStatus'], "add")
            self.updateAppearances('occupation', Person['occupation'], "add")
            self.updateAppearances('relationship', Person['relationship'], "add")
            self.updateAppearances('race', Person['race'], "add")
            self.updateAppearances('sex', Person['sex'], "add")
            self.updateAppearances('capitalGain', Person['capitalGain'], "add")
            self.updateAppearances('capitalLoss', Person['capitalLoss'], "add")
            self.updateAppearances('hoursPerWeek', Person['hoursPerWeek'], "add")
            self.updateAppearances('nativeCountry', Person['nativeCountry'], "add")
            self.updateAppearances('salaryPerYear', Person['salaryPerYear'], "add")
        else:
            try:
                self.updateAppearances('age', Person['age'], "remove")
            except:
                print("bugg")

            self.updateAppearances('workclass', Person['workclass'], "remove")
            self.updateAppearances('fnlwgt', Person['fnlwgt'], "remove")
            self.updateAppearances('education', Person['education'], "remove")
            self.updateAppearances('educationNum', Person['educationNum'], "remove")
            self.updateAppearances('maritalStatus', Person['maritalStatus'], "remove")
            self.updateAppearances('occupation', Person['occupation'], "remove")
            self.updateAppearances('relationship', Person['relationship'], "remove")
            self.updateAppearances('race', Person['race'], "remove")
            self.updateAppearances('sex', Person['sex'], "remove")
            self.updateAppearances('capitalGain', Person['capitalGain'], "remove")
            self.updateAppearances('capitalLoss', Person['capitalLoss'], "remove")
            self.updateAppearances('hoursPerWeek', Person['hoursPerWeek'], "remove")
            self.updateAppearances('nativeCountry', Person['nativeCountry'], "remove")
            self.updateAppearances('salaryPerYear', Person['salaryPerYear'], "remove")

    def getClusterInfo(self):
        l1 = "Cluster size is: " + str(self.clusterSize) +"\n \n"
        l2 = "Numeric fileds range: \n"
        for numKey in self.NumericFieldsRange:
            l2 = l2 + numKey + ": \n" + str(self.NumericFieldsRange[numKey]) + "\n"

        l3 = "\nNon-Numeric fileds:" + "\n"
        for key in self.Appearances:
            if (key !='age') and (key != 'fnlwgt') and  (key != 'educationNum') and (key != 'capitalGain') and (key != 'capitalLoss') and (key != 'hoursPerWeek'):
                l3 = l3 + key + ": \n" + str(self.Appearances[key]) + "\n"

        return l1 + l2 + l3

    def getNewValues(self):
        output = ""

        age = self.getNumericRangeString('age')
        workclass = self.getNonNumericFieldString('workclass')
        fnlwgt = self.getNumericRangeString('fnlwgt')
        education = self.getNonNumericFieldString('education')
        educationNum = self.getNumericRangeString('educationNum')
        maritalStatus = self.getNonNumericFieldString('maritalStatus')
        occupation = self.getNonNumericFieldString('occupation')
        relationship = self.getNonNumericFieldString('relationship')
        race = self.getNonNumericFieldString('race')
        sex = self.getNonNumericFieldString('sex')
        capitalGain = self.getNumericRangeString('capitalGain')
        capitalLoss = self.getNumericRangeString('capitalLoss')
        hoursPerWeek = self.getNumericRangeString('hoursPerWeek')
        # nativeCountry = ""
        salaryPerYear = self.getNonNumericFieldString('salaryPerYear')

        stringBeforeNativeCountry = age +", "+ workclass +", "+ fnlwgt +", "+ education +", "+ educationNum +", "+ maritalStatus +", "+ occupation +", "+ relationship +", "+ race +", "+ sex +", "+ capitalGain +", "+ capitalLoss +", "+ hoursPerWeek +", "

        for Person in self.Persons.values():
            nativeCountry = Person['nativeCountry']

            newPerson = stringBeforeNativeCountry + nativeCountry +", "+ salaryPerYear
            output = output + newPerson + "\n"

        return output

    def getNumericRangeString(self, fieldName):
        range = self.getNumericRange(fieldName)
        return str(int(range[0])) + "-" + str(int(range[1]))

    def getNonNumericFieldString(self, fieldName):
        output = ""
        Keys = self.Appearances[fieldName].keys()
        for key in Keys:
            output = output + key + "|"

        output = output[0:len(output)-1]

        return output

