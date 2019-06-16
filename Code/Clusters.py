import Functions
import uuid
import os

class Clusters:
    ClustersList = []

    def addCluster(self, Cluster):
        self.ClustersList.append(Cluster)

    def removeCluster(self,Cluster):
        self.ClustersList.remove(Cluster)

    def getMinDiversity(self):
        if len(self.ClustersList) == 0:
            return 0

        minDiversity = self.ClustersList[0].getDiversity()
        for Cluster in self.ClustersList:
            clusterDiversity = Cluster.getDiversity()
            if clusterDiversity < minDiversity:
                minDiversity = clusterDiversity

        return minDiversity

    def getClusterByIndex(self,index):
        for Cluster in self.ClustersList:
            if Cluster.clusterIndex == index:
                return Cluster
        print("There is no Cluster with index ")

    def clustersSuitableForPerson(self, Person, l):
        output = []

        for Cluster in self.ClustersList:
            if Cluster.divWithPersonIsLegal(Person, l):
                output.append(Cluster)

        return output

    def clusterWithMinInformationLoss(self, Person,l):
        B = self.clustersSuitableForPerson(Person, l)
        highestMatchScore = 0
        HighestMatchCluster = B.pop()

        for Cluster in B:
            matchingScore = Cluster.matchingScoreByAddingPersonToCluster(Person)

            if matchingScore > highestMatchScore:
                HighestMatchCluster = Cluster
                highestMatchScore = matchingScore

        return HighestMatchCluster

    def removePersonClusterIfItEmpty(self,_Cluster):
        for Cluster in self.ClustersList:
            if _Cluster == Cluster:
                if Cluster.clusterSize == 0:
                    self.ClustersList.remove(Cluster)
                return

    def unifyClustersSmallerThanK(self, k):
        # sort clusters according to their size
        self.ClustersList.sort(key = lambda  C:C.clusterSize)

        FirstCluster = self.ClustersList[0]
        while FirstCluster.clusterSize < k:
            SecondCluster = self.ClustersList[1]
            SecondCluster.appendCluster(FirstCluster)

            self.removeCluster(FirstCluster)
            self.ClustersList.sort(key=lambda C: C.clusterSize)
            FirstCluster = self.ClustersList[0]

        # sort clusters according to their desc size
        self.ClustersList.sort(key=lambda C: C.clusterIndex, reverse=True)

    def spliteBigClusters(self, k, l):
        hadSplitted = False
        hadSplittedInThisIteration = True
        omega = 1.5

        while hadSplittedInThisIteration:
            hadSplittedInThisIteration = False
            for Cluster in self.ClustersList:
                if Cluster.clusterSize > omega * k:
                    ListOfPersons = Cluster.getPersons()
                    SplittedCluster = Functions.algorithm3(ListOfPersons, 2)
                    Cluster1 = SplittedCluster.ClustersList[0]
                    Cluster2 = SplittedCluster.ClustersList[1]
                    if Cluster1.divIsLegal(l) and Cluster2.divIsLegal(l):
                        self.ClustersList.remove(Cluster)
                        self.ClustersList.append(Cluster1)
                        self.ClustersList.append(Cluster2)
                        hadSplittedInThisIteration = True
                        hadSplitted = True

        return hadSplitted

    def printClusters(self):
        for Cluster in self.ClustersList:
            Cluster.printCluster()

    def printClustersToFile(self,k,l,n):
        dirpath = os.getcwd()

        path = dirpath + "/results/"

        fileName = "k="+ str(k) +"_l="+str(l) +"_n="+ str(n)

        txtFileName = fileName + ".txt"
        dataFileName = fileName + ".data"

        textFile = open(path + txtFileName, "w+")
        dataFile = open(path + dataFileName, "w+")

        textFileHeadLine = "Number of people = "+str(n) + "k = " + str(k) +", l = " + str(l) + "\n \n"
        textFile.write(textFileHeadLine)

        textFileSecondLine = self.getClusterValues()
        textFile.write(textFileSecondLine)

        for Cluster in self.ClustersList:
            # text file:
            textFile.write(Cluster.getClusterInfo())
            textFile.write("------------------------------------------ \n ")
            textFile.write("------------------------------------------ \n ")

            # data file:
            dataFile.write(Cluster.getNewValues())

        textFile.close()
        dataFile.close()

    def getClusterValues(self):
        Appearances = {'workclass': {}, 'education': {}, 'maritalStatus': {}, 'occupation': {},
                       'relationship': {}, 'race': {}, 'sex': {},
                       'nativeCountry': {}, 'salaryPerYear': {}}

        for key in Appearances:
            for Cluster in self.ClustersList:
                for instance in Cluster.Appearances[key].keys():
                    if instance not in Appearances[key]:
                        Appearances[key].update({instance: 1})

        appearancesString = ""
        for key in Appearances:
            appearancesString += key +": " + str(Appearances[key].__len__())+ " different  values \n"
            appearancesString+= str(Appearances[key].keys()) + "\n \n"

        NumericRange = {'age': "", 'fnlwgt': "", 'educationNum': "", 'capitalGain': "",
                        'capitalLoss': "", 'hoursPerWeek': ""}



        for key in NumericRange.keys():
            Range = self.ClustersList[0].getNumericRange(key)
            minVal = Range[0]
            maxVal = Range[1]

            for Cluster in self.ClustersList:
                ClusterRange = Cluster.getNumericRange(key)
                clusterMinVal = ClusterRange[0]
                clusterMaxVal = ClusterRange[1]

                if clusterMinVal<minVal:
                    minVal = clusterMinVal

                if clusterMaxVal>maxVal:
                    maxVal = clusterMaxVal

                NumericRange[key] = str(int(minVal)) + "-"+ str(int(maxVal))

        rangeString = ""
        for key in NumericRange:
            rangeString += "The range of '" + key +"' is: " + NumericRange[key] + "\n"

        return appearancesString + rangeString


